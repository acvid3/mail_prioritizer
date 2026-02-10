import os
import requests
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

router = APIRouter()

class CreateLabelRequest(BaseModel):
    name: str

class MoveEmailRequest(BaseModel):
    email_id: str
    label_name: str

def verify_google_token(access_token: str) -> bool:
    try:
        response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return response.status_code == 200
    except:
        return False

def get_or_create_label(access_token: str, label_name: str) -> str:
    gmail_api_url = "https://gmail.googleapis.com/gmail/v1/users/me/labels"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Check if label exists
    response = requests.get(gmail_api_url, headers=headers)
    if response.status_code == 200:
        labels = response.json().get("labels", [])
        for label in labels:
            if label.get("name") == label_name:
                return label["id"]
    
    # Create new label
    create_label_data = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }
    
    response = requests.post(gmail_api_url, headers=headers, json=create_label_data)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise Exception(f"Failed to create label: {response.text}")

@router.post("/labels/create")
def create_label(request: CreateLabelRequest, authorization: str = Header(None), token: str = None):
    access_token = None
    if authorization and authorization.startswith("Bearer "):
        access_token = authorization.split(" ")[1]
    elif token:
        access_token = token
    else:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    if not verify_google_token(access_token):
        raise HTTPException(status_code=401, detail="Invalid Google OAuth token")
    
    try:
        label_id = get_or_create_label(access_token, request.name)
        return {
            "success": True,
            "label_id": label_id,
            "label_name": request.name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/emails/move")
def move_email_to_label(request: MoveEmailRequest, authorization: str = Header(None), token: str = None):
    access_token = None
    if authorization and authorization.startswith("Bearer "):
        access_token = authorization.split(" ")[1]
    elif token:
        access_token = token
    else:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    if not verify_google_token(access_token):
        raise HTTPException(status_code=401, detail="Invalid Google OAuth token")
    
    try:
        # Get or create label
        label_id = get_or_create_label(access_token, request.label_name)
        
        # Move email to label
        gmail_api_url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{request.email_id}/modify"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        modify_data = {
            "addLabelIds": [label_id]
        }
        
        response = requests.post(gmail_api_url, headers=headers, json=modify_data)
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Email moved to label '{request.label_name}'",
                "label_id": label_id,
                "email_id": request.email_id
            }
        else:
            return {
                "success": False,
                "error": f"Failed to move email: {response.text}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/emails/classify-and-move")
def classify_and_move_email(request: MoveEmailRequest, authorization: str = Header(None), token: str = None):
    access_token = None
    if authorization and authorization.startswith("Bearer "):
        access_token = authorization.split(" ")[1]
    elif token:
        access_token = token
    else:
        raise HTTPException(status_code=401, detail="Authorization required")
    
    if not verify_google_token(access_token):
        raise HTTPException(status_code=401, detail="Invalid Google OAuth token")
    
    try:
        # Get email details first
        gmail_api_url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{request.email_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(gmail_api_url, headers=headers, params={"format": "full"})
        if response.status_code != 200:
            return {
                "success": False,
                "error": "Failed to fetch email details"
            }
        
        email_data = response.json()
        payload = email_data.get('payload', {})
        headers_list = payload.get('headers', [])
        
        subject = next((h['value'] for h in headers_list if h['name'] == 'Subject'), 'No Subject')
        from_email = next((h['value'] for h in headers_list if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers_list if h['name'] == 'Date'), 'Unknown')
        snippet = email_data.get('snippet', '')
        
        # Classify email
        text = f"{subject} {snippet}".lower()
        
        if "invoice" in text or "payment" in text or "overdue" in text:
            label_name = "AI_URGENT"
        else:
            label_name = "AI_IMPORTANT"
        
        # Move to classified label
        label_id = get_or_create_label(access_token, label_name)
        
        modify_url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{request.email_id}/modify"
        modify_data = {
            "addLabelIds": [label_id]
        }
        
        modify_response = requests.post(modify_url, headers=headers, json=modify_data)
        if modify_response.status_code == 200:
            return {
                "success": True,
                "message": f"Email classified as '{label_name}' and moved to label",
                "label_name": label_name,
                "label_id": label_id,
                "email_id": request.email_id,
                "classification": {
                    "subject": subject,
                    "from": from_email,
                    "priority": "high" if label_name == "AI_URGENT" else "medium"
                }
            }
        else:
            return {
                "success": False,
                "error": f"Failed to move email: {modify_response.text}"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

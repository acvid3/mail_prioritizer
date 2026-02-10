import os
import requests
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from ..services.gmail_utils import get_message_content

router = APIRouter()

GMAIL_API_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

@router.get("/emails")
def get_emails(request: Request, authorization: str = Header(None), max_results: int = 10, token: str = None):
    print(f"=== Request headers: {dict(request.headers)} ===")
    print(f"=== Authorization header: {authorization} ===")
    print(f"=== Token param: {token} ===")
    
    # Try to get token from multiple sources
    access_token = None
    
    if authorization and authorization.startswith("Bearer "):
        access_token = authorization.split(" ")[1]
        print(f"=== Using token from Authorization header ===")
    elif token:
        access_token = token
        print(f"=== Using token from query parameter ===")
    else:
        print(f"=== No token found ===")
        raise HTTPException(status_code=401, detail="Authorization header required. Use: Authorization: Bearer YOUR_ACCESS_TOKEN")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    try:
        # Get email list
        params = {
            "maxResults": max_results,
            "format": "metadata"
        }
        
        response = requests.get(GMAIL_API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            
            result = []
            for msg in messages:
                # Get details for each email
                detail_response = requests.get(f"{GMAIL_API_URL}/{msg['id']}", headers=headers, params={"format": "full"})
                if detail_response.status_code == 200:
                    msg_detail = detail_response.json()
                    payload = msg_detail.get('payload', {})
                    headers_list = payload.get('headers', [])
                    
                    # Extract headers
                    subject = next((h['value'] for h in headers_list if h['name'] == 'Subject'), 'No Subject')
                    from_email = next((h['value'] for h in headers_list if h['name'] == 'From'), 'Unknown')
                    date = next((h['value'] for h in headers_list if h['name'] == 'Date'), 'Unknown')
                    snippet = msg_detail.get('snippet', '')
                    
                    # Get full text
                    full_content = get_message_content(msg['id'], headers, GMAIL_API_URL)
                    
                    result.append({
                        "id": msg['id'],
                        "threadId": msg['threadId'],
                        "subject": subject,
                        "from": from_email,
                        "date": date,
                        "snippet": snippet,
                        "content": full_content
                    })
            
            return JSONResponse({
                "success": True,
                "count": len(result),
                "emails": result
            })
        else:
            return JSONResponse({
                "success": False,
                "error": f"Gmail API error: {response.status_code}",
                "details": response.text
            }, status_code=response.status_code)
            
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

def get_message_content(message_id: str, headers: dict):
    import requests
    import base64
    
    GMAIL_API_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
    
    response = requests.get(f"{GMAIL_API_URL}/{message_id}", headers=headers, params={"format": "full"})
    if response.status_code == 200:
        msg = response.json()
        payload = msg.get('payload', {})
        
        text_content = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        try:
                            text_content += base64.urlsafe_b64decode(data).decode('utf-8')
                        except:
                            pass
        elif 'body' in payload and payload['body'].get('data'):
            try:
                text_content = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            except:
                text_content = msg.get('snippet', '')
        
        return text_content[:500]
    return ""

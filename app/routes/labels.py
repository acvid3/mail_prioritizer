import requests
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from .. import config
from ..services.gmail_utils import verify_google_token

router = APIRouter()


class CreateLabelRequest(BaseModel):
    name: str


class MoveEmailRequest(BaseModel):
    email_id: str
    label_name: str


def resolve_token(authorization, token):
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ")[1]
    if token:
        return token
    raise HTTPException(status_code=401, detail="Authorization required")


def get_or_create_label(access_token: str, label_name: str) -> str:
    gmail_labels_url = f"{config.GMAIL_API_BASE_URL}/labels"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(gmail_labels_url, headers=headers)
    if response.status_code == 200:
        labels = response.json().get("labels", [])
        for label in labels:
            if label.get("name") == label_name:
                return label["id"]

    create_label_data = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
    }

    response = requests.post(
        gmail_labels_url, headers=headers, json=create_label_data
    )
    if response.status_code == 200:
        return response.json()["id"]
    raise Exception(f"Failed to create label: {response.text}")


@router.get("/labels")
def get_labels(authorization: str = Header(None), token: str = None):
    access_token = resolve_token(authorization, token)

    if not verify_google_token(access_token):
        raise HTTPException(status_code=401, detail="Invalid Google OAuth token")

    gmail_labels_url = f"{config.GMAIL_API_BASE_URL}/labels"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    response = requests.get(gmail_labels_url, headers=headers)
    if response.status_code == 200:
        labels = response.json().get("labels", [])
        return {
            "success": True,
            "count": len(labels),
            "labels": labels,
        }
    return {
        "success": False,
        "error": f"Failed to fetch labels: {response.text}",
    }


@router.post("/labels/create")
def create_label(
    request: CreateLabelRequest,
    authorization: str = Header(None),
    token: str = None,
):
    access_token = resolve_token(authorization, token)

    if not verify_google_token(access_token):
        raise HTTPException(status_code=401, detail="Invalid Google OAuth token")

    label_id = get_or_create_label(access_token, request.name)
    return {
        "success": True,
        "label_id": label_id,
        "label_name": request.name,
    }


@router.post("/emails/move")
def move_email_to_label(
    request: MoveEmailRequest,
    authorization: str = Header(None),
    token: str = None,
):
    access_token = resolve_token(authorization, token)

    if not verify_google_token(access_token):
        raise HTTPException(status_code=401, detail="Invalid Google OAuth token")

    label_id = get_or_create_label(access_token, request.label_name)

    modify_url = (
        f"{config.GMAIL_API_BASE_URL}/messages/{request.email_id}/modify"
    )
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    modify_data = {"addLabelIds": [label_id]}

    response = requests.post(modify_url, headers=headers, json=modify_data)
    if response.status_code == 200:
        return {
            "success": True,
            "message": f"Email moved to label '{request.label_name}'",
            "label_id": label_id,
            "email_id": request.email_id,
        }
    return {
        "success": False,
        "error": f"Failed to move email: {response.text}",
    }

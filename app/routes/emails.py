from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from ..services.gmail_api import GmailAPI

router = APIRouter()

gmail = GmailAPI()


def resolve_token(authorization, token):
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ")[1]
    if token:
        return token
    raise HTTPException(
        status_code=401,
        detail="Authorization header required. Use: Authorization: Bearer YOUR_ACCESS_TOKEN",
    )


@router.get("/emails")
def get_emails(
    request: Request,
    authorization: str = Header(None),
    max_results: int = 10,
    token: str = None,
):
    access_token = resolve_token(authorization, token)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    result = gmail.get_messages_list(headers, max_results=max_results)
    if not result.get("success"):
        return JSONResponse(result, status_code=500)

    return JSONResponse(result)

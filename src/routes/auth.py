from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse

from ..services import GmailOAuth

router = APIRouter()
oauth = GmailOAuth()

@router.get("/login")
def google_login():
    url = oauth.get_auth_url()
    return RedirectResponse(url)

@router.get("/callback")
def google_callback(code: str):
    token_data = oauth.exchange_code_for_token(code)
    return JSONResponse(token_data)

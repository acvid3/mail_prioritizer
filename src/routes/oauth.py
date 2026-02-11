import os
import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from ..services.gmail_oauth import GmailOAuth

router = APIRouter()
oauth = GmailOAuth()

@router.get("/login")
def google_login():
    url = oauth.get_auth_url()
    return RedirectResponse(url)

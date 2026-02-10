import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GmailOAuth:
    def __init__(self):
        self.CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
        self.REDIRECT_URI = "https://echo9.online/rest/oauth2-credential/callback"
        
        self.AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
        self.TOKEN_URL = "https://oauth2.googleapis.com/token"
        
        self.SCOPES = [
            "openid",
            "email", 
            "profile",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send"
        ]
    
    def get_auth_url(self) -> str:
        """Get authorization URL for OAuth flow"""
        params = {
            "client_id": self.CLIENT_ID,
            "redirect_uri": self.REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(self.SCOPES),
            "access_type": "offline",
            "prompt": "consent"
        }
        
        return requests.Request("GET", self.AUTH_URL, params=params).prepare().url
    
    def exchange_code_for_token(self, code: str) -> dict:
        """Exchange authorization code for access token"""
        data = {
            "code": code,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "redirect_uri": self.REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        response = requests.post(self.TOKEN_URL, data=data)
        return response.json()

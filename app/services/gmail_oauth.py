import requests

from .. import config


class GmailOAuth:
    def __init__(self):
        self.CLIENT_ID = config.GMAIL_CLIENT_ID
        self.CLIENT_SECRET = config.GMAIL_CLIENT_SECRET
        self.REDIRECT_URI = config.OAUTH_REDIRECT_URI

        self.AUTH_URL = config.GOOGLE_AUTH_URL
        self.TOKEN_URL = config.GOOGLE_TOKEN_URL

        self.SCOPES = config.GMAIL_SCOPES

    def get_auth_url(self) -> str:
        params = {
            "client_id": self.CLIENT_ID,
            "redirect_uri": self.REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(self.SCOPES),
            "access_type": "offline",
            "prompt": "consent",
        }

        url = requests.Request("GET", self.AUTH_URL, params=params).prepare().url
        return url

    def exchange_code_for_token(self, code: str) -> dict:
        data = {
            "code": code,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "redirect_uri": self.REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.TOKEN_URL, data=data)
        return response.json()

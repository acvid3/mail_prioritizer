import os

from dotenv import load_dotenv

load_dotenv()


def get(name, default=""):
    return os.getenv(name, default).strip()


GOOGLE_AUTH_URL = get("GOOGLE_AUTH_URL")
GOOGLE_TOKEN_URL = get("GOOGLE_TOKEN_URL")
GOOGLE_USERINFO_URL = get("GOOGLE_USERINFO_URL")

GMAIL_API_BASE_URL = get("GMAIL_API_BASE_URL")

GMAIL_CLIENT_ID = get("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = get("GMAIL_CLIENT_SECRET")
OAUTH_REDIRECT_URI = get("OAUTH_REDIRECT_URI")

GMAIL_SCOPES = get("GMAIL_SCOPES").split()

OPENAI_API_KEY = get("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = get("OPENAI_ASSISTANT_ID")

PORT = int(get("PORT", "8082"))

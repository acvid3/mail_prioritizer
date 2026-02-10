import os
import requests
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
REDIRECT_URI = "https://echo9.online/rest/oauth2-credential/callback"

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_API_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"

SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

class EmailPayload(BaseModel):
    id: str
    threadId: str
    subject: str
    from_: str
    date: str
    snippet: str
    content: str

    class Config:
        fields = {
            "from_": "from"
        }

class ClassificationResult(BaseModel):
    id: str
    threadId: str
    importance: str
    label: str
    reason: str

def get_message_content(message_id: str, headers: dict):
    """Get full email content"""
    response = requests.get(f"{GMAIL_API_URL}/{message_id}", headers=headers, params={"format": "full"})
    if response.status_code == 200:
        msg = response.json()
        payload = msg.get('payload', {})
        
        # Extract text from email
        text_content = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        import base64
                        try:
                            text_content += base64.urlsafe_b64decode(data).decode('utf-8')
                        except:
                            pass
        elif 'body' in payload and payload['body'].get('data'):
            import base64
            try:
                text_content = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            except:
                text_content = payload.get('snippet', '')
        
        return text_content[:500]  # Limit to 500 characters for display
    return ""

@app.get("/")
def root():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Gmail OAuth API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .email { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
        .subject { font-weight: bold; color: #333; }
        .from { color: #666; font-size: 0.9em; }
        .date { color: #999; font-size: 0.8em; }
        .snippet { margin-top: 10px; color: #555; line-height: 1.4; }
        .content { margin-top: 10px; padding: 10px; background: #f9f9f9; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>Gmail OAuth API</h1>
    <a href="/rest/oauth2-credential/login">Login with Google</a>
    <br><br>
    <h3>Get Emails:</h3>
    <p>Use Authorization header: <code>Authorization: Bearer YOUR_ACCESS_TOKEN</code></p>
    <p>Example: <code>curl -H "Authorization: Bearer ya29..." https://echo9.online/emails</code></p>
    <br><br>
    <h3>Test with token:</h3>
    <p><a href="/emails?token=ya29.a0AUMWg_KZdifKr3TZPUV5KghdY7WTZsd2ocpZYXmFfBNkuub33Ey0RUz6s9zLv5vcUAbvc4TLVIeZ2WdmNIGfHGBo0m_rGaT5ihJhB_h2cFADTGB-nuz4zeDVaplSehZZdxZ3VwJG6qNWVU_gXHZG5OQi9ur0m6WB2H_XhvTaxntMqigEbjbbo2zMyecIsolUn5akYN0aCgYKARUSARMSFQHGX2Mi7E8vQASqqVcqwp0x7wTIpw0206">Click to test with token</a></p>
</body>
</html>"""
    return HTMLResponse(content=html_content, media_type="text/html")

@app.get("/rest/oauth2-credential/login")
def google_login():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    
    url = requests.Request("GET", AUTH_URL, params=params).prepare().url
    return RedirectResponse(url)

@app.get("/rest/oauth2-credential/callback")
def google_callback(code: str):
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    r = requests.post(TOKEN_URL, data=data)
    return JSONResponse(r.json())

@app.get("/emails")
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
                    full_content = get_message_content(msg['id'], headers)
                    
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

@app.get("/docs")
def docs():
    return HTMLResponse(content="<h1>Gmail OAuth API</h1><p>Use /rest/oauth2-credential/login to start OAuth flow</p>", media_type="text/html")

@app.post("/classify", response_model=ClassificationResult)
def classify_email(email: EmailPayload):
    """
    OpenAI Assistant will be called here later
    Currently - stub for testing
    """
    
    # TEMP logic
    text = f"{email.subject} {email.snippet}".lower()
    
    if "invoice" in text or "payment" in text or "overdue" in text:
        return ClassificationResult(
            id=email.id,
            threadId=email.threadId,
            importance="high",
            label="AI_URGENT",
            reason="Payment related email"
        )
    
    return ClassificationResult(
        id=email.id,
        threadId=email.threadId,
        importance="medium",
        label="AI_IMPORTANT",
        reason="Service related email"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)

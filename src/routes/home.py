from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/")
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
    <p>API is running. Use the following endpoints:</p>
    <ul>
        <li><strong>OAuth Login:</strong> <code>GET /rest/oauth2-credential/login</code></li>
        <li><strong>OAuth Callback:</strong> <code>GET /rest/oauth2-credential/callback</code></li>
        <li><strong>Get Emails:</strong> <code>GET /emails</code></li>
        <li><strong>Classify Email:</strong> <code>POST /classify</code></li>
    </ul>
    <h3>API Documentation:</h3>
    <p>Use <code>Authorization: Bearer YOUR_ACCESS_TOKEN</code> header for protected endpoints</p>
</body>
</html>"""
    return HTMLResponse(content=html_content, media_type="text/html")

@router.get("/docs")
def docs():
    return HTMLResponse(content="<h1>Gmail OAuth API</h1><p>Use /rest/oauth2-credential/login to start OAuth flow</p>", media_type="text/html")

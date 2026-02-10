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

@router.get("/docs")
def docs():
    return HTMLResponse(content="<h1>Gmail OAuth API</h1><p>Use /rest/oauth2-credential/login to start OAuth flow</p>", media_type="text/html")

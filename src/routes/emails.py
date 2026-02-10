from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse

from ..services import GmailAPI

router = APIRouter()
gmail = GmailAPI()

@router.get("/emails")
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
        result = gmail.get_messages_list(headers, max_results)
        
        if result["success"]:
            return JSONResponse(result)
        else:
            return JSONResponse(result, status_code=400)
            
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

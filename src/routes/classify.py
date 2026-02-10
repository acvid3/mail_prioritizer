import os
import openai
import requests
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from ..interfaces.classify import IEmailPayload, IClassificationResult, ISendEmailRequest

router = APIRouter()

class EmailPayload(BaseModel, IEmailPayload):
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

class ClassificationResult(BaseModel, IClassificationResult):
    id: str
    threadId: str
    importance: str
    label: str
    reason: str

class SendEmailRequest(BaseModel, ISendEmailRequest):
    to: str
    subject: str
    content: str
    thread_id: str = None

def verify_google_token(access_token: str) -> bool:
    """Verify Google OAuth token"""
    try:
        # Get user info from Google API
        response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return response.status_code == 200
    except:
        return False
    to: str
    subject: str
    content: str
    thread_id: str = None

@router.post("/classify", response_model=ClassificationResult)
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

@router.post("/send")
def send_email_to_assistant(request: SendEmailRequest, authorization: str = Header(None), token: str = None):
    """
    Send email to OpenAI Assistant (requires Google OAuth token verification)
    """
    # Verify Google token
    access_token = None
    if authorization and authorization.startswith("Bearer "):
        access_token = authorization.split(" ")[1]
    elif token:
        access_token = token
    else:
        raise HTTPException(status_code=401, detail="Authorization required. Use: Authorization: Bearer YOUR_ACCESS_TOKEN or ?token=YOUR_ACCESS_TOKEN")
    
    if not verify_google_token(access_token):
        raise HTTPException(status_code=401, detail="Invalid Google OAuth token")
    
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Create thread or use existing
        if request.thread_id:
            thread = client.beta.threads.retrieve(request.thread_id)
        else:
            thread = client.beta.threads.create()
        
        # Add message to thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Email from: {request.to}\nSubject: {request.subject}\n\n{request.content}"
        )
        
        # Run assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=os.getenv("OPENAI_ASSISTANT_ID")
        )
        
        return {
            "success": True,
            "message": "Email sent to assistant",
            "thread_id": thread.id,
            "message_id": message.id,
            "run_id": run.id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

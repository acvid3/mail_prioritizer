import os
import openai
from fastapi import APIRouter
from pydantic import BaseModel
from ..interfaces.emails import IEmailData

router = APIRouter()

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

class SendEmailRequest(BaseModel):
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
def send_email_to_assistant(request: SendEmailRequest):
    """
    Send email to OpenAI Assistant
    """
    import openai
    
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

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

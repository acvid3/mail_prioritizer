import os
import openai
import requests
from fastapi import APIRouter, HTTPException, Header
from ..interfaces.classify import IEmailPayload, IClassificationResult, ISendEmailRequest

router = APIRouter()

def verify_google_token(access_token: str) -> bool:
    try:
        response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return response.status_code == 200
    except:
        return False

@router.post("/classify", response_model=IClassificationResult)
def classify_email(email: IEmailPayload, authorization: str = Header(None), token: str = None):
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
        
        thread = client.beta.threads.create()
        
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Classify this email:\n\nFrom: {email.from_email}\nSubject: {email.subject}\nDate: {email.date}\nSnippet: {email.snippet}\nContent: {email.content}"
        )
        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=os.getenv("OPENAI_ASSISTANT_ID")
        )
        
        import time
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                raise Exception("Assistant run failed")
            time.sleep(1)
        
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        for msg in messages.data:
            if msg.role == "assistant":
                for content in msg.content:
                    if content.type == "text":
                        import json
                        try:
                            result = json.loads(content.text)
                            return IClassificationResult(
                                id=email.id,
                                threadId=email.threadId,
                                importance=result.get("importance", "medium"),
                                label=result.get("label", "AI_IMPORTANT"),
                                reason=result.get("reason", "AI classified email")
                            )
                        except:
                            pass
        
        return IClassificationResult(
            id=email.id,
            threadId=email.threadId,
            importance="medium",
            label="AI_IMPORTANT",
            reason="AI classification completed"
        )
        
    except Exception as e:
        text = f"{email.subject} {email.snippet}".lower()
        
        if "invoice" in text or "payment" in text or "overdue" in text:
            return IClassificationResult(
                id=email.id,
                threadId=email.threadId,
                importance="high",
                label="AI_URGENT",
                reason="Payment related email (fallback)"
            )
        
        return IClassificationResult(
            id=email.id,
            threadId=email.threadId,
            importance="medium",
            label="AI_IMPORTANT",
            reason="Service related email (fallback)"
        )

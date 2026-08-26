import json
import time

import openai
from fastapi import APIRouter, Header, HTTPException

from .. import config
from ..interfaces.classify import IClassificationResult, IEmailPayload
from ..services.gmail_utils import verify_google_token

router = APIRouter()


def resolve_token(authorization, token):
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ")[1]
    if token:
        return token
    raise HTTPException(
        status_code=401,
        detail="Authorization required. Use: Authorization: Bearer YOUR_ACCESS_TOKEN or ?token=YOUR_ACCESS_TOKEN",
    )


@router.post("/classify", response_model=IClassificationResult)
def classify_email(
    email: IEmailPayload, authorization: str = Header(None), token: str = None
):
    access_token = resolve_token(authorization, token)

    if not verify_google_token(access_token):
        raise HTTPException(status_code=401, detail="Invalid Google OAuth token")

    try:
        client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=(
                "Classify this email:\n\n"
                f"From: {email.from_email}\n"
                f"Subject: {email.subject}\n"
                f"Date: {email.date}\n"
                f"Snippet: {email.snippet}\n"
                f"Content: {email.content}"
            ),
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=config.OPENAI_ASSISTANT_ID,
        )

        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                raise Exception("Assistant run failed")
            time.sleep(1)

        messages = client.beta.threads.messages.list(thread_id=thread.id)

        for msg in messages.data:
            if msg.role == "assistant":
                for content in msg.content:
                    if content.type == "text":
                        try:
                            result = json.loads(content.text)
                            return IClassificationResult(
                                id=email.id,
                                threadId=email.threadId,
                                importance=result.get("importance", "medium"),
                                label=result.get("label", "AI_IMPORTANT"),
                                reason=result.get(
                                    "reason", "AI classified email"
                                ),
                            )
                        except (json.JSONDecodeError, ValueError):
                            pass

        return IClassificationResult(
            id=email.id,
            threadId=email.threadId,
            importance="medium",
            label="AI_IMPORTANT",
            reason="AI classification completed",
        )

    except Exception as e:
        text = f"{email.subject} {email.snippet}".lower()

        if "invoice" in text or "payment" in text or "overdue" in text:
            return IClassificationResult(
                id=email.id,
                threadId=email.threadId,
                importance="high",
                label="AI_URGENT",
                reason="Payment related email (fallback)",
            )

        return IClassificationResult(
            id=email.id,
            threadId=email.threadId,
            importance="medium",
            label="AI_IMPORTANT",
            reason="Service related email (fallback)",
        )

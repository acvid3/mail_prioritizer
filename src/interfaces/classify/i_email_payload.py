from pydantic import BaseModel

class IEmailPayload(BaseModel):
    id: str
    threadId: str
    subject: str
    from_email: str
    date: str
    snippet: str
    content: str

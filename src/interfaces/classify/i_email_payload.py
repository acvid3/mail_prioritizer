from pydantic import BaseModel, Field

class IEmailPayload(BaseModel):
    id: str
    threadId: str
    subject: str
    from_email: str = Field(alias="from")
    date: str
    snippet: str
    content: str

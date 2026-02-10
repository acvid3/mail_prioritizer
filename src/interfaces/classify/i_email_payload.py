from pydantic import BaseModel

class IEmailPayload(BaseModel):
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

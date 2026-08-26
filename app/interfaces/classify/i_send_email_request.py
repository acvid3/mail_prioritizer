from pydantic import BaseModel

class ISendEmailRequest(BaseModel):
    to: str
    subject: str
    content: str
    thread_id: str = None

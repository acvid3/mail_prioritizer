from typing import Protocol

class ISendEmailRequest(Protocol):
    to: str
    subject: str
    content: str
    thread_id: str = None

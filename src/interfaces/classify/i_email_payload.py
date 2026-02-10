from typing import Protocol

class IEmailPayload(Protocol):
    id: str
    threadId: str
    subject: str
    from_: str
    date: str
    snippet: str
    content: str

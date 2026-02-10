from typing import Protocol

class IClassificationResult(Protocol):
    id: str
    threadId: str
    importance: str
    label: str
    reason: str

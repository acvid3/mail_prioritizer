from pydantic import BaseModel

class IClassificationResult(BaseModel):
    id: str
    threadId: str
    importance: str
    label: str
    reason: str

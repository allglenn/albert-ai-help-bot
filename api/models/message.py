from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    content: str
    emitter: str
    created_at: datetime
    sources: Optional[str] = None

    class Config:
        from_attributes = True 
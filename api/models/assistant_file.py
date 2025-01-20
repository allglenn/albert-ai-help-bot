from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AssistantFileBase(BaseModel):
    filename: str
    file_type: str
    file_size: int
    file_path: str

class AssistantFileCreate(AssistantFileBase):
    help_assistant_id: int

class AssistantFile(AssistantFileBase):
    id: int
    help_assistant_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True 
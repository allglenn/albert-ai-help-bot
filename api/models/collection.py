from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CollectionBase(BaseModel):
    albert_id: str

class CollectionCreate(CollectionBase):
    pass

class Collection(CollectionBase):
    id: int
    created_at: datetime
    help_assistant_id: Optional[int] = None

    class Config:
        from_attributes = True 
from pydantic import BaseModel, validator
from typing import List, Optional
from enum import Enum
import random
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import JSON
from db.database import Base
from datetime import datetime

class Authorization(str, Enum):
    CAN_SEND_EMAIL = "CAN_SEND_EMAIL"
    CAN_READ_DOCUMENTS = "CAN_READ_DOCUMENTS"


class HelpAssistantBase(BaseModel):
    name: str
    url: str
    mission: str
    description: Optional[str] = None
    authorizations: List[Authorization] = []
    operator_name: str
    operator_pic: Optional[str] = None  # Made optional as we'll generate it if not provided

    @validator('operator_pic', pre=True, always=True)
    def set_operator_pic(cls, v, values):
        if v is None:
            # Randomly choose between men and women
            gender = random.choice(['men', 'women'])
            # Random number between 0 and 99
            number = random.randint(0, 99)
            return f"https://randomuser.me/api/portraits/{gender}/{number}.jpg"
        return v

    @validator('authorizations', pre=True)
    def split_authorizations(cls, v):
        if isinstance(v, str):
            # Handle empty string
            if not v:
                return []
            # Split string and convert to Authorization enum
            return [Authorization(auth.strip()) for auth in v.split(',')]
        return v

class HelpAssistantCreate(HelpAssistantBase):
    pass

class HelpAssistantUpdate(HelpAssistantBase):
    pass

class HelpAssistantResponse(HelpAssistantBase):
    id: int
    user_id: int
    message: Optional[str] = None
    response: Optional[str] = None

    class Config:
        from_attributes = True

class HelpAssistant(Base):
    __tablename__ = "help_assistant"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    mission: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    authorizations: Mapped[List[str]] = mapped_column(JSON, default=list)
    operator_name: Mapped[str] = mapped_column(String)
    operator_pic: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    message: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    response: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Relationships
    collection = relationship("Collection", back_populates="help_assistant", uselist=False)
    chats = relationship("Chat", back_populates="assistant")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True 
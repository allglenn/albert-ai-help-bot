from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from db.database import Base
from pydantic import BaseModel
from typing import Optional

# SQLAlchemy Model
class Collection(Base):
    __tablename__ = "collection"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    albert_id: Mapped[str] = mapped_column(String)
    help_assistant_id: Mapped[int] = mapped_column(Integer, ForeignKey("help_assistant.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    help_assistant = relationship("HelpAssistant", back_populates="collection")

# Pydantic Models for API
class CollectionBase(BaseModel):
    albert_id: str

    class Config:
        from_attributes = True

class CollectionCreate(CollectionBase):
    pass

class CollectionResponse(CollectionBase):
    id: int
    help_assistant_id: int
    created_at: datetime

    class Config:
        from_attributes = True 
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

# SQLAlchemy Model
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    chats = relationship("Chat", back_populates="user")

# Pydantic Models for API
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class UserInDB(UserBase):
    id: int
    is_active: bool = True
    hashed_password: str

    class Config:
        from_attributes = True 
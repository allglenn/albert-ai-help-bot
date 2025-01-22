from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

# Remove enum and use string constants instead
class EmitterType:
    USER = "USER"
    ASSISTANT = "ASSISTANT"

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    assistant_id = Column(Integer, ForeignKey("help_assistant.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))  # Changed from "user" to "users"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assistant = relationship("HelpAssistant", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    user = relationship("User", back_populates="chats")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"))
    content = Column(String, nullable=False)
    emitter = Column(String, nullable=False)  # Using string instead of enum
    created_at = Column(DateTime, default=datetime.utcnow)
    sources = Column(String, nullable=True)  # JSON string of source documents

    # Relationship
    chat = relationship("Chat", back_populates="messages") 
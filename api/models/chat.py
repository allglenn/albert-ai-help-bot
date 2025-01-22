from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from db.database import Base
from models.user import User
from models.help_assistant import HelpAssistant

class EmitterType(str, enum.Enum):
    ASSISTANT = "ASSISTANT"
    CLIENT = "CLIENT"

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    assistant_id = Column(Integer, ForeignKey(HelpAssistant.__table__.name + ".id"))
    user_id = Column(Integer, ForeignKey(User.__table__.name + ".id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assistant = relationship("HelpAssistant", back_populates="chats")
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    emitter = Column(Enum(EmitterType))
    content = Column(String)
    sources = Column(String, nullable=True)  # Store as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    chat = relationship("Chat", back_populates="messages") 
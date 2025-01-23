from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)

class Authorization(enum.Enum):
    CAN_SEND_EMAIL = "CAN_SEND_EMAIL"
    CAN_READ_DOCUMENTS = "CAN_READ_DOCUMENTS"


class HelpAssistant(Base):
    __tablename__ = "help_assistant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    mission = Column(String, nullable=False)
    description = Column(String)
    authorizations = Column(JSON, default=list)
    operator_name = Column(String, nullable=False)
    operator_pic = Column(String, nullable=False)  # URL to the operator's picture
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    response = Column(String)
    tone = Column(String, nullable=False, default="PROFESSIONAL") 

    # Update relationship definition
    collection = relationship("Collection", back_populates="help_assistant", uselist=False)

    @property
    def authorization_list(self):
        """Convert stored string to list of Authorization enums"""
        if not self.authorizations:
            return []
        return [Authorization(auth) for auth in self.authorizations]

    @authorization_list.setter
    def authorization_list(self, auths):
        """Convert list of Authorization enums to stored string"""
        self.authorizations = [auth.value for auth in auths]

class AssistantFile(Base):
    __tablename__ = "assistant_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    help_assistant_id = Column(Integer, ForeignKey("help_assistant.id", ondelete="CASCADE"))
    assistant_collection_id = Column(String, nullable=True)
    albert_ai_id = Column(String, nullable=True)

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    albert_id = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    help_assistant_id = Column(Integer, ForeignKey("help_assistant.id", ondelete="SET NULL"), nullable=True)
    
    # Add the back reference
    help_assistant = relationship("HelpAssistant", back_populates="collection")

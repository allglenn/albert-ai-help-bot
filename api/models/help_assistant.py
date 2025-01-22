from pydantic import BaseModel, validator
from typing import List, Optional, Dict
from enum import Enum
import random
import json
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import JSON
from db.database import Base
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Authorization(str, Enum):
    CAN_SEND_EMAIL = "CAN_SEND_EMAIL"
    CAN_READ_DOCUMENTS = "CAN_READ_DOCUMENTS"

class ToneType(str, Enum):
    PROFESSIONAL = "PROFESSIONAL"  # Formal and business-like
    FRIENDLY = "FRIENDLY"         # Warm and approachable
    CASUAL = "CASUAL"            # Relaxed and informal
    EMPATHETIC = "EMPATHETIC"    # Understanding and compassionate
    TECHNICAL = "TECHNICAL"      # Precise and technical
    EDUCATIONAL = "EDUCATIONAL"  # Teaching-oriented
    HUMOROUS = "HUMOROUS"       # Light and funny

    @classmethod
    def get_description(cls, tone: str, language: str = 'fr') -> str:
        """Get the description of a tone in the specified language"""
        descriptions = {
            'fr': {
                cls.PROFESSIONAL: "Formel et professionnel",
                cls.FRIENDLY: "Chaleureux et accessible",
                cls.CASUAL: "Décontracté et informel",
                cls.EMPATHETIC: "Compréhensif et compatissant",
                cls.TECHNICAL: "Précis et technique",
                cls.EDUCATIONAL: "Pédagogique et instructif",
                cls.HUMOROUS: "Léger et humoristique"
            },
            'en': {
                cls.PROFESSIONAL: "Formal and business-like",
                cls.FRIENDLY: "Warm and approachable",
                cls.CASUAL: "Relaxed and informal",
                cls.EMPATHETIC: "Understanding and compassionate",
                cls.TECHNICAL: "Precise and technical",
                cls.EDUCATIONAL: "Teaching-oriented",
                cls.HUMOROUS: "Light and funny"
            }
        }
        return descriptions.get(language, descriptions['en']).get(tone, "Unknown tone")

    @classmethod
    def get_all_descriptions(cls, language: str = 'fr') -> Dict[str, str]:
        """Get all tone descriptions in the specified language"""
        return {tone: cls.get_description(tone, language) for tone in cls}

class HelpAssistantBase(BaseModel):
    name: str
    url: str
    mission: str
    description: Optional[str] = None
    authorizations: List[Authorization] = []
    operator_name: str
    operator_pic: Optional[str] = None
    tone: ToneType = ToneType.PROFESSIONAL

    @validator('operator_pic', pre=True, always=True)
    def set_operator_pic(cls, v, values):
        if v is None:
            gender = random.choice(['men', 'women'])
            number = random.randint(0, 99)
            return f"https://randomuser.me/api/portraits/{gender}/{number}.jpg"
        return v

    @validator('authorizations', pre=True)
    def parse_authorizations(cls, v):
        """Convert various authorization formats to List[Authorization]"""
        logger.info(f"Parsing authorizations input: {v} (type: {type(v)})")
        
        if isinstance(v, str):
            logger.info("Input is string, attempting to parse")
            try:
                # Try to parse JSON string
                v = json.loads(v)
                logger.info(f"Successfully parsed JSON string to: {v}")
            except json.JSONDecodeError as e:
                logger.info(f"Not a JSON string, splitting by comma: {e}")
                # If not JSON, split comma-separated string
                v = [x.strip() for x in v.split(',') if x.strip()]
                logger.info(f"Split result: {v}")
        
        if isinstance(v, list):
            logger.info(f"Converting list items to Authorization enums: {v}")
            try:
                result = [
                    auth if isinstance(auth, Authorization)
                    else Authorization(auth)
                    for auth in v
                    if auth
                ]
                logger.info(f"Successfully converted to Authorization enums: {result}")
                return result
            except ValueError as e:
                logger.error(f"Error converting to Authorization enum: {e}")
                raise
        
        logger.info(f"Returning value as-is: {v}")
        return v

    @staticmethod
    def get_available_tones():
        """Get all available tones with their descriptions"""
        return {
            ToneType.PROFESSIONAL: "Formal and business-like",
            ToneType.FRIENDLY: "Warm and approachable",
            ToneType.CASUAL: "Relaxed and informal",
            ToneType.EMPATHETIC: "Understanding and compassionate",
            ToneType.TECHNICAL: "Precise and technical",
            ToneType.EDUCATIONAL: "Teaching-oriented",
            ToneType.HUMOROUS: "Light and funny"
        }

class HelpAssistantCreate(HelpAssistantBase):
    pass

class HelpAssistantUpdate(HelpAssistantBase):
    pass

class HelpAssistantResponse(HelpAssistantBase):
    id: int
    user_id: int
    message: Optional[str] = None
    response: Optional[str] = None
    tone: ToneType = ToneType.PROFESSIONAL

    class Config:
        from_attributes = True
        json_encoders = {
            Authorization: lambda v: v.value  # Ensure Authorization enums are serialized as strings
        }

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
    tone: Mapped[str] = mapped_column(String, default=ToneType.PROFESSIONAL)  # Make sure this exists
    
    # Relationships
    collection = relationship("Collection", back_populates="help_assistant", uselist=False)
    chats = relationship("Chat", back_populates="assistant")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True 
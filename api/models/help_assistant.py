from pydantic import BaseModel, validator
from typing import List, Optional
from enum import Enum
import random

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

class HelpAssistant(HelpAssistantBase):
    id: int
    user_id: int
    message: Optional[str] = None
    response: Optional[str] = None

    class Config:
        orm_mode = True 
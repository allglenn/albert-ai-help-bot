from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

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
    authorizations = Column(String)  # Stored as comma-separated values
    operator_name = Column(String, nullable=False)
    operator_pic = Column(String, nullable=False)  # URL to the operator's picture
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    response = Column(String)

    @property
    def authorization_list(self):
        """Convert stored string to list of Authorization enums"""
        if not self.authorizations:
            return []
        return [Authorization(auth) for auth in self.authorizations.split(',')]

    @authorization_list.setter
    def authorization_list(self, auths):
        """Convert list of Authorization enums to stored string"""
        if not auths:
            self.authorizations = ""
        else:
            self.authorizations = ','.join(auth.value for auth in auths)

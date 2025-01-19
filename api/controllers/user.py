from models.user import User, UserCreate
from services.external_api import AlbertAIService

class UserController:
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        # Business logic for user creation
        # Example: validate data, check AI service, create user
        ai_service = AlbertAIService()
        # Add your business logic here
        return User(id=1, **user_data.dict())

    @staticmethod
    async def get_user(user_id: int) -> User:
        # Business logic for retrieving user
        return User(id=user_id, email="test@example.com", full_name="Test User") 
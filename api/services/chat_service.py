from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.chat import Chat, Message, EmitterType
from models.user import User
from models.help_assistant import HelpAssistant
from typing import Optional, List
import json

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_chat(self, assistant_id: int, user_id: int) -> Chat:
        """Create a new chat session"""
        try:
            # First verify both user and assistant exist
            user_query = select(User).where(User.id == user_id)
            assistant_query = select(HelpAssistant).where(HelpAssistant.id == assistant_id)
            
            # Execute both queries
            user_result = await self.db.execute(user_query)
            assistant_result = await self.db.execute(assistant_query)
            
            user = user_result.scalar_one_or_none()
            assistant = assistant_result.scalar_one_or_none()

            if not user:
                raise ValueError(f"User with ID {user_id} does not exist in database")
            if not assistant:
                raise ValueError(f"Assistant with ID {assistant_id} does not exist in database")

            # Create chat only if both exist
            chat = Chat(
                assistant_id=assistant_id,
                user_id=user_id
            )
            self.db.add(chat)
            await self.db.commit()
            await self.db.refresh(chat)
            return chat
            
        except Exception as e:
            await self.db.rollback()
            print(f"Error details - User ID: {user_id}, Assistant ID: {assistant_id}")  # Debug print
            raise ValueError(f"Failed to create chat: {str(e)}")

    async def add_message(self, chat_id: int, content: str, emitter: EmitterType, sources: Optional[List[str]] = None) -> Message:
        """Add a message to the chat"""
        message = Message(
            chat_id=chat_id,
            content=content,
            emitter=emitter,
            sources=json.dumps(sources) if sources else None
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_chat_messages(self, chat_id: int) -> List[Message]:
        """Get all messages for a chat"""
        query = select(Message).where(Message.chat_id == chat_id).order_by(Message.created_at)
        result = await self.db.execute(query)
        return result.scalars().all() 
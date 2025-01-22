from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.chat import Chat, Message, EmitterType
from typing import Optional, List
import json

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_chat(self, assistant_id: int, user_id: int) -> Chat:
        """Create a new chat session"""
        chat = Chat(
            assistant_id=assistant_id,
            user_id=user_id
        )
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

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
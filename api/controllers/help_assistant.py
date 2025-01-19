from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import HelpAssistant as HelpAssistantDB
from models.help_assistant import HelpAssistantCreate, HelpAssistantUpdate
from fastapi import HTTPException

class HelpAssistantController:
    @staticmethod
    async def create_help_assistant(help_assistant: HelpAssistantCreate, user_id: int, db: AsyncSession):
        db_help_assistant = HelpAssistantDB(
            **help_assistant.dict(),
            user_id=user_id
        )
        db.add(db_help_assistant)
        await db.commit()
        await db.refresh(db_help_assistant)
        return db_help_assistant

    @staticmethod
    async def get_help_assistant(help_assistant_id: int, db: AsyncSession):
        result = await db.execute(
            select(HelpAssistantDB).filter(HelpAssistantDB.id == help_assistant_id)
        )
        help_assistant = result.scalar_one_or_none()
        if not help_assistant:
            raise HTTPException(status_code=404, detail="Help Assistant not found")
        return help_assistant

    @staticmethod
    async def get_user_help_assistants(user_id: int, db: AsyncSession):
        result = await db.execute(
            select(HelpAssistantDB).filter(HelpAssistantDB.user_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def update_help_assistant(
        help_assistant_id: int,
        help_assistant_update: HelpAssistantUpdate,
        db: AsyncSession
    ):
        result = await db.execute(
            select(HelpAssistantDB).filter(HelpAssistantDB.id == help_assistant_id)
        )
        db_help_assistant = result.scalar_one_or_none()
        if not db_help_assistant:
            raise HTTPException(status_code=404, detail="Help Assistant not found")

        for key, value in help_assistant_update.dict(exclude_unset=True).items():
            setattr(db_help_assistant, key, value)

        await db.commit()
        await db.refresh(db_help_assistant)
        return db_help_assistant 
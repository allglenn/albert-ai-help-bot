from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import HelpAssistant as HelpAssistantDB
from models.help_assistant import HelpAssistantCreate, HelpAssistantUpdate
from fastapi import HTTPException

class HelpAssistantController:
    @staticmethod
    async def create_help_assistant(help_assistant: HelpAssistantCreate, user_id: int, db: AsyncSession):
        # Convert authorizations list to comma-separated string
        auth_string = ','.join([auth.value for auth in help_assistant.authorizations]) if help_assistant.authorizations else ''
        
        # Create dict of values and update authorizations
        help_assistant_dict = help_assistant.dict()
        help_assistant_dict['authorizations'] = auth_string

        db_help_assistant = HelpAssistantDB(
            **help_assistant_dict,
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

        # Convert authorizations list to comma-separated string
        update_data = help_assistant_update.dict(exclude_unset=True)
        if 'authorizations' in update_data:
            update_data['authorizations'] = ','.join([auth.value for auth in update_data['authorizations']]) if update_data['authorizations'] else ''

        for key, value in update_data.items():
            setattr(db_help_assistant, key, value)

        await db.commit()
        await db.refresh(db_help_assistant)
        return db_help_assistant

    @staticmethod
    async def delete_help_assistant(help_assistant_id: int, db: AsyncSession):
        result = await db.execute(
            select(HelpAssistantDB).filter(HelpAssistantDB.id == help_assistant_id)
        )
        help_assistant = result.scalar_one_or_none()
        if not help_assistant:
            raise HTTPException(status_code=404, detail="Help Assistant not found")
        
        await db.delete(help_assistant)
        await db.commit()
        return help_assistant 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.models import HelpAssistant as HelpAssistantDB
from models.help_assistant import (
    HelpAssistantCreate, 
    HelpAssistantUpdate,
    Authorization,
    ToneType
)
from fastapi import HTTPException
from utils.exceptions import UserNotFoundException, EmailAlreadyExistsException
import logging

logger = logging.getLogger(__name__)

class HelpAssistantController:
    @staticmethod
    async def create_help_assistant(help_assistant: HelpAssistantCreate, user_id: int, db: AsyncSession):
        # Convert authorizations to list of strings
        auth_list = [auth.value for auth in help_assistant.authorizations] if help_assistant.authorizations else []
        
        # Create dict of values and update authorizations
        help_assistant_dict = help_assistant.dict()
        help_assistant_dict['authorizations'] = auth_list  # Store as JSON array

        db_help_assistant = HelpAssistantDB(
            **help_assistant_dict,
            user_id=user_id
        )
        db.add(db_help_assistant)
        await db.commit()
        await db.refresh(db_help_assistant)
        return db_help_assistant

    @staticmethod
    async def get_help_assistant(help_assistant_id: int, db: AsyncSession) -> HelpAssistantDB:
        """Get a help assistant by ID"""
        query = select(HelpAssistantDB).where(HelpAssistantDB.id == help_assistant_id)
        result = await db.execute(query)
        help_assistant = result.scalar_one_or_none()
        
        if not help_assistant:
            raise HTTPException(status_code=404, detail="Help Assistant not found")
            
        return help_assistant

    @staticmethod
    async def get_user_help_assistants(user_id: int, db: AsyncSession) -> list[HelpAssistantDB]:
        result = await db.execute(
            select(HelpAssistantDB)
            .options(selectinload(HelpAssistantDB.collection))
            .filter(HelpAssistantDB.user_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def update_help_assistant(
        help_assistant_id: int,
        help_assistant_update: HelpAssistantUpdate,
        db: AsyncSession
    ) -> HelpAssistantDB:
        """Update a help assistant"""
        logger.info(f"Updating help assistant {help_assistant_id}")
        logger.info(f"Update data received: {help_assistant_update.dict()}")
        
        query = select(HelpAssistantDB).where(HelpAssistantDB.id == help_assistant_id)
        result = await db.execute(query)
        db_help_assistant = result.scalar_one_or_none()
        
        if not db_help_assistant:
            logger.error(f"Help Assistant {help_assistant_id} not found")
            raise HTTPException(status_code=404, detail="Help Assistant not found")
        
        update_data = help_assistant_update.dict(exclude_unset=True)
        logger.info(f"Update data after dict conversion: {update_data}")
        
        # Handle authorizations conversion
        if 'authorizations' in update_data:
            logger.info(f"Processing authorizations: {update_data['authorizations']}")
            try:
                # Convert Authorization enum list to list of strings
                auth_list = [
                    auth.value if isinstance(auth, Authorization) else auth 
                    for auth in update_data['authorizations']
                ] if update_data['authorizations'] else []
                
                logger.info(f"Converted authorizations to: {auth_list}")
                update_data['authorizations'] = auth_list
            except Exception as e:
                logger.error(f"Error processing authorizations: {e}", exc_info=True)
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid authorization format: {str(e)}"
                )
        
        # Update fields
        try:
            for field, value in update_data.items():
                logger.info(f"Setting field {field} to value: {value}")
                setattr(db_help_assistant, field, value)
            
            await db.commit()
            await db.refresh(db_help_assistant)
            logger.info("Successfully updated help assistant")
            return db_help_assistant
        except Exception as e:
            logger.error(f"Error updating help assistant: {e}", exc_info=True)
            raise

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
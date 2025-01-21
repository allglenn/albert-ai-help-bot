from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Collection
from models.collection import CollectionCreate
from services.external_api import AlbertAIService

class CollectionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.albert_service = AlbertAIService()

    async def get_by_help_assistant(self, help_assistant_id: int) -> Collection:
        """Get or create collection for a help assistant"""
        # Check if collection exists
        result = await self.db.execute(
            select(Collection).filter(Collection.help_assistant_id == help_assistant_id)
        )
        collection = result.scalar_one_or_none()
        
        if not collection:
            # Create new collection in Albert AI
            collection_name = f"assistant_{help_assistant_id}_collection"
            albert_response = await self.albert_service.create_collection(collection_name)
            
            # Create local collection record
            collection = Collection(
                albert_id=albert_response["id"],
                help_assistant_id=help_assistant_id
            )
            self.db.add(collection)
            await self.db.commit()
            await self.db.refresh(collection)
        
        return collection

    async def delete_collection(self, collection_id: int):
        """Delete collection both locally and in Albert AI"""
        result = await self.db.execute(
            select(Collection).filter(Collection.id == collection_id)
        )
        collection = result.scalar_one_or_none()
        
        if collection:
            # Delete from Albert AI
            await self.albert_service.delete_collection(collection.albert_id)
            
            # Delete local record
            await self.db.delete(collection)
            await self.db.commit() 
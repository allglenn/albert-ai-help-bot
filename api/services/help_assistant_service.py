from services.collection_service import CollectionService

class HelpAssistantService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.collection_service = CollectionService(db)

    async def get_collection(self, help_assistant_id: int):
        """Get or create collection for help assistant"""
        return await self.collection_service.get_by_help_assistant(help_assistant_id)

    async def delete_help_assistant(self, help_assistant_id: int):
        """Delete help assistant and its collection"""
        help_assistant = await self.get_help_assistant(help_assistant_id)
        if help_assistant and help_assistant.collection:
            await self.collection_service.delete_collection(help_assistant.collection.id)
        await super().delete_help_assistant(help_assistant_id) 
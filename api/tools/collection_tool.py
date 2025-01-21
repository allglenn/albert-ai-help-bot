from typing import List, Dict, Any
from services.external_api import AlbertAIService

class CollectionTool:
    """Tool for interacting with document collections"""
    
    def __init__(self, albert_service: AlbertAIService):
        self.albert_service = albert_service

    async def search_collection(self, collection_id: str, query: str, k: int = 6) -> List[str]:
        """
        Search a collection for relevant chunks based on a query.
        
        Args:
            collection_id: The ID of the collection to search
            query: The search query
            k: Number of results to return (default: 6)
            
        Returns:
            List of relevant text chunks from the collection
        """
        return await self.albert_service.search_collection(
            collection_id=collection_id,
            query=query,
            k=k
        )

    async def chat_with_context(self, collection_id: str, prompt: str) -> Dict[str, Any]:
        """
        Search collection and use relevant chunks to answer the prompt.
        
        Args:
            collection_id: The ID of the collection to search
            prompt: The user's question
            
        Returns:
            Dict containing the AI response, source documents, and context chunks
        """
        return await self.albert_service.chat_with_context(
            collection_id=collection_id,
            prompt=prompt
        ) 
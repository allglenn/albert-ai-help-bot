import httpx
from config import settings

class AlbertAIService:
    def __init__(self):
        self.base_url = f"{settings.ALBERT_AI_BASE_URL}/v1"
        self.api_key = settings.ALBERT_AI_API_KEY
        self.embeddings_model = settings.ALBERT_AI_EMBEDDINGS_MODEL
        self.llm_model  = settings.ALBERT_AI_LLM_MODEL

    async def query_ai_model(self, prompt: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/query",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"prompt": prompt}
            )
            return response.json()

    async def list_models(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()

    async def create_collection(self, collection_name: str) -> dict:
        """Create a new collection for embeddings"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/collections",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "name": collection_name,
                    "model": self.embeddings_model
                }
            )
            return response.json()

    async def delete_collection(self, collection_id: str) -> dict:
        """Delete a collection by its ID"""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/collections/{collection_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}"
                }
            )
            return response.json()


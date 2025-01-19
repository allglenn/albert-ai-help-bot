import httpx
from config import settings

class AlbertAIService:
    def __init__(self):
        self.base_url = settings.ALBERT_AI_BASE_URL
        self.api_key = settings.ALBERT_AI_API_KEY

    async def query_ai_model(self, prompt: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/query",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"prompt": prompt}
            )
            return response.json() 
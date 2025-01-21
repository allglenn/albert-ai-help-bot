import httpx
import os
from config import settings
from typing import List, Dict, Any
import json

class AlbertAIService:
    def __init__(self):
        self.base_url = f"{settings.ALBERT_AI_BASE_URL}/v1"
        self.api_key = settings.ALBERT_AI_API_KEY
        self.embeddings_model = settings.ALBERT_AI_EMBEDDINGS_MODEL
        self.llm_model = settings.ALBERT_AI_LLM_MODEL

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

    async def upload_file(self, file_path: str, collection_id: str) -> dict:
        """Upload a file to Albert AI and associate it with a collection"""
        async with httpx.AsyncClient() as client:
            try:
                with open(file_path, "rb") as f:
                    request_json = {"collection": collection_id}
                    files = {
                        "file": (
                            os.path.basename(file_path),
                            f,
                            "application/pdf"
                        ),
                        "request": (
                            None,
                            json.dumps(request_json),
                            "application/json"
                        )
                    }

                    response = await client.post(
                        f"{self.base_url}/files",
                        headers={
                            "Authorization": f"Bearer {self.api_key}"
                        },
                        files=files
                    )
                    
                    # Accept both 200 and 201 as success
                    if response.status_code not in (200, 201):
                        raise ValueError(f"Upload failed with status {response.status_code}: {response.text}")

                    # Handle empty response
                    if not response.text:
                        return {"status": "success", "code": response.status_code}
                    return response.json()

            except Exception as e:
                raise

    async def get_documents(self, collection_id: str) -> List[Dict[str, Any]]:
        """Get all documents for a collection"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/documents/{collection_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}"
                }
            )
            data = response.json()
            return data.get("data", [])  # Return just the data array from response

    async def delete_document(self, collection_id: str, document_id: str) -> dict:
        """Delete a document from a collection"""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/documents/{collection_id}/{document_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}"
                }
            )
            return response.json()


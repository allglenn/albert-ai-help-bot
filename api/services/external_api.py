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

    async def search_collection(self, collection_id: str, query: str, k: int = 6) -> List[str]:
        """
        Search a collection for relevant chunks based on a query.
        
        Args:
            collection_id: The ID of the collection to search
            query: The search query
            k: Number of results to return (default: 5)
            
        Returns:
            List of chunk contents from the search results
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/search",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "collections": [collection_id],
                    "prompt": query,
                    "k": k,
                    "method": "semantic"
                }
            )
            
            if response.status_code == 200:
                results = response.json()
                return [result["chunk"]["content"] for result in results.get("data", [])]
            else:
                raise ValueError(f"Search failed with status {response.status_code}: {response.text}")

    async def chat_with_context(self, collection_id: str, prompt: str) -> Dict[str, Any]:
        """
        Search collection for relevant chunks and use them to answer the prompt.
        
        Args:
            collection_id: The ID of the collection to search
            prompt: The user's question
            
        Returns:
            Dict containing the response and source documents
        """
        async with httpx.AsyncClient() as client:
            # Get relevant chunks using existing search method
            search_results = await client.post(
                f"{self.base_url}/search",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "collections": [collection_id],
                    "prompt": prompt,
                    "k": 6,
                    "method": "semantic"
                }
            )
            
            results = search_results.json()
            chunks = "\n\n\n".join([result["chunk"]["content"] for result in results["data"]])
            sources = list({result["chunk"]["metadata"]["document_name"] for result in results["data"]})
            
            # Format prompt with context
            prompt_template = "Réponds à la question suivante en te basant sur les documents ci-dessous : {prompt}\n\nDocuments :\n\n{chunks}"
            context_prompt = prompt_template.format(prompt=prompt, chunks=chunks)
            
            # Get AI response
            query_response = await client.post(
                f"{self.base_url}/query",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": context_prompt,
                    "model": self.llm_model
                }
            )
            
            if query_response.status_code != 200:
                raise ValueError(f"Query failed with status {query_response.status_code}: {query_response.text}")
            
            response_data = query_response.json()
            
            return {
                "response": response_data.get("text", ""),
                "sources": sources,
                "chunks": chunks
            }


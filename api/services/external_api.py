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

    async def search_collection(self, collection_id: str, query: str, k: int = 6) -> List[Dict[str, Any]]:
        """
        Search a collection for relevant chunks based on a query.
        
        Args:
            collection_id: The ID of the collection to search
            query: The search query
            k: Number of results to return (default: 6)
            
        Returns:
            List of dictionaries containing chunk content and metadata
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
                return [
                    {
                        "content": result["chunk"]["content"],
                        "metadata": result["chunk"]["metadata"],
                        "score": result["score"]
                    } 
                    for result in results.get("data", [])
                ]
            else:
                raise ValueError(f"Search failed with status {response.status_code}: {response.text}")

    async def chat_with_context(self, collection_id: str, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
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
            
            chat_history = context.get("chat_history", "")
            messages = []
            # add system {"role": "system", "content": context.get("system", "")}
            messages.append({"role": "system", "content": context.get("system", "")})
            #a add history 
            for message in chat_history:
                messages.append({"role": message['role'] , "content": message['content']})
            prompt_template = "Réponds à la question suivante en te basant sur les documents ci-dessous : {prompt}\n\nDocuments :\n\n{chunks}"
            chunks = "\n\n\n".join([result["chunk"]["content"] for result in search_results.json()["data"]])
            sources = set([result["chunk"]["metadata"]["document_name"] for result in search_results.json()["data"]])
            prompt = prompt_template.format(prompt=prompt, chunks=chunks)
            messages.append({"role": "user", "content": prompt})
            data = {
                "model": self.llm_model,
                "messages": messages,
                "stream": False,
                "n": 1,
                "temperature": 0.7,

            }
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data
            )
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                raise ValueError(f"Request failed with status {response.status_code}")
            else:
                print("request worked")
                print(response.json())
            return response.json()
            
          
        

    async def rephrase_with_tone(self, message: str, tone: str) -> str:
        """
        Rephrase a message according to a specific tone using the AI model.
        
        Args:
            message: The message to rephrase
            tone: The tone to use (e.g., PROFESSIONAL, FRIENDLY, etc.)
            
        Returns:
            The rephrased message
        """
        tone_prompts = {
            "PROFESSIONAL": "Reformule ce message de manière professionnelle et formelle",
            "FRIENDLY": "Reformule ce message de manière chaleureuse et amicale",
            "CASUAL": "Reformule ce message de manière décontractée et informelle",
            "EMPATHETIC": "Reformule ce message avec empathie et compréhension",
            "TECHNICAL": "Reformule ce message de manière technique et précise",
            "EDUCATIONAL": "Reformule ce message de manière pédagogique",
            "HUMOROUS": "Reformule ce message avec humour et légèreté"
        }

        # Add clear instructions for a single response
        system_prompt = """Tu es un assistant qui reformule les messages selon le ton demandé.
        Instructions:
        - Donne une seule reformulation
        - Ne propose pas plusieurs options
        - Ne mets pas de guillemets
        - Réponds directement avec la reformulation
        """

        prompt = f"{tone_prompts.get(tone, tone_prompts['PROFESSIONAL'])} : {message}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.llm_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "n": 1,
                    "temperature": 0.7  # Add some randomness but not too much
                }
            )

            if response.status_code != 200:
                raise ValueError(f"Failed to rephrase message: {response.text}")

            result = response.json()
            # Clean up the response by removing quotes and extra whitespace
            response_text = result["choices"][0]["message"]["content"]
            response_text = response_text.strip('"\'').strip()
            return response_text


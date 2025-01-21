import os
import shutil
from fastapi import UploadFile
from pathlib import Path
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import AssistantFile
from models.assistant_file import AssistantFileCreate
from services.collection_service import CollectionService
from services.external_api import AlbertAIService
import logging

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
ALLOWED_EXTENSIONS = {'.pdf', '.md', '.txt'}

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.collection_service = CollectionService(db)
        self.albert_service = AlbertAIService()
        UPLOAD_DIR.mkdir(exist_ok=True)

    def _is_allowed_file(self, filename: str) -> bool:
        return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

    async def save_file(self, file: UploadFile, help_assistant_id: int) -> AssistantFile:
        """Save file locally and upload to Albert AI if collection exists"""
        if not self._is_allowed_file(file.filename):
            raise ValueError("File type not allowed")

        # Get collection for the assistant
        collection = await self.collection_service.get_by_help_assistant(help_assistant_id)
        
        # Create assistant-specific directory
        assistant_dir = UPLOAD_DIR / str(help_assistant_id)
        assistant_dir.mkdir(exist_ok=True)

        # Save file locally
        file_path = assistant_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            # Create database record
            db_file = AssistantFile(
                filename=file.filename,
                file_type=Path(file.filename).suffix.lower(),
                file_size=os.path.getsize(file_path),
                file_path=str(file_path),
                help_assistant_id=help_assistant_id,
                assistant_collection_id=collection.albert_id if collection else None
            )
            
            self.db.add(db_file)
            await self.db.commit()
            await self.db.refresh(db_file)

            # Upload to Albert AI if collection exists
            if collection:
                try:
                    await self.albert_service.upload_file(
                        file_path=str(file_path),
                        collection_id=collection.albert_id
                    )
                    
                    # Get documents to find the ID of our newly uploaded file
                    documents = await self.albert_service.get_documents(collection.albert_id)
                    
                    # Find the most recently created document with matching filename
                    matching_docs = [
                        doc for doc in documents 
                        if doc["name"] == file.filename
                    ]
                    if matching_docs:
                        newest_doc = max(matching_docs, key=lambda x: x["created_at"])
                        db_file.albert_ai_id = newest_doc["id"]
                        await self.db.commit()

                except Exception as e:
                    raise ValueError(f"Failed to upload file to Albert AI: {str(e)}")

            return db_file

        except Exception as e:
            if file_path.exists():
                file_path.unlink()
            raise e

    async def get_assistant_files(self, help_assistant_id: int) -> List[AssistantFile]:
        result = await self.db.execute(
            select(AssistantFile).filter(AssistantFile.help_assistant_id == help_assistant_id)
        )
        return result.scalars().all()

    async def delete_file(self, file_id: int):
        result = await self.db.execute(
            select(AssistantFile).filter(AssistantFile.id == file_id)
        )
        db_file = result.scalar_one_or_none()
        
        if db_file:
            try:
                # Delete from Albert AI if it exists there
                if db_file.assistant_collection_id and db_file.albert_ai_id:
                    try:
                        await self.albert_service.delete_document(
                            collection_id=db_file.assistant_collection_id,
                            document_id=db_file.albert_ai_id
                        )
                    except Exception as e:
                        # Log error but continue with local deletion
                        print(f"Failed to delete file from Albert AI: {str(e)}")

                # Delete physical file
                os.remove(db_file.file_path)
                # Delete database record
                await self.db.delete(db_file)
                await self.db.commit()
                
            except Exception as e:
                await self.db.rollback()
                raise ValueError(f"Failed to delete file: {str(e)}") 
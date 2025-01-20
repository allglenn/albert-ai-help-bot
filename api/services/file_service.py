import os
import shutil
from fastapi import UploadFile
from pathlib import Path
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import AssistantFile
from models.assistant_file import AssistantFileCreate

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
ALLOWED_EXTENSIONS = {'.pdf', '.md', '.txt'}

class FileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        UPLOAD_DIR.mkdir(exist_ok=True)

    def _is_allowed_file(self, filename: str) -> bool:
        return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

    async def save_file(self, file: UploadFile, help_assistant_id: int) -> AssistantFile:
        if not self._is_allowed_file(file.filename):
            raise ValueError("File type not allowed")

        # Create assistant-specific directory
        assistant_dir = UPLOAD_DIR / str(help_assistant_id)
        assistant_dir.mkdir(exist_ok=True)

        # Save file
        file_path = assistant_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create database record
        db_file = AssistantFile(
            filename=file.filename,
            file_type=Path(file.filename).suffix.lower(),
            file_size=os.path.getsize(file_path),
            file_path=str(file_path),
            help_assistant_id=help_assistant_id
        )
        
        self.db.add(db_file)
        await self.db.commit()
        await self.db.refresh(db_file)
        
        return db_file

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
            # Delete physical file
            os.remove(db_file.file_path)
            # Delete database record
            await self.db.delete(db_file)
            await self.db.commit() 
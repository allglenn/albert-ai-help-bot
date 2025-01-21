from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from db.database import get_db
from models.help_assistant import HelpAssistant, HelpAssistantCreate, HelpAssistantUpdate
from controllers.help_assistant import HelpAssistantController
from views.auth import get_current_user
from models.user import User
from models.assistant_file import AssistantFile
from services.file_service import FileService
from services.external_api import AlbertAIService
from models.collection import Collection
from services.collection_service import CollectionService
from tools.collection_tool import CollectionTool

router = APIRouter(prefix="/help-assistant", tags=["help-assistant"])

@router.post("/", response_model=HelpAssistant)
async def create_help_assistant(
    help_assistant: HelpAssistantCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await HelpAssistantController.create_help_assistant(help_assistant, current_user.id, db)

@router.get("/me", response_model=List[HelpAssistant])
async def get_my_help_assistants(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await HelpAssistantController.get_user_help_assistants(current_user.id, db)

@router.get("/models")
async def list_models():
    ai_service = AlbertAIService()
    response = await ai_service.list_models()
    return response.get('data', [])  # Extract only data key when present 

@router.get("/{help_assistant_id}", response_model=HelpAssistant)
async def get_help_assistant(
    help_assistant_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this help assistant")
    return help_assistant

@router.put("/{help_assistant_id}", response_model=HelpAssistant)
async def update_help_assistant(
    help_assistant_id: int,
    help_assistant_update: HelpAssistantUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this help assistant")
    return await HelpAssistantController.update_help_assistant(help_assistant_id, help_assistant_update, db)

@router.delete("/{help_assistant_id}")
async def delete_help_assistant(
    help_assistant_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this help assistant")
    await HelpAssistantController.delete_help_assistant(help_assistant_id, db)
    return {"message": "Assistant deleted successfully"}

@router.post("/{help_assistant_id}/files", response_model=AssistantFile)
async def upload_file(
    help_assistant_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if user owns the assistant
    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to upload files to this assistant")

    file_service = FileService(db)
    return await file_service.save_file(file, help_assistant_id)

@router.get("/{help_assistant_id}/files", response_model=List[AssistantFile])
async def get_assistant_files(
    help_assistant_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view these files")

    file_service = FileService(db)
    return await file_service.get_assistant_files(help_assistant_id)

@router.delete("/{help_assistant_id}/files/{file_id}")
async def delete_file(
    help_assistant_id: int,
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this file")

    file_service = FileService(db)
    await file_service.delete_file(file_id)
    return {"message": "File deleted successfully"}

@router.get("/{help_assistant_id}/collection", response_model=Collection)
async def get_assistant_collection(
    help_assistant_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this assistant's collection")
    
    collection_service = CollectionService(db)
    return await collection_service.get_by_help_assistant(help_assistant_id)

@router.post("/{assistant_id}/agent/search", response_model=Dict[str, Any])
async def agent_search(
    assistant_id: int,
    query: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Search assistant's collection using AI agent
    """
    try:
        # Get collection for the assistant
        collection_service = CollectionService(db)
        collection = await collection_service.get_by_help_assistant(assistant_id)
        
        if not collection:
            raise HTTPException(
                status_code=404,
                detail="No collection found for this assistant"
            )

        # Initialize tools
        albert_service = AlbertAIService()
        collection_tool = CollectionTool(albert_service)
        
        # Search collection
        search_results = await collection_tool.search_collection(
            collection_id=collection.albert_id,
            query=query["query"]
        )
        
        return {
            "results": search_results,
            "collection_id": collection.albert_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search collection: {str(e)}"
        )


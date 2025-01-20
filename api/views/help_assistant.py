from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.database import get_db
from models.help_assistant import HelpAssistant, HelpAssistantCreate, HelpAssistantUpdate
from controllers.help_assistant import HelpAssistantController
from views.auth import get_current_user
from models.user import User

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
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from db.database import get_db
from models import (
    HelpAssistant, 
    HelpAssistantCreate, 
    HelpAssistantUpdate, 
    HelpAssistantResponse,
    User,
    Chat,
    EmitterType,
    ToneType
)
from controllers.help_assistant import HelpAssistantController
from views.auth import get_current_user
from models.assistant_file import AssistantFile
from services.file_service import FileService
from services.external_api import AlbertAIService
from models.collection import Collection, CollectionResponse
from services.collection_service import CollectionService
from tools.collection_tool import CollectionTool
from fastapi.responses import FileResponse
import os
from services.chat_service import ChatService
from sqlalchemy import select
from models.message import MessageCreate

router = APIRouter(prefix="/help-assistant", tags=["help-assistant"])

@router.get("/tones", response_model=Dict[str, str])
async def get_available_tones():
    """Get all available assistant tones with descriptions in French"""
    return ToneType.get_all_descriptions('fr')

@router.post("/", response_model=HelpAssistantResponse)
async def create_help_assistant(
    help_assistant: HelpAssistantCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await HelpAssistantController.create_help_assistant(help_assistant, current_user.id, db)

@router.get("/me", response_model=List[HelpAssistantResponse])
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

@router.get("/{help_assistant_id}", response_model=HelpAssistantResponse)
async def get_help_assistant(
    help_assistant_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this help assistant")
    return help_assistant

@router.put("/{help_assistant_id}", response_model=HelpAssistantResponse)
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

@router.get("/{help_assistant_id}/collection", response_model=CollectionResponse)
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
            query=query["query"],
            k=10
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

@router.get("/{help_assistant_id}/files/{file_id}/download")
async def get_assistant_file(
    help_assistant_id: int,
    file_id: int,
    token: str = Query(...),  # Make token required query parameter
    db: AsyncSession = Depends(get_db)
):
    """Get a specific file from an assistant"""
    # Verify token manually since we're not using the dependency
    try:
        current_user = await get_current_user(token, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Not authenticated")

    help_assistant = await HelpAssistantController.get_help_assistant(help_assistant_id, db)
    if help_assistant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this file")

    file_service = FileService(db)
    files = await file_service.get_assistant_files(help_assistant_id)
    file = next((f for f in files if f.id == file_id), None)
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        file.file_path,
        filename=file.filename,
        media_type="application/octet-stream"
    )

@router.post("/{assistant_id}/chat/init", response_model=Dict)
async def init_chat(
    assistant_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Initialize a new chat session"""
    try:
        # Debug prints
        print(f"Current user details - ID: {current_user.id}, Email: {current_user.email}")
        
        # Verify user exists in database
        user_query = select(User).where(User.id == current_user.id)
        result = await db.execute(user_query)
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"User {current_user.id} not found in database")  # Debug print
            raise HTTPException(
                status_code=404,
                detail=f"User with ID {current_user.id} not found in database"
            )

        # Check if assistant exists and user has access
        help_assistant = await HelpAssistantController.get_help_assistant(assistant_id, db)
        
        # Get tone with fallback
        tone = getattr(help_assistant, 'tone', None) or ToneType.PROFESSIONAL
        print(f"Assistant details - ID: {assistant_id}, User ID: {help_assistant.user_id}, Tone: {tone}")
        
        if help_assistant.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this assistant")

        # Create new chat
        chat_service = ChatService(db)
        chat = await chat_service.create_chat(assistant_id, current_user.id)

        # Create initial welcome message
        raw_welcome = (
            f"Bonjour ! Je suis {help_assistant.operator_name} de {help_assistant.name}. "
            f"Ma mission est {help_assistant.mission}. "
            "Comment puis-je vous aider aujourd'hui ?"
        )

        # Rephrase welcome message according to assistant's tone
        ai_service = AlbertAIService()
        try:
            welcome_message = await ai_service.rephrase_with_tone(raw_welcome, tone)
        except Exception as e:
            print(f"Error rephrasing welcome message: {str(e)}")
            welcome_message = raw_welcome

        await chat_service.add_message(
            chat_id=chat.id,
            content=welcome_message,
            emitter=EmitterType.ASSISTANT
        )

        return {
            "chat_id": chat.id,
            "assistant": {
                "id": help_assistant.id,
                "name": help_assistant.name,
                "operator_name": help_assistant.operator_name,
                "operator_pic": help_assistant.operator_pic,
                "mission": help_assistant.mission
            },
            "messages": [{
                "content": welcome_message,
                "emitter": EmitterType.ASSISTANT,
                "created_at": chat.created_at
            }]
        }

    except HTTPException:
        raise 
    except Exception as e:
        print(f"Error initializing chat: {str(e)}")  # Debug print
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize chat: {str(e)}"
        )

@router.post("/{assistant_id}/chat/{chat_id}/message", response_model=Dict)
async def add_chat_message(
    assistant_id: int,
    chat_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a message to the chat and get AI response with context"""
    try:
        # Verify user has access to this chat
        chat_service = ChatService(db)
        chat = await chat_service.get_chat(chat_id)
        
        if not chat or chat.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this chat")
            
        # Get the assistant
        help_assistant = await HelpAssistantController.get_help_assistant(assistant_id, db)
        
        # Save user message
        await chat_service.add_message(
            chat_id=chat_id,
            content=message.content,
            emitter=EmitterType.USER
        )
        
        # Get chat history for context
        chat_history = await chat_service.get_chat_messages(chat_id)
        
        # Format chat history as a list of dictionaries
        formatted_history = [
            {"role": "assistant" if msg.emitter == EmitterType.ASSISTANT else "user", "content": msg.content}
            for msg in chat_history
        ]
        
        # Build system context with assistant details
        system_context = (
            f"Tu es {help_assistant.operator_name}, un assistant virtuel de {help_assistant.name}. "
            f"Ta mission est {help_assistant.mission}. "
            f"Ton ton de communication est {help_assistant.tone or 'professionnel'}. "
            "Réponds toujours en français de manière naturelle et cohérente avec ton rôle."
        )
        
        # Get collection for knowledge base context
        collection_service = CollectionService(db)
        collection: Optional[Collection] = await collection_service.get_by_help_assistant(assistant_id)
        
        # Initialize tools
        ai_service = AlbertAIService()
        collection_tool = CollectionTool(ai_service)
        
        # Get response using chat_with_context
        if collection:
            print(f"Using collection: {collection.albert_id}")  # Debug print
            response = await collection_tool.chat_with_context(
                collection_id=collection.albert_id,
                prompt=message.content,
                context={
                    "system": system_context,
                    "chat_history": formatted_history  # Pass the formatted history
                }
            )
        else:
            print("No collection found, using fallback")  # Debug print
            # Fallback if no collection exists
            response = await ai_service.chat_completion(
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": formatted_history + "\n\nUser: " + message.content}
                ]
            )
        print(f"AI response: {response}")  # Debug print

        # Save assistant response
        assistant_message = await chat_service.add_message(
            chat_id=chat_id,
            content=response['choices'][0]['message']['content'],
            emitter=EmitterType.ASSISTANT
        )
        
        return {
            "message": assistant_message,
            "chat_id": chat_id,
            "assistant": {
                "id": help_assistant.id,
                "name": help_assistant.name,
                "operator_name": help_assistant.operator_name
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message: {str(e)}"
        )


from fastapi import APIRouter, Depends, HTTPException
from controllers.user import UserController
from models.user import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    return await UserController.create_user(user)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    return await UserController.get_user(user_id) 
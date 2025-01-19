from fastapi import APIRouter, Depends, Security, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth import Token, LoginRequest
from models.user import User
from controllers.auth import AuthController
from services.auth_service import AuthService
from db.database import get_db
import asyncio
import random

router = APIRouter(prefix="/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    login_request = LoginRequest(
        email=form_data.username,
        password=form_data.password
    )
    return await AuthController.login(login_request, db)

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await AuthController.login(login_data, db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    auth_service = AuthService(db)
    return await auth_service.get_current_user(token)

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    return await AuthController.logout(token, db)

@router.get("/test-metrics")
async def test_metrics():
    """Endpoint to generate test metrics"""
    # Simulate work with random delay
    delay = random.uniform(0.1, 0.5)
    await asyncio.sleep(delay)
    
    # Randomly generate different responses
    rand = random.random()
    if rand < 0.6:  # 60% success
        return {"message": "Success", "delay": delay}
    elif rand < 0.8:  # 20% client error
        return Response(
            status_code=400,
            content='{"error": "Bad Request"}',
            media_type="application/json"
        )
    else:  # 20% server error
        return Response(
            status_code=500,
            content='{"error": "Internal Server Error"}',
            media_type="application/json"
        ) 
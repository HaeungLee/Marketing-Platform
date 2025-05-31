from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....domain.services.auth_service import AuthService
from ....interfaces.api.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterPersonalRequest,
    RegisterBusinessRequest,
    RegisterResponse,
)
from ....interfaces.api.dependencies import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    print(f"Login attempt with user ID: {request.user_id}")  # 디버깅용 로그
    auth_service = AuthService(db)
    try:
        user, access_token = auth_service.authenticate_user(
            request.user_id, request.password
        )
        print(f"Login successful for user: {user.id}")  # 디버깅용 로그
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "user_type": user.user_type.value,
        }
    except Exception as e:
        print(f"Login failed: {str(e)}")  # 디버깅용 로그
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@router.post("/register/personal", response_model=RegisterResponse)
def register_personal(request: RegisterPersonalRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        user = auth_service.register_personal_user(
            request.username,
            request.email,
            request.password,
        )
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type.value,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post("/register/business", response_model=RegisterResponse)
def register_business(request: RegisterBusinessRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        user = auth_service.register_business_user(
            request.username,
            request.email,
            request.password,
        )
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type.value,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
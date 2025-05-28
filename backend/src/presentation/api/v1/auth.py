"""
인증 관련 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional

from backend.src.config.settings import settings

router = APIRouter()
security = HTTPBearer()


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    username: str
    password: str


class SocialLoginRequest(BaseModel):
    provider: str  # 'google', 'naver', 'kakao'
    token: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """회원가입"""
    # TODO: 실제 구현 필요
    return {
        "access_token": "fake-jwt-token",
        "user_id": "user-123",
        "username": request.username
    }


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """로그인"""
    # TODO: 실제 구현 필요
    return {
        "access_token": "fake-jwt-token",
        "user_id": "user-123",
        "username": "testuser"
    }


@router.post("/social-login", response_model=AuthResponse)
async def social_login(request: SocialLoginRequest):
    """소셜 로그인"""
    
    # API 키 설정 확인
    config_status = settings.is_social_login_configured
    
    if request.provider == "google" and not config_status["google"]:
        raise HTTPException(
            status_code=501,
            detail="Google 로그인 API 키가 설정되지 않았습니다. 관리자에게 문의하세요."
        )
    
    if request.provider == "naver" and not config_status["naver"]:
        raise HTTPException(
            status_code=501,
            detail="네이버 로그인 API 키가 설정되지 않았습니다. 관리자에게 문의하세요."
        )
    
    if request.provider == "kakao" and not config_status["kakao"]:
        raise HTTPException(
            status_code=501,
            detail="카카오 로그인 API 키가 설정되지 않았습니다. 관리자에게 문의하세요."
        )
    
    # TODO: 실제 소셜 로그인 구현 필요
    return {
        "access_token": "fake-social-jwt-token",
        "user_id": f"social-user-{request.provider}",
        "username": f"{request.provider}_user"
    }


@router.post("/logout")
async def logout():
    """로그아웃"""
    return {"message": "Successfully logged out"}


@router.post("/refresh")
async def refresh_token():
    """토큰 갱신"""
    # TODO: 실제 구현 필요
    return {
        "access_token": "refreshed-jwt-token",
        "token_type": "bearer"
    }


@router.get("/me")
async def get_current_user():
    """현재 사용자 정보 조회"""
    # TODO: 실제 구현 필요 (JWT 토큰 검증)
    return {
        "user_id": "user-123",
        "username": "testuser",
        "email": "test@example.com",
        "is_active": True
    }

"""
Auth 관련 Pydantic 모델
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from domain.entities.user_type import UserType

# 기본 사용자 등록 모델
class UserRegisterBase(BaseModel):
    user_id: str = Field(..., min_length=4, max_length=20)
    email: EmailStr
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None

# 개인 사용자 등록 모델
class PersonalUserRegister(UserRegisterBase):
    pass

# 사업자 사용자 등록 모델
class BusinessUserRegister(UserRegisterBase):
    business_name: str
    business_registration_number: str
    business_type: str
    business_category: str
    address: str
    representative_name: str

# 로그인 요청 모델
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 토큰 응답 모델
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    user_type: UserType

# 사용자 응답 모델
class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    phone: Optional[str] = None
    user_type: UserType
    created_at: datetime
    updated_at: datetime

# 이메일 인증 요청 모델
class EmailVerificationRequest(BaseModel):
    email: EmailStr
    code: str

# 이메일 인증 응답 모델
class EmailVerificationResponse(BaseModel):
    is_verified: bool
    message: str

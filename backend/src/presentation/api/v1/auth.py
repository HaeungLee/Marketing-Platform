"""
인증 관련 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from sqlalchemy.orm import Session
from typing import Union, Dict, Any
import secrets
from datetime import datetime, timedelta
from pydantic import BaseModel, ValidationError
import uuid
import logging
import json

from domain.schemas.auth import (
    PersonalUserRegister,
    BusinessUserRegister,
    LoginRequest,
    Token,
    UserResponse,
    EmailVerificationRequest,
    EmailVerificationResponse
)
from domain.entities.user import User, BusinessProfile, EmailVerification, PasswordReset
from domain.entities.user_type import UserType
from config.database import get_db
from infrastructure.security.password import get_password_hash, verify_password
from infrastructure.security.jwt import create_access_token
from infrastructure.email import send_verification_email, send_password_reset_email
from config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

def format_error_response(error: Any) -> Dict[str, Any]:
    """에러 응답 형식 변환"""
    if isinstance(error, ValidationError):
        return {
            "status": "error",
            "message": "입력 데이터가 올바르지 않습니다.",
            "errors": [{"field": err["loc"][0], "message": err["msg"]} for err in error.errors()]
        }
    elif isinstance(error, HTTPException):
        return {
            "status": "error",
            "message": error.detail
        }
    else:
        return {
            "status": "error",
            "message": str(error)
        }

# 이메일 인증 요청 모델
class EmailRequest(BaseModel):
    email: str


@router.post("/register/personal", response_model=Token)
async def register_personal(
    request: Request,
    user_data: PersonalUserRegister,
    db: Session = Depends(get_db)
):
    """개인 사용자 회원가입"""
    try:
        # 요청 데이터 로깅
        body = await request.body()
        logger.info(f"Raw request body: {body.decode()}")
        logger.info(f"Parsed user data: {user_data.dict()}")
        
        # 중복 ID 체크
        if db.query(User).filter(User.id == user_data.user_id).first():
            logger.warning(f"중복된 ID: {user_data.user_id}")
            raise HTTPException(
                status_code=400,
                detail="이미 사용 중인 ID입니다."
            )
        
        # 중복 이메일 체크
        if db.query(User).filter(User.email == user_data.email).first():
            logger.warning(f"중복된 이메일: {user_data.email}")
            raise HTTPException(
                status_code=400,
                detail="이미 사용 중인 이메일입니다."
            )
        
        # 새 사용자 생성
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            id=user_data.user_id,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            phone=user_data.phone,
            user_type=UserType.PERSONAL
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # 액세스 토큰 생성
        access_token = create_access_token(
            data={"sub": new_user.id, "user_type": new_user.user_type.value}
        )
        
        logger.info(f"회원가입 성공: {new_user.id}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=new_user.id,
            user_type=new_user.user_type
        )
        
    except ValidationError as e:
        logger.error(f"유효성 검사 오류: {str(e)}")
        logger.error(f"Validation errors: {e.errors()}")
        return {
            "status": "error",
            "message": "입력 데이터가 올바르지 않습니다.",
            "errors": [{"field": err["loc"][0], "message": err["msg"]} for err in e.errors()]
        }
    except HTTPException as e:
        logger.error(f"HTTP 예외: {str(e)}")
        return {
            "status": "error",
            "message": e.detail
        }
    except Exception as e:
        logger.error(f"회원가입 중 오류 발생: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/register/business", response_model=Token)
async def register_business(
    user_data: BusinessUserRegister,
    db: Session = Depends(get_db)
):
    """사업자 회원가입"""
    try:
        logger.info(f"사업자 회원가입 요청 데이터: {user_data.dict()}")
        
        # 중복 ID 체크
        if db.query(User).filter(User.id == user_data.id).first():
            logger.warning(f"중복된 ID: {user_data.id}")
            raise HTTPException(
                status_code=400,
                detail="이미 사용 중인 ID입니다."
            )
        
        # 중복 이메일 체크
        if db.query(User).filter(User.email == user_data.email).first():
            logger.warning(f"중복된 이메일: {user_data.email}")
            raise HTTPException(
                status_code=400,
                detail="이미 사용 중인 이메일입니다."
            )
        
        # 새 사용자 생성
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            id=user_data.id,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            phone=user_data.phone,
            user_type=UserType.BUSINESS
        )
        
        db.add(new_user)
        db.flush()  # ID를 얻기 위해 flush
        
        # 사업자 프로필 생성
        business_profile = BusinessProfile(
            users_id=new_user.id,
            business_name=user_data.business_profile.business_name,
            business_registration_number=user_data.business_profile.business_registration_number,
            business_type=user_data.business_profile.business_type,
            business_category=user_data.business_profile.business_category,
            address=user_data.business_profile.address,
            representative_name=user_data.business_profile.representative_name
        )
        
        db.add(business_profile)
        db.commit()
        db.refresh(new_user)
        
        # 액세스 토큰 생성
        access_token = create_access_token(
            data={"sub": new_user.id, "user_type": new_user.user_type.value}
        )
        
        logger.info(f"사업자 회원가입 성공: {new_user.id}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=new_user.id,
            user_type=new_user.user_type
        )
        
    except ValidationError as e:
        logger.error(f"유효성 검사 오류: {str(e)}")
        return format_error_response(e)
    except HTTPException as e:
        logger.error(f"HTTP 예외: {str(e)}")
        return format_error_response(e)
    except Exception as e:
        logger.error(f"사업자 회원가입 중 오류 발생: {str(e)}")
        return format_error_response(e)


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """로그인"""
    try:
        logger.info(f"로그인 시도: {login_data.email}")
        
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            logger.warning(f"로그인 실패: {login_data.email}")
            raise HTTPException(
                status_code=401,
                detail="이메일 또는 비밀번호가 올바르지 않습니다."
            )
        
        access_token = create_access_token(
            data={"sub": user.id, "user_type": user.user_type.value}
        )
        
        logger.info(f"로그인 성공: {user.id}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            user_type=user.user_type
        )
        
    except ValidationError as e:
        logger.error(f"유효성 검사 오류: {str(e)}")
        return format_error_response(e)
    except HTTPException as e:
        logger.error(f"HTTP 예외: {str(e)}")
        return format_error_response(e)
    except Exception as e:
        logger.error(f"로그인 중 오류 발생: {str(e)}")
        return format_error_response(e)


@router.post("/send-verification-email", response_model=EmailVerificationResponse)
async def send_verification_email_endpoint(
    request: EmailRequest,
    db: Session = Depends(get_db)
):
    """이메일 인증 메일 발송"""
    # 이메일 중복 체크
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=400,
            detail="이미 사용 중인 이메일입니다."
        )
    
    # 인증 코드 생성
    verification_code = str(uuid.uuid4())[:6]
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    # 기존 인증 정보 삭제
    db.query(EmailVerification).filter(EmailVerification.email == request.email).delete()
    
    # 새로운 인증 정보 저장
    verification = EmailVerification(
        id=str(uuid.uuid4()),  # UUID 생성
        email=request.email,
        code=verification_code,
        expires_at=expires_at
    )
    db.add(verification)
    db.commit()
    
    # 이메일 전송
    try:
        await send_verification_email(request.email, verification_code)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="이메일 전송에 실패했습니다."
        )
    
    return EmailVerificationResponse(
        message="인증 이메일이 전송되었습니다.",
        expires_at=expires_at
    )


@router.post("/verify-email", response_model=dict)
async def verify_email(
    verification_data: EmailVerificationRequest,
    db: Session = Depends(get_db)
):
    """이메일 인증 코드 확인"""
    verification = db.query(EmailVerification).filter(
        EmailVerification.email == verification_data.email,
        EmailVerification.code == verification_data.code,
        EmailVerification.expires_at > datetime.utcnow()
    ).first()
    
    if not verification:
        raise HTTPException(
            status_code=400,
            detail="잘못된 인증 코드입니다."
        )
    
    # 인증 완료 처리
    verification.verified = True
    verification.verified_at = datetime.utcnow()
    db.commit()
    
    return {"message": "이메일 인증이 완료되었습니다."}


@router.post("/forgot-password")
async def forgot_password(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """비밀번호 재설정 이메일 발송"""
    try:
        logger.info(f"비밀번호 재설정 요청: {email}")
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # 보안을 위해 사용자가 존재하지 않아도 성공 응답
            return {"status": "success", "message": "If the email exists, a password reset link will be sent"}
        
        # 재설정 토큰 생성
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        # 기존 토큰 삭제
        db.query(PasswordReset).filter(PasswordReset.user_id == user.id).delete()
        
        # 새로운 토큰 저장
        reset = PasswordReset(
            user_id=user.id,
            token=reset_token,
            expires_at=expires_at
        )
        db.add(reset)
        db.commit()
        
        # 이메일 발송 (백그라운드 작업)
        background_tasks.add_task(send_password_reset_email, email, reset_token)
        
        logger.info(f"비밀번호 재설정 이메일 발송 성공: {email}")
        
        return {"status": "success", "message": "If the email exists, a password reset link will be sent"}
        
    except Exception as e:
        logger.error(f"비밀번호 재설정 이메일 발송 중 오류 발생: {str(e)}")
        return format_error_response(e)


@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """비밀번호 재설정"""
    try:
        logger.info(f"비밀번호 재설정 시도: {token}")
        
        reset = db.query(PasswordReset).filter(
            PasswordReset.token == token,
            PasswordReset.expires_at > datetime.utcnow(),
            PasswordReset.used == False
        ).first()
        
        if not reset:
            logger.warning(f"유효하지 않은 재설정 토큰: {token}")
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        
        # 비밀번호 업데이트
        user = db.query(User).filter(User.id == reset.user_id).first()
        user.hashed_password = get_password_hash(new_password)
        
        # 토큰 사용 처리
        reset.used = True
        reset.used_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"비밀번호 재설정 성공: {user.id}")
        
        return {"status": "success", "message": "Password has been reset successfully"}
        
    except ValidationError as e:
        logger.error(f"유효성 검사 오류: {str(e)}")
        return format_error_response(e)
    except HTTPException as e:
        logger.error(f"HTTP 예외: {str(e)}")
        return format_error_response(e)
    except Exception as e:
        logger.error(f"비밀번호 재설정 중 오류 발생: {str(e)}")
        return format_error_response(e)

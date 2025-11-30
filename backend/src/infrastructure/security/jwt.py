"""
JWT 토큰 관련 유틸리티

보안 강화:
- 토큰에 issuer, audience 추가
- Refresh Token 지원
- Token Blacklist 지원 (Redis 연동)
- 토큰 타입 구분 (access/refresh)
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Literal
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from src.config.settings import settings

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# Token types
TokenType = Literal["access", "refresh"]


class TokenPayload:
    """토큰 페이로드 데이터 클래스"""
    def __init__(
        self,
        sub: str,
        exp: datetime,
        iat: datetime,
        token_type: TokenType,
        iss: str,
        aud: str,
        jti: Optional[str] = None,
        **extra_data
    ):
        self.sub = sub
        self.exp = exp
        self.iat = iat
        self.token_type = token_type
        self.iss = iss
        self.aud = aud
        self.jti = jti
        self.extra_data = extra_data


def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None,
    include_refresh: bool = False
) -> Dict[str, str]:
    """
    Access 토큰 생성
    
    Args:
        data: 토큰에 포함할 데이터 (sub 필드 필수)
        expires_delta: 만료 시간 (기본값: settings에서 가져옴)
        include_refresh: Refresh 토큰도 함께 생성할지 여부
    
    Returns:
        토큰 딕셔너리 {"access_token": "...", "refresh_token": "...", "token_type": "bearer"}
    """
    import secrets
    
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    
    # Access Token 만료 시간
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    
    # 표준 JWT 클레임 추가
    to_encode.update({
        "exp": expire,
        "iat": now,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "token_type": "access",
        "jti": secrets.token_urlsafe(16),  # JWT ID for blacklisting
    })
    
    access_token = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.jwt_algorithm
    )
    
    result = {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int((expire - now).total_seconds()),
    }
    
    # Refresh Token 생성 (선택적)
    if include_refresh:
        refresh_token = create_refresh_token(data)
        result["refresh_token"] = refresh_token
    
    return result


def create_refresh_token(data: dict) -> str:
    """
    Refresh 토큰 생성
    
    Refresh 토큰은 Access 토큰보다 긴 만료 시간을 가짐
    """
    import secrets
    
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.refresh_token_expire_days)
    
    to_encode.update({
        "exp": expire,
        "iat": now,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "token_type": "refresh",
        "jti": secrets.token_urlsafe(16),
    })
    
    return jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.jwt_algorithm
    )


def verify_token(
    token: str, 
    expected_type: Optional[TokenType] = "access",
    verify_audience: bool = True,
    verify_issuer: bool = True
) -> dict:
    """
    토큰 검증
    
    Args:
        token: JWT 토큰 문자열
        expected_type: 예상되는 토큰 타입 (access/refresh)
        verify_audience: audience 검증 여부
        verify_issuer: issuer 검증 여부
    
    Returns:
        검증된 토큰 페이로드
    
    Raises:
        HTTPException: 토큰 검증 실패시
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # JWT 디코딩 옵션
        options = {
            "verify_aud": verify_audience,
            "verify_iss": verify_issuer,
        }
        
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience if verify_audience else None,
            issuer=settings.jwt_issuer if verify_issuer else None,
            options=options
        )
        
        # 토큰 타입 검증
        token_type = payload.get("token_type")
        if expected_type and token_type != expected_type:
            logger.warning(f"Token type mismatch: expected {expected_type}, got {token_type}")
            raise credentials_exception
        
        # 필수 필드 검증
        if not payload.get("sub"):
            logger.warning("Token missing 'sub' field")
            raise credentials_exception
            
        return payload
        
    except ExpiredSignatureError:
        logger.info("Token has expired")
        raise expired_exception
    except JWTError as e:
        logger.warning(f"JWT validation error: {e}")
        raise credentials_exception


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    현재 인증된 사용자 정보 가져오기 (FastAPI Dependency)
    
    Usage:
        @router.get("/protected")
        async def protected_route(current_user: dict = Depends(get_current_user)):
            return {"user": current_user}
    """
    token = credentials.credentials
    payload = verify_token(token, expected_type="access")
    return payload


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[dict]:
    """
    현재 인증된 사용자 정보 가져오기 (선택적, 인증 없어도 OK)
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = verify_token(token, expected_type="access")
        return payload
    except HTTPException:
        return None


def refresh_access_token(refresh_token: str) -> Dict[str, str]:
    """
    Refresh 토큰을 사용하여 새 Access 토큰 발급
    
    Args:
        refresh_token: 유효한 Refresh 토큰
    
    Returns:
        새로운 Access 토큰
    """
    payload = verify_token(refresh_token, expected_type="refresh")
    
    # 새 Access 토큰 생성 (sub 정보만 사용)
    user_data = {"sub": payload.get("sub")}
    
    # 기타 사용자 정보가 있다면 포함
    for key in ["email", "name", "role"]:
        if key in payload:
            user_data[key] = payload[key]
    
    return create_access_token(user_data)


# Token Blacklist (Redis 연동시 사용)
class TokenBlacklist:
    """
    토큰 블랙리스트 관리
    로그아웃 또는 토큰 무효화시 사용
    """
    
    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self._local_blacklist: set = set()  # Redis 없을 때 임시 저장
    
    async def add(self, jti: str, expires_in: int) -> bool:
        """토큰을 블랙리스트에 추가"""
        if self.redis_client:
            await self.redis_client.setex(
                f"token_blacklist:{jti}", 
                expires_in, 
                "1"
            )
            return True
        else:
            self._local_blacklist.add(jti)
            return True
    
    async def is_blacklisted(self, jti: str) -> bool:
        """토큰이 블랙리스트에 있는지 확인"""
        if self.redis_client:
            result = await self.redis_client.get(f"token_blacklist:{jti}")
            return result is not None
        else:
            return jti in self._local_blacklist
    
    async def remove(self, jti: str) -> bool:
        """토큰을 블랙리스트에서 제거"""
        if self.redis_client:
            await self.redis_client.delete(f"token_blacklist:{jti}")
            return True
        else:
            self._local_blacklist.discard(jti)
            return True


# 전역 블랙리스트 인스턴스 (Redis 연결 후 초기화)
token_blacklist = TokenBlacklist()

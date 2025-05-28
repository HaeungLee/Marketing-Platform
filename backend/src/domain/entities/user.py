"""
User 엔티티 구현
SOLID 원칙과 Clean Architecture 준수
"""
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from backend.src.domain.value_objects.email import Email


@dataclass
class User:
    """사용자 엔티티"""
    
    id: str
    email: Email
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    social_provider: Optional[str] = None  # 'google', 'naver', 'kakao'
    social_id: Optional[str] = None
    
    def __post_init__(self):
        """생성 후 유효성 검증"""
        self._validate_username()
    
    def _validate_username(self):
        """사용자명 유효성 검증"""
        if not self.username or not self.username.strip():
            raise ValueError("Username cannot be empty")
        
        if len(self.username) < 2:
            raise ValueError("Username must be at least 2 characters long")
        
        if len(self.username) > 50:
            raise ValueError("Username must be less than 50 characters")
    
    def deactivate(self):
        """사용자 비활성화"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self):
        """사용자 활성화"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def update_password(self, new_hashed_password: str):
        """비밀번호 업데이트"""
        if not new_hashed_password:
            raise ValueError("Password cannot be empty")
        
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.utcnow()
    
    def update_username(self, new_username: str):
        """사용자명 업데이트"""
        old_username = self.username
        self.username = new_username
        
        try:
            self._validate_username()
            self.updated_at = datetime.utcnow()
        except ValueError:
            # 유효성 검증 실패 시 원래 값으로 복원
            self.username = old_username
            raise

"""
Email 값 객체 구현
SOLID 원칙: 단일 책임 - 이메일 검증과 관련된 로직만 담당
"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)  # 불변 객체
class Email:
    """이메일 값 객체"""
    
    value: str
    
    def __post_init__(self):
        """생성 후 유효성 검증"""
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email format: {self.value}")
    
    def _is_valid_email(self, email: str) -> bool:
        """이메일 형식 검증"""
        if not email or not isinstance(email, str):
            return False
        
        # 기본적인 이메일 정규식 패턴
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Email):
            return False
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)

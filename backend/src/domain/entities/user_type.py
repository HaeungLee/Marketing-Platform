"""
사용자 타입 정의
"""
from enum import Enum

class UserType(Enum):
    PERSONAL = "personal"    # 개인 사용자
    BUSINESS = "business"    # 사업자

"""
User 엔티티 테스트
TDD 방식: 테스트 먼저 작성
"""
import pytest
import sys
import os
from uuid import uuid4

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from domain.entities.user import User
from domain.value_objects.email import Email


class TestUser:
    """User 엔티티 테스트 클래스"""
    
    def test_should_create_user_with_valid_data(self):
        """유효한 데이터로 사용자 생성 테스트"""
        # Given
        user_id = str(uuid4())
        email = Email("test@example.com")
        username = "testuser"
        hashed_password = "hashed_password_123"
        
        # When
        user = User(
            id=user_id,
            email=email,
            username=username,
            hashed_password=hashed_password
        )
        
        # Then
        assert user.id == user_id
        assert user.email == email
        assert user.username == username
        assert user.hashed_password == hashed_password
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_should_raise_error_for_invalid_username(self):
        """잘못된 사용자명에 대한 에러 테스트"""
        # Given
        user_id = str(uuid4())
        email = Email("test@example.com")
        invalid_username = ""  # 빈 문자열
        hashed_password = "hashed_password_123"
        
        # When & Then
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User(
                id=user_id,
                email=email,
                username=invalid_username,
                hashed_password=hashed_password
            )
    
    def test_should_deactivate_user(self):
        """사용자 비활성화 테스트"""
        # Given
        user = User(
            id=str(uuid4()),
            email=Email("test@example.com"),
            username="testuser",
            hashed_password="hashed_password_123"
        )
        
        # When
        user.deactivate()
        
        # Then
        assert user.is_active is False
    
    def test_should_update_password(self):
        """비밀번호 업데이트 테스트"""
        # Given
        user = User(
            id=str(uuid4()),
            email=Email("test@example.com"),
            username="testuser",
            hashed_password="old_password"
        )
        new_password = "new_hashed_password"
        
        # When
        user.update_password(new_password)
        
        # Then
        assert user.hashed_password == new_password
        assert user.updated_at is not None

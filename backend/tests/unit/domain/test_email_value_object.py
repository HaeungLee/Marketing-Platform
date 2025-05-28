"""
Email 값 객체 테스트
"""
import pytest
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from domain.value_objects.email import Email


class TestEmail:
    """Email 값 객체 테스트 클래스"""
    
    def test_should_create_valid_email(self):
        """유효한 이메일 생성 테스트"""
        # Given
        email_str = "test@example.com"
        
        # When
        email = Email(email_str)
        
        # Then
        assert email.value == email_str
        assert str(email) == email_str
    
    def test_should_raise_error_for_invalid_email(self):
        """잘못된 이메일 형식 에러 테스트"""
        # Given
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "",
            "test..test@example.com"
        ]
        
        # When & Then
        for invalid_email in invalid_emails:
            with pytest.raises(ValueError, match="Invalid email format"):
                Email(invalid_email)
    
    def test_email_equality(self):
        """이메일 동등성 테스트"""
        # Given
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("different@example.com")
        
        # When & Then
        assert email1 == email2
        assert email1 != email3
        assert hash(email1) == hash(email2)

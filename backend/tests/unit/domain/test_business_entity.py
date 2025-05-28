"""
Business 엔티티 테스트
"""
import pytest
import sys
import os
from uuid import uuid4

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from domain.entities.business import Business
from domain.value_objects.coordinates import Coordinates


class TestBusiness:
    """Business 엔티티 테스트 클래스"""
    
    def test_should_create_business_with_valid_data(self):
        """유효한 데이터로 비즈니스 생성 테스트"""
        # Given
        business_id = str(uuid4())
        user_id = str(uuid4())
        name = "테스트 카페"
        category = "음식점>카페"
        description = "맛있는 커피를 파는 카페"
        coordinates = Coordinates(37.5665, 126.9780)  # 서울시청
        
        # When
        business = Business(
            id=business_id,
            user_id=user_id,
            name=name,
            category=category,
            description=description,
            coordinates=coordinates
        )
        
        # Then
        assert business.id == business_id
        assert business.user_id == user_id
        assert business.name == name
        assert business.category == category
        assert business.description == description
        assert business.coordinates == coordinates
        assert business.created_at is not None
    
    def test_should_raise_error_for_empty_name(self):
        """빈 비즈니스 이름에 대한 에러 테스트"""
        # Given & When & Then
        with pytest.raises(ValueError, match="Business name cannot be empty"):
            Business(
                id=str(uuid4()),
                user_id=str(uuid4()),
                name="",
                category="음식점>카페",
                description="설명",
                coordinates=Coordinates(37.5665, 126.9780)
            )
    
    def test_should_update_business_info(self):
        """비즈니스 정보 업데이트 테스트"""
        # Given
        business = Business(
            id=str(uuid4()),
            user_id=str(uuid4()),
            name="기존 카페",
            category="음식점>카페",
            description="기존 설명",
            coordinates=Coordinates(37.5665, 126.9780)
        )
        
        # When
        business.update_info(
            name="새로운 카페",
            description="새로운 설명"
        )
        
        # Then
        assert business.name == "새로운 카페"
        assert business.description == "새로운 설명"
        assert business.updated_at is not None

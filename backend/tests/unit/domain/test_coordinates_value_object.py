"""
Coordinates 값 객체 테스트
"""
import pytest
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from domain.value_objects.coordinates import Coordinates


class TestCoordinates:
    """Coordinates 값 객체 테스트 클래스"""
    
    def test_should_create_valid_coordinates(self):
        """유효한 좌표 생성 테스트"""
        # Given
        latitude = 37.5665
        longitude = 126.9780
        
        # When
        coords = Coordinates(latitude, longitude)
        
        # Then
        assert coords.latitude == latitude
        assert coords.longitude == longitude
    
    def test_should_raise_error_for_invalid_latitude(self):
        """잘못된 위도에 대한 에러 테스트"""
        # Given & When & Then
        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            Coordinates(91.0, 126.9780)
        
        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            Coordinates(-91.0, 126.9780)
    
    def test_should_raise_error_for_invalid_longitude(self):
        """잘못된 경도에 대한 에러 테스트"""
        # Given & When & Then
        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            Coordinates(37.5665, 181.0)
        
        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            Coordinates(37.5665, -181.0)
    
    def test_coordinates_equality(self):
        """좌표 동등성 테스트"""
        # Given
        coords1 = Coordinates(37.5665, 126.9780)
        coords2 = Coordinates(37.5665, 126.9780)
        coords3 = Coordinates(37.5666, 126.9780)
        
        # When & Then
        assert coords1 == coords2
        assert coords1 != coords3

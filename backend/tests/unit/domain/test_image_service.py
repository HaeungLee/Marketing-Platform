"""
Image Service 테스트
TDD 방식: 테스트 먼저 작성
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, AsyncMock
from base64 import b64encode

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from domain.services.image_service import ImageService


class TestImageService:
    """Image Service 테스트 클래스"""
    
    @pytest.fixture
    def image_service(self):
        """ImageService 인스턴스를 반환하는 픽스처"""
        return ImageService()
    
    @pytest.mark.asyncio
    async def test_should_generate_image_with_valid_prompt(self, image_service):
        """유효한 프롬프트로 이미지 생성 테스트"""
        # Given
        prompt = "modern cafe flyer design"
        
        # Mock Gemini API response
        mock_response = Mock()
        mock_candidate = Mock()
        mock_content = Mock()
        mock_part = Mock()
        mock_inline_data = Mock()
        
        # Base64 인코딩된 샘플 이미지 데이터 (1x1 PNG)
        sample_image_data = b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x12IDATx\x9cc```bPPP\x00\x02D\x00\x00Z\x00\x02Fs\x95\x14\x00\x00\x00\x00IEND\xaeB`\x82').decode('utf-8')
        
        mock_inline_data.data = sample_image_data
        mock_part.inline_data = mock_inline_data
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        
        # Mock the generate_content method
        with patch.object(image_service.image_model, 'generate_content', return_value=mock_response):
            # When
            result = await image_service.generate_image(prompt)
            
            # Then
            assert result is not None
            assert isinstance(result, str)
            assert len(result) > 0
            # Base64 문자열인지 확인
            import base64
            try:
                base64.b64decode(result)
                assert True
            except Exception:
                assert False, "Result should be valid base64 string"
    
    @pytest.mark.asyncio
    async def test_should_generate_placeholder_when_api_fails(self, image_service):
        """API 실패 시 플레이스홀더 이미지 생성 테스트"""
        # Given
        prompt = "test prompt"
        
        # Mock API failure
        with patch.object(image_service.image_model, 'generate_content', side_effect=Exception("API Error")):
            # When
            result = await image_service.generate_image(prompt)
            
            # Then
            assert result is not None
            assert isinstance(result, str)
            assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_should_handle_empty_prompt(self, image_service):
        """빈 프롬프트 처리 테스트"""
        # Given
        prompt = ""
        
        # When
        result = await image_service.generate_image(prompt)
        
        # Then
        assert result is not None  # 플레이스홀더 이미지라도 생성되어야 함
    
    @pytest.mark.asyncio
    async def test_should_enhance_korean_prompt(self, image_service):
        """한국어 프롬프트 향상 테스트"""
        # Given
        korean_prompt = "카페 전단지 디자인"
        
        # Mock Gemini API response
        mock_response = Mock()
        mock_candidate = Mock()
        mock_content = Mock()
        mock_part = Mock()
        mock_inline_data = Mock()
        
        sample_image_data = "base64_encoded_image_data"
        mock_inline_data.data = sample_image_data
        mock_part.inline_data = mock_inline_data
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        
        # Capture the enhanced prompt
        captured_prompt = None
        def capture_prompt(prompt):
            nonlocal captured_prompt
            captured_prompt = prompt
            return mock_response
        
        with patch.object(image_service.image_model, 'generate_content', side_effect=capture_prompt):
            # When
            await image_service.generate_image(korean_prompt)
            
            # Then
            assert captured_prompt is not None
            assert "Create a high-quality, detailed image:" in captured_prompt
            assert korean_prompt in captured_prompt
    
    @pytest.mark.asyncio 
    async def test_placeholder_image_generation(self, image_service):
        """플레이스홀더 이미지 생성 기능 테스트"""
        # Given
        prompt = "test placeholder"
        
        # When
        result = await image_service.generate_placeholder_image(prompt)
        
        # Then
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Base64 디코딩 테스트
        import base64
        try:
            decoded_data = base64.b64decode(result)
            assert len(decoded_data) > 0
        except Exception:
            assert False, "Placeholder image should be valid base64"
    
    def test_should_initialize_with_correct_model(self, image_service):
        """올바른 모델로 초기화되는지 테스트"""
        # Then
        assert image_service.image_model is not None
        # Note: 실제 모델명은 환경에 따라 다를 수 있으므로 존재 여부만 확인

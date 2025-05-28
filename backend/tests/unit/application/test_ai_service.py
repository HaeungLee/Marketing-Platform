"""
AI 서비스 인터페이스 테스트
"""
import pytest
import sys
import os
from unittest.mock import AsyncMock, Mock

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from application.interfaces.ai_service import AIService
from infrastructure.ai.ollama_service import OllamaService


class TestAIService:
    """AI 서비스 인터페이스 테스트"""
    
    @pytest.mark.asyncio
    async def test_should_generate_content_successfully(self):
        """콘텐츠 생성 성공 테스트"""
        # Given
        mock_service = AsyncMock(spec=AIService)
        mock_service.generate_content.return_value = {
            "blog_content": "테스트 블로그 포스트",
            "instagram_content": "테스트 인스타그램 포스트 #테스트",
            "youtube_script": "30초 유튜브 스크립트",
            "hashtags": ["#테스트", "#카페", "#서울"]
        }
        
        business_info = {
            "name": "테스트 카페",
            "category": "음식점>카페",
            "description": "맛있는 커피"
        }
        
        # When
        result = await mock_service.generate_content(
            business_info=business_info,
            content_type="blog"
        )
        
        # Then
        assert "blog_content" in result
        assert len(result["hashtags"]) > 0
        mock_service.generate_content.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_should_measure_model_performance(self):
        """모델 성능 측정 테스트"""
        # Given
        mock_service = AsyncMock(spec=AIService)
        mock_service.measure_performance.return_value = {
            "model_name": "gemma3:1b",
            "inference_time_ms": 1500,
            "memory_usage_mb": 2048,
            "tokens_per_second": 25.5
        }
        
        # When
        performance = await mock_service.measure_performance("gemma3:1b", "테스트 프롬프트")
        
        # Then
        assert performance["model_name"] == "gemma3:1b"
        assert performance["inference_time_ms"] > 0
        assert performance["memory_usage_mb"] > 0
        mock_service.measure_performance.assert_called_once()

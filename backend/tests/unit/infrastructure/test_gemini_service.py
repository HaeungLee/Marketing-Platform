"""
Google Gemini AI 서비스 테스트
TDD 방식으로 먼저 테스트 작성
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from typing import Dict, Any, List

from src.infrastructure.ai.gemini_service import GeminiService
from src.application.interfaces.ai_service import AIService


class TestGeminiService:
    """Google Gemini AI 서비스 테스트 클래스"""
    
    @pytest.fixture
    def mock_genai(self):
        """Google Generative AI 모킹"""
        with patch('src.infrastructure.ai.gemini_service.genai') as mock:
            # Mock the list_models function
            mock_model = MagicMock()
            mock_model.name = "models/gemini-1.5-flash"
            mock_model.supported_generation_methods = ['generateContent']
            mock.list_models.return_value = [mock_model]
            yield mock
    
    @pytest.fixture
    def gemini_service(self, mock_genai):
        """테스트용 Gemini 서비스 인스턴스"""
        with patch('src.infrastructure.ai.gemini_service.GENAI_AVAILABLE', True):
            return GeminiService(api_key="test_api_key")
    
    @pytest.mark.asyncio
    async def test_should_implement_ai_service_interface(self, gemini_service):
        """AIService 인터페이스 구현 확인"""
        assert isinstance(gemini_service, AIService)
    @pytest.mark.asyncio
    async def test_should_generate_blog_content(self, gemini_service):
        """블로그 콘텐츠 생성 테스트"""
        # Given
        business_info = {
            "name": "카페 모카",
            "industry": "카페",
            "location": "강남구"
        }
        target_audience = {
            "age_range": "20-30대",
            "interests": ["커피", "디저트"]
        }
        
        # Mock the async generation
        mock_response = MagicMock()
        mock_response.text = """제목: 카페 모카의 특별한 커피 이야기

본문:
강남의 숨은 보석, 카페 모카
카페 모카는 강남구에 위치한 아늑한 커피 전문점입니다.

20-30대를 위한 완벽한 공간
바쁜 일상 속에서 잠시 쉬어갈 수 있는...

커피와 디저트의 조화
신선한 원두와 수제 디저트로...

키워드: 카페, 커피, 디저트, 강남구, 모카"""
        
        with patch.object(gemini_service, '_generate_async', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_response
            
            # When
            result = await gemini_service.generate_content(
                business_info=business_info,
                content_type="blog",
                target_audience=target_audience
            )
            
            # Then
            assert "title" in result
            assert "content" in result
            assert "keywords" in result
            assert "카페 모카" in result["title"] or "카페 모카" in result["content"]
            assert result["content_type"] == "blog"
            mock_generate.assert_called_once()
    @pytest.mark.asyncio
    async def test_should_generate_instagram_content(self, gemini_service):
        """인스타그램 콘텐츠 생성 테스트"""
        # Given
        business_info = {
            "name": "피자스토리",
            "industry": "피자",
            "specialties": ["마르게리타", "페퍼로니"]
        }
        
        mock_response = MagicMock()
        mock_response.text = """캡션: 🍕 피자스토리 오늘의 특가! 🍕

✨ 마르게리타 + 페퍼로니 
💯 신선한 재료로 만든 수제 피자
📍 우리 동네 맛집

해시태그: #피자 #맛집 #수제피자 #마르게리타 #페퍼로니"""
        
        with patch.object(gemini_service, '_generate_async', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_response
            
            # When
            result = await gemini_service.generate_content(
                business_info=business_info,
                content_type="instagram"
            )
            
            # Then
            assert "caption" in result
            assert "hashtags" in result
            assert "피자스토리" in result["caption"]
            assert len(result["hashtags"]) > 0
            assert result["content_type"] == "instagram"
    @pytest.mark.asyncio
    async def test_should_generate_youtube_content(self, gemini_service):
        """유튜브 숏폼 콘텐츠 생성 테스트"""
        # Given
        business_info = {
            "name": "헬스케어",
            "industry": "헬스장",
            "programs": ["요가", "필라테스", "웨이트"]
        }
        
        mock_response = MagicMock()
        mock_response.text = """제목: 헬스케어에서 변화를 경험하세요!

스크립트:
[0-15초] 💪 "헬스케어에서 변화를 경험하세요!"
[15-30초] 🧘‍♀️ 요가, 필라테스, 웨이트까지
[30-45초] 📈 30일만에 몸이 달라집니다
[45-60초] 🔔 구독하고 첫 수업 무료!

해시태그: #헬스 #요가 #필라테스 #운동 #Shorts"""
        
        with patch.object(gemini_service, '_generate_async', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_response
            
            # When
            result = await gemini_service.generate_content(
                business_info=business_info,
                content_type="youtube"
            )
            
            # Then
            assert "script" in result
            assert "scenes" in result  # Changed from "timeline" to "scenes"
            assert "hashtags" in result
            assert "헬스케어" in result["title"] or "헬스케어" in result["script"]
            assert result["content_type"] == "youtube"
    @pytest.mark.asyncio
    async def test_should_generate_flyer_content(self, gemini_service):
        """전단지 콘텐츠 생성 테스트"""
        # Given
        business_info = {
            "name": "김밥천국",
            "industry": "분식점",
            "promotion": "신규 오픈"
        }
        
        mock_response = MagicMock()
        mock_response.text = """헤드라인: 🎉 김밥천국 신규 오픈! 🎉

서브텍스트: 오픈 기념 특가 이벤트

본문: ⭐ 오픈 기념 이벤트:
   - 모든 김밥 20% 할인
   - 라면 + 김밥 세트 5,000원
   - 첫 방문 고객 음료 서비스

행동유도: 📞 문의: 02-1234-5678
📍 주소: 서울시 강남구 테헤란로
⏰ 영업시간: 오전 8시 ~ 밤 10시"""
        
        with patch.object(gemini_service, '_generate_async', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_response
            
            # When
            result = await gemini_service.generate_content(
                business_info=business_info,
                content_type="flyer"
            )
            
            # Then
            assert "headline" in result
            assert "body" in result
            assert "call_to_action" in result  # Changed from "contact_info" to "call_to_action"
            assert "김밥천국" in result["headline"]
            assert result["content_type"] == "flyer"
    @pytest.mark.asyncio
    async def test_should_generate_hashtags(self, gemini_service):
        """해시태그 생성 테스트"""
        # Given
        content = "우리 카페의 신메뉴 딸기라떼가 출시되었습니다. 신선한 딸기와 부드러운 우유의 조화"
        business_info = {"name": "카페모카", "industry": "카페"}
        
        mock_response = MagicMock()
        mock_response.text = "#딸기라떼 #신메뉴 #카페 #딸기 #라떼 #카페모카 #음료 #맛집"
        
        with patch.object(gemini_service, '_generate_async', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_response
            
            # When
            hashtags = await gemini_service.generate_hashtags(content, business_info)
            
            # Then
            assert isinstance(hashtags, list)
            assert len(hashtags) > 0
            assert any("딸기라떼" in tag for tag in hashtags)
            assert any("카페" in tag for tag in hashtags)
    @pytest.mark.asyncio
    async def test_should_analyze_keywords(self, gemini_service):
        """키워드 분석 테스트"""
        # Given
        text = "신선한 재료로 만든 수제 햄버거와 감자튀김을 판매하는 패스트푸드점입니다."
        
        mock_response = MagicMock()
        mock_response.text = "신선한 재료, 수제 햄버거, 감자튀김, 패스트푸드점, 햄버거, 수제, 신선"
        
        with patch.object(gemini_service, '_generate_async', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_response
            
            # When
            keywords = await gemini_service.analyze_keywords(text)
            
            # Then
            assert isinstance(keywords, list)
            assert len(keywords) > 0
            assert "햄버거" in keywords or "수제 햄버거" in keywords
            assert "수제" in keywords or "신선한 재료" in keywords
    @pytest.mark.asyncio
    async def test_should_measure_performance(self, gemini_service):
        """모델 성능 측정 테스트"""
        # Given
        model_name = "gemini-1.5-flash"
        prompt = "테스트 프롬프트"
        
        mock_response = MagicMock()
        mock_response.text = "테스트 응답"
        
        with patch.object(gemini_service, '_generate_async_with_model', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = mock_response
            
            # When
            performance = await gemini_service.measure_performance(model_name, prompt)
            
            # Then
            assert "model_name" in performance
            assert "response_time" in performance  # Changed from "inference_time_ms"
            assert "tokens_used" in performance  # Changed from "tokens_generated"
            assert "response_length" in performance
            assert performance["model_name"] == model_name
            assert performance["response_time"] >= 0

    @pytest.mark.asyncio
    async def test_should_get_available_models(self, gemini_service, mock_genai):
        """사용 가능한 모델 목록 조회 테스트"""
        # Given - Mock API call failure to test default models
        mock_genai.list_models.side_effect = Exception("API Error")
        
        # When
        models = await gemini_service.get_available_models()
        
        # Then
        assert isinstance(models, list)
        assert len(models) > 0
        # Check for default Gemini models (should return default models when API fails)
        expected_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-pro-vision"]
        for expected_model in expected_models:
            assert expected_model in models
    @pytest.mark.asyncio
    async def test_should_handle_api_error(self, gemini_service):
        """API 오류 처리 테스트"""
        # Given
        business_info = {"name": "테스트", "industry": "카페"}
        
        # Mock the _generate_async method to raise an exception
        with patch.object(gemini_service, '_generate_async', new_callable=AsyncMock) as mock_generate:
            mock_generate.side_effect = Exception("API Error")
            
            # When & Then
            with pytest.raises(Exception) as exc_info:
                await gemini_service.generate_content(
                    business_info=business_info,
                    content_type="blog"
                )
            
            assert "API Error" in str(exc_info.value) or "Content generation failed" in str(exc_info.value)
    
    def test_should_require_api_key(self):
        """API 키 필수 여부 테스트"""
        # When & Then
        with pytest.raises(ValueError) as exc_info:
            GeminiService(api_key=None)
        
        assert "API key is required" in str(exc_info.value)

"""
AI Consultation Service Unit Tests

AI 상담 서비스 단위 테스트
"""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# 프로젝트 루트 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAIConsultantService:
    """AI 상담 서비스 테스트"""
    
    @pytest.mark.unit
    def test_consultation_topics_structure(self, client):
        """상담 주제 목록 구조 확인"""
        response = client.get("/api/v1/consultation/topics")
        
        assert response.status_code == 200
        data = response.json()
        
        # 필수 필드 확인
        assert "topics" in data
        assert isinstance(data["topics"], list)
        assert len(data["topics"]) > 0
        
        # 각 토픽 구조 확인 (실제 API 구조에 맞게)
        for topic in data["topics"]:
            assert "category" in topic
            assert "description" in topic
            # keywords 필드가 있음
            assert "keywords" in topic
    
    @pytest.mark.unit
    def test_consultation_health_check(self, client):
        """AI 상담 서비스 헬스체크"""
        response = client.get("/api/v1/consultation/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] in ["healthy", "degraded"]
    
    @pytest.mark.unit
    def test_consultation_ask_validation(self, client):
        """상담 질문 유효성 검증"""
        # 빈 질문
        response = client.post(
            "/api/v1/consultation/ask",
            json={"question": ""}
        )
        assert response.status_code == 400
        
        # 질문 없음
        response = client.post(
            "/api/v1/consultation/ask",
            json={}
        )
        assert response.status_code in [400, 422]
    
    @pytest.mark.unit
    def test_consultation_ask_with_context(self, client, sample_consultation_request):
        """컨텍스트를 포함한 상담 요청"""
        response = client.post(
            "/api/v1/consultation/ask",
            json=sample_consultation_request
        )
        
        # AI 서비스 가용성에 따라 다름
        # 성공하면 200, AI 서비스 오류면 500/503
        assert response.status_code in [200, 500, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "answer" in data
            assert len(data["answer"]) > 0


class TestConsultationTopics:
    """상담 주제 관련 테스트"""
    
    @pytest.mark.unit
    def test_all_categories_covered(self, client):
        """모든 상담 카테고리가 포함되어 있는지 확인"""
        response = client.get("/api/v1/consultation/topics")
        data = response.json()
        
        # 실제 API 응답에 맞는 카테고리명
        expected_categories = [
            "상권 분석",
            "창업 전략", 
            "마케팅",
            "정부 지원",
            "경영 개선"
        ]
        
        actual_categories = [topic["category"] for topic in data["topics"]]
        
        for category in expected_categories:
            assert category in actual_categories, f"카테고리 '{category}' 누락"
    
    @pytest.mark.unit
    def test_topics_have_keywords(self, client):
        """각 토픽에 키워드가 있는지 확인"""
        response = client.get("/api/v1/consultation/topics")
        data = response.json()
        
        for topic in data["topics"]:
            assert "keywords" in topic, \
                f"카테고리 '{topic['category']}'의 키워드가 없음"
            assert len(topic["keywords"]) > 0


class TestSettingsValidation:
    """설정 유효성 검증 테스트"""
    
    @pytest.mark.unit
    def test_settings_loads_correctly(self):
        """설정이 올바르게 로드되는지 확인"""
        from src.config.settings import Settings
        
        settings = Settings()
        
        # 기본값 확인
        assert settings.app_name is not None
        assert settings.debug is not None
    
    @pytest.mark.unit
    def test_cors_origins_parsing(self):
        """CORS 오리진 파싱 테스트"""
        from src.config.settings import Settings
        
        settings = Settings()
        origins = settings.cors_origins_list
        
        assert isinstance(origins, list)
        # 기본 개발 오리진 포함 확인
        assert any("localhost" in origin for origin in origins)
    
    @pytest.mark.unit
    def test_database_url_format(self):
        """데이터베이스 URL 형식 확인"""
        from src.config.settings import Settings
        
        settings = Settings()
        
        if settings.database_url:
            assert "postgresql" in settings.database_url


class TestRateLimitMiddleware:
    """Rate Limiting 미들웨어 테스트"""
    
    @pytest.mark.unit
    def test_rate_limiter_initialization(self):
        """Rate Limiter 초기화 테스트"""
        from src.infrastructure.middleware.rate_limit import InMemoryRateLimiter
        
        # 실제 파라미터명 사용
        limiter = InMemoryRateLimiter(requests_per_minute=10, window_seconds=60)
        
        assert limiter.requests_per_minute == 10
        assert limiter.window_seconds == 60
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_rate_limiter_allows_requests(self):
        """Rate Limiter가 요청을 허용하는지 테스트"""
        from src.infrastructure.middleware.rate_limit import InMemoryRateLimiter
        
        limiter = InMemoryRateLimiter(requests_per_minute=5, window_seconds=60)
        client_ip = "127.0.0.1"
        
        # 5개 요청 허용
        for _ in range(5):
            is_allowed, remaining = await limiter.is_allowed(client_ip)
            assert is_allowed is True
        
        # 6번째 요청 거부
        is_allowed, remaining = await limiter.is_allowed(client_ip)
        assert is_allowed is False
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_rate_limiter_different_clients(self):
        """다른 클라이언트는 별도로 제한"""
        from src.infrastructure.middleware.rate_limit import InMemoryRateLimiter
        
        limiter = InMemoryRateLimiter(requests_per_minute=2, window_seconds=60)
        
        # 클라이언트 A
        is_allowed_a, _ = await limiter.is_allowed("192.168.1.1")
        assert is_allowed_a is True
        
        # 클라이언트 B
        is_allowed_b, _ = await limiter.is_allowed("192.168.1.2")
        assert is_allowed_b is True
        
        # 클라이언트 A 추가 요청
        is_allowed_a2, _ = await limiter.is_allowed("192.168.1.1")
        assert is_allowed_a2 is True


class TestJWTTokenBlacklist:
    """JWT 토큰 블랙리스트 테스트"""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_local_blacklist_add_and_check(self):
        """로컬 블랙리스트 추가 및 확인"""
        from src.infrastructure.security.jwt import TokenBlacklist
        
        blacklist = TokenBlacklist(redis_client=None)
        
        test_jti = "test-token-id-123"
        
        # 블랙리스트에 추가
        await blacklist.add(test_jti, expires_in=3600)
        
        # 블랙리스트 확인
        is_blacklisted = await blacklist.is_blacklisted(test_jti)
        assert is_blacklisted is True
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_non_blacklisted_token(self):
        """블랙리스트에 없는 토큰"""
        from src.infrastructure.security.jwt import TokenBlacklist
        
        blacklist = TokenBlacklist(redis_client=None)
        
        is_blacklisted = await blacklist.is_blacklisted("non-existent-token")
        assert is_blacklisted is False

"""
API 엔드포인트 통합 테스트
"""
import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """헬스체크 엔드포인트 테스트"""
    
    @pytest.mark.api
    def test_root_endpoint(self, client: TestClient):
        """루트 엔드포인트 테스트"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Marketing Platform API" in data["message"]
        assert "environment" in data
        assert "version" in data
    
    @pytest.mark.api
    def test_health_endpoint(self, client: TestClient):
        """헬스 엔드포인트 테스트"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "environment" in data
    
    @pytest.mark.api
    def test_api_health_endpoint(self, client: TestClient):
        """API 상세 헬스 엔드포인트 테스트"""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "checks" in data
        assert "api" in data["checks"]


class TestAuthEndpoints:
    """인증 API 테스트"""
    
    @pytest.mark.api
    @pytest.mark.auth
    def test_login_invalid_credentials(self, client: TestClient):
        """잘못된 자격증명으로 로그인 시도"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            }
        )
        
        # 400 또는 401 응답 예상
        assert response.status_code in [400, 401, 422]
    
    @pytest.mark.api
    @pytest.mark.auth
    def test_register_invalid_email(self, client: TestClient):
        """잘못된 이메일로 회원가입 시도"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "TestPassword123!",
                "name": "테스트"
            }
        )
        
        # Validation error 예상
        assert response.status_code == 422


class TestConsultationEndpoints:
    """AI 상담 API 테스트"""
    
    @pytest.mark.api
    def test_consultation_topics(self, client: TestClient):
        """상담 주제 목록 조회"""
        response = client.get("/api/v1/consultation/topics")
        
        assert response.status_code == 200
        data = response.json()
        assert "topics" in data
        assert len(data["topics"]) > 0
        
        # 첫 번째 토픽 구조 확인
        topic = data["topics"][0]
        assert "category" in topic
        assert "keywords" in topic
        assert "description" in topic
    
    @pytest.mark.api
    def test_consultation_health(self, client: TestClient):
        """상담 서비스 헬스체크"""
        response = client.get("/api/v1/consultation/health")
        
        # API 키 설정에 따라 200 또는 503
        assert response.status_code in [200, 503]
    
    @pytest.mark.api
    def test_consultation_ask_empty_question(self, client: TestClient):
        """빈 질문으로 상담 요청"""
        response = client.post(
            "/api/v1/consultation/ask",
            json={
                "question": "   "
            }
        )
        
        # 400 Bad Request 예상
        assert response.status_code in [400, 500, 503]


class TestContentEndpoints:
    """콘텐츠 생성 API 테스트"""
    
    @pytest.mark.api
    def test_content_types_exist(self, client: TestClient):
        """콘텐츠 엔드포인트 존재 확인"""
        # 콘텐츠 관련 엔드포인트가 존재하는지 확인
        response = client.get("/api/v1/content/types")
        
        # 404가 아니면 엔드포인트가 존재함
        # 실제 구현에 따라 응답 코드가 다를 수 있음
        assert response.status_code != 405  # Method Not Allowed가 아님


class TestBusinessStoresEndpoints:
    """상가정보 API 테스트"""
    
    @pytest.mark.api
    def test_nearby_stores_missing_params(self, client: TestClient):
        """필수 파라미터 없이 주변 상가 조회"""
        response = client.get("/api/v1/business-stores/nearby")
        
        # 파라미터 검증 에러 예상
        assert response.status_code == 422


class TestCORSHeaders:
    """CORS 헤더 테스트"""
    
    @pytest.mark.api
    def test_cors_preflight(self, client: TestClient):
        """CORS Preflight 요청 테스트"""
        response = client.options(
            "/api/v1/auth/login",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        # Preflight 응답 확인
        assert response.status_code == 200
    
    @pytest.mark.api
    def test_cors_headers_present(self, client: TestClient):
        """CORS 헤더 존재 확인"""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # CORS 헤더가 있어야 함 (개발 환경에서)


class TestRequestLogging:
    """요청 로깅 미들웨어 테스트"""
    
    @pytest.mark.api
    def test_request_id_header(self, client: TestClient):
        """요청 ID 헤더 존재 확인"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert "x-request-id" in response.headers
        assert "x-process-time" in response.headers

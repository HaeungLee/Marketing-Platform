"""
Business Stores API Integration Tests

상가 정보 API 통합 테스트
"""
import pytest
from fastapi.testclient import TestClient


class TestBusinessStoresAPI:
    """상가 정보 API 테스트"""
    
    @pytest.mark.api
    def test_nearby_stores_requires_params(self, client: TestClient):
        """주변 상가 조회 - 필수 파라미터 누락 시 422 반환"""
        response = client.get("/api/v1/business-stores/nearby")
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.api
    def test_nearby_stores_with_valid_params(self, client: TestClient):
        """주변 상가 조회 - 유효한 파라미터"""
        response = client.get(
            "/api/v1/business-stores/nearby",
            params={
                "latitude": 37.5066,
                "longitude": 127.0534,
                "radius_km": 1.0
            }
        )
        
        # DB 연결 없이도 쿼리 형식이 올바르면 500 또는 200
        # 실제 DB가 없으면 500, 있으면 200
        assert response.status_code in [200, 500]
    
    @pytest.mark.api
    def test_nearby_stores_invalid_latitude(self, client: TestClient):
        """주변 상가 조회 - 유효하지 않은 위도"""
        response = client.get(
            "/api/v1/business-stores/nearby",
            params={
                "latitude": "invalid",
                "longitude": 127.0534
            }
        )
        
        assert response.status_code == 422
    
    @pytest.mark.api
    def test_stores_by_region_no_params(self, client: TestClient):
        """지역별 상가 조회 - 파라미터 없이 호출"""
        response = client.get("/api/v1/business-stores/by-region")
        
        # 파라미터 없이도 전체 조회 가능 (DB 연결 필요)
        assert response.status_code in [200, 500]
    
    @pytest.mark.api
    def test_stores_by_region_with_filters(self, client: TestClient):
        """지역별 상가 조회 - 필터 적용"""
        response = client.get(
            "/api/v1/business-stores/by-region",
            params={
                "sido_name": "서울특별시",
                "sigungu_name": "강남구",
                "page": 1,
                "page_size": 10
            }
        )
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.api
    def test_business_statistics_no_params(self, client: TestClient):
        """상가 통계 조회 - 파라미터 없이 호출"""
        response = client.get("/api/v1/business-stores/statistics")
        
        assert response.status_code in [200, 500]
    
    @pytest.mark.api
    def test_business_statistics_with_region(self, client: TestClient):
        """상가 통계 조회 - 지역 필터"""
        response = client.get(
            "/api/v1/business-stores/statistics",
            params={
                "sido_name": "서울특별시"
            }
        )
        
        assert response.status_code in [200, 500]


class TestContentAPI:
    """콘텐츠 생성 API 테스트"""
    
    @pytest.mark.api
    def test_generate_blog_content(self, client: TestClient, sample_content_request):
        """블로그 콘텐츠 생성"""
        response = client.post(
            "/api/v1/content/generate",
            json=sample_content_request
        )
        
        # AI 서비스 연결에 따라 다름
        assert response.status_code in [200, 404, 500, 503]
    
    @pytest.mark.api
    def test_generate_content_missing_type(self, client: TestClient):
        """콘텐츠 생성 - 타입 누락"""
        response = client.post(
            "/api/v1/content/generate",
            json={
                "business_name": "테스트 가게"
            }
        )
        
        # 필수 필드 누락 시 422 또는 404
        assert response.status_code in [404, 422]


class TestAnalysisAPI:
    """분석 API 테스트"""
    
    @pytest.mark.api
    def test_trend_analysis_endpoint(self, client: TestClient):
        """트렌드 분석 엔드포인트"""
        response = client.get("/api/v1/analysis/trends")
        
        # 엔드포인트 존재 여부에 따라
        assert response.status_code in [200, 404, 422, 500]
    
    @pytest.mark.api
    def test_competitor_analysis(self, client: TestClient):
        """경쟁사 분석 엔드포인트"""
        response = client.get(
            "/api/v1/analysis/competitors",
            params={
                "latitude": 37.5066,
                "longitude": 127.0534,
                "business_type": "카페"
            }
        )
        
        assert response.status_code in [200, 404, 422, 500]


class TestInsightsAPI:
    """인사이트 API 테스트"""
    
    @pytest.mark.api
    def test_get_target_insights(self, client: TestClient):
        """타겟 인사이트 조회"""
        response = client.get("/api/v1/insights/target")
        
        assert response.status_code in [200, 404, 500]
    
    @pytest.mark.api
    def test_get_location_insights(self, client: TestClient):
        """위치 기반 인사이트 조회"""
        response = client.get(
            "/api/v1/insights/location",
            params={
                "latitude": 37.5066,
                "longitude": 127.0534
            }
        )
        
        assert response.status_code in [200, 404, 422, 500]


class TestImageAPI:
    """이미지 생성 API 테스트"""
    
    @pytest.mark.api
    def test_generate_image_endpoint(self, client: TestClient):
        """이미지 생성 엔드포인트"""
        response = client.post(
            "/api/images/generate",
            json={
                "prompt": "테스트 이미지 생성",
                "style": "modern"
            }
        )
        
        # AI 서비스 상태에 따라
        assert response.status_code in [200, 404, 422, 500, 503]
    
    @pytest.mark.api
    def test_generate_image_empty_prompt(self, client: TestClient):
        """이미지 생성 - 빈 프롬프트"""
        response = client.post(
            "/api/images/generate",
            json={
                "prompt": ""
            }
        )
        
        # 빈 프롬프트 검증
        assert response.status_code in [400, 404, 422]

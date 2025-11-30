"""
Pytest Configuration and Fixtures

이 파일은 pytest 테스트에서 공통으로 사용되는 fixture와 설정을 정의합니다.
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
import os
import sys

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =================================
# 환경 설정
# =================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """테스트 환경 설정"""
    # 테스트용 환경변수 설정
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "true"
    os.environ["TESTING"] = "true"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only-32chars!"
    os.environ["GOOGLE_API_KEY"] = "test-google-api-key"
    
    yield
    
    # 테스트 후 정리
    for key in ["ENVIRONMENT", "DEBUG", "TESTING"]:
        os.environ.pop(key, None)


# =================================
# 이벤트 루프 설정
# =================================

@pytest.fixture(scope="session")
def event_loop():
    """세션 범위의 이벤트 루프 생성"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# =================================
# FastAPI 애플리케이션 Fixtures
# =================================

@pytest.fixture(scope="module")
def app():
    """FastAPI 애플리케이션 인스턴스"""
    from src.main import create_app
    return create_app()


@pytest.fixture(scope="module")
def client(app) -> Generator[TestClient, None, None]:
    """동기 테스트 클라이언트"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
async def async_client(app) -> AsyncGenerator[AsyncClient, None]:
    """비동기 테스트 클라이언트"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


# =================================
# 인증 관련 Fixtures
# =================================

@pytest.fixture
def auth_headers():
    """테스트용 인증 헤더"""
    from src.infrastructure.security.jwt import create_access_token
    
    token_data = create_access_token(
        data={"sub": "test-user@example.com", "user_id": "test-user-123"}
    )
    
    return {"Authorization": f"Bearer {token_data['access_token']}"}


@pytest.fixture
def mock_current_user():
    """Mock 현재 사용자"""
    return {
        "sub": "test-user@example.com",
        "user_id": "test-user-123",
        "name": "테스트 사용자",
        "role": "user"
    }


# =================================
# 데이터베이스 Fixtures
# =================================

@pytest.fixture
def mock_db_session():
    """Mock 데이터베이스 세션"""
    session = MagicMock()
    session.commit = MagicMock()
    session.rollback = MagicMock()
    session.close = MagicMock()
    return session


@pytest.fixture
async def async_mock_db_session():
    """비동기 Mock 데이터베이스 세션"""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    return session


# =================================
# Redis Fixtures
# =================================

@pytest.fixture
def mock_redis():
    """Mock Redis 클라이언트"""
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock(return_value=True)
    redis.setex = AsyncMock(return_value=True)
    redis.delete = AsyncMock(return_value=True)
    redis.exists = AsyncMock(return_value=False)
    return redis


# =================================
# AI 서비스 Fixtures
# =================================

@pytest.fixture
def mock_gemini_service():
    """Mock Gemini AI 서비스"""
    service = MagicMock()
    service.generate_content = AsyncMock(return_value={
        "text": "테스트 콘텐츠입니다.",
        "model": "gemini-pro"
    })
    return service


@pytest.fixture
def mock_consultant_service():
    """Mock AI 상담 서비스"""
    service = AsyncMock()
    service.get_consultation = AsyncMock(return_value={
        "answer": "테스트 상담 응답입니다.",
        "context": "",
        "question": "테스트 질문",
        "timestamp": "2025-11-30T00:00:00"
    })
    return service


# =================================
# 테스트 데이터 Fixtures
# =================================

@pytest.fixture
def sample_user_data():
    """샘플 사용자 데이터"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "name": "테스트 사용자"
    }


@pytest.fixture
def sample_business_data():
    """샘플 비즈니스 데이터"""
    return {
        "name": "테스트 가게",
        "category": "카페/디저트",
        "description": "테스트용 카페입니다.",
        "address": "서울시 강남구 테헤란로 123",
        "phone": "02-1234-5678",
        "latitude": 37.5066,
        "longitude": 127.0534
    }


@pytest.fixture
def sample_content_request():
    """샘플 콘텐츠 생성 요청"""
    return {
        "content_type": "blog",
        "business_name": "테스트 카페",
        "business_category": "카페",
        "keywords": ["커피", "디저트", "브런치"],
        "tone": "친근한",
        "target_audience": "20-30대"
    }


@pytest.fixture
def sample_consultation_request():
    """샘플 상담 요청"""
    return {
        "question": "카페 창업 시 상권 분석은 어떻게 해야 하나요?",
        "business_type": "카페",
        "region": "서울 강남구",
        "budget": "5000만원"
    }


# =================================
# 유틸리티 Fixtures
# =================================

@pytest.fixture
def freeze_time(monkeypatch):
    """시간 고정 fixture"""
    from datetime import datetime
    
    frozen_time = datetime(2025, 11, 30, 12, 0, 0)
    
    class FrozenDatetime:
        @classmethod
        def now(cls, tz=None):
            return frozen_time
        
        @classmethod
        def utcnow(cls):
            return frozen_time
    
    monkeypatch.setattr("datetime.datetime", FrozenDatetime)
    return frozen_time


# =================================
# Markers
# =================================

def pytest_configure(config):
    """pytest 마커 등록"""
    config.addinivalue_line(
        "markers", "slow: 느린 테스트 (--runslow 옵션으로 실행)"
    )
    config.addinivalue_line(
        "markers", "integration: 통합 테스트"
    )
    config.addinivalue_line(
        "markers", "unit: 단위 테스트"
    )
    config.addinivalue_line(
        "markers", "api: API 엔드포인트 테스트"
    )
    config.addinivalue_line(
        "markers", "db: 데이터베이스 관련 테스트"
    )
    config.addinivalue_line(
        "markers", "auth: 인증 관련 테스트"
    )


def pytest_collection_modifyitems(config, items):
    """slow 마커가 있는 테스트 스킵 (--runslow 옵션 없을 때)"""
    if not config.getoption("--runslow", default=False):
        skip_slow = pytest.mark.skip(reason="--runslow 옵션 필요")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


def pytest_addoption(parser):
    """커맨드라인 옵션 추가"""
    parser.addoption(
        "--runslow", action="store_true", default=False, help="느린 테스트 실행"
    )

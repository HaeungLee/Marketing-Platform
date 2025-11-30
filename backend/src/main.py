#!/usr/bin/env python3
"""
Main FastAPI application module following Clean Architecture principles.

보안 개선사항:
- CORS 설정을 환경변수 기반으로 변경
- 프로덕션/개발 환경 분리
- Rate Limiting 미들웨어 추가
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import logging
import time

from src.config.settings import settings
from src.infrastructure.middleware.rate_limit import RateLimitMiddleware

# API 라우터 임포트
from src.presentation.api.v1.auth import router as auth_router
from src.presentation.api.v1.business import router as business_router
from src.presentation.api.v1.content import router as content_router
from src.presentation.api.v1.analysis import router as analysis_router
from src.presentation.api.v1.insights import router as insights_router
from src.presentation.api.v1.consultation import router as consultation_router
from src.presentation.api.population import router as population_router
from src.presentation.api.image_router import router as image_router
from src.presentation.api.v1.business_stores import router as business_stores_router

# 로깅 설정
logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Factory function that creates and configures the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="Marketing Platform API",
        description="Marketing Platform backend API service",
        version="0.1.0",
        docs_url="/docs" if settings.is_development else None,  # 프로덕션에서 docs 비활성화 (선택적)
        redoc_url="/redoc" if settings.is_development else None,
    )
    
    # =================================
    # CORS 설정 (환경변수 기반)
    # =================================
    # 프로덕션에서는 명시적 도메인만 허용
    cors_origins = settings.cors_origins_list
    
    # 개발 환경에서 추가 허용
    if settings.is_development:
        development_origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",  # Vite dev server
            "http://127.0.0.1:5173",
            "http://localhost:8000",
        ]
        cors_origins = list(set(cors_origins + development_origins))
    
    logger.info(f"CORS Origins: {cors_origins}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Content-Type", 
            "Authorization", 
            "Accept", 
            "Origin", 
            "X-Requested-With",
            "X-Request-ID",
        ],
        expose_headers=[
            "Content-Length", 
            "Content-Type", 
            "X-Request-ID",
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
        ],
        max_age=600,  # Preflight 캐시 시간 (초)
    )
    
    # =================================
    # Rate Limiting 미들웨어
    # =================================
    if settings.rate_limit_enabled:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=settings.rate_limit_requests,
            window_seconds=settings.rate_limit_window,
            redis_client=None,  # TODO: Redis 연결 시 추가
            exclude_paths=["/health", "/docs", "/redoc", "/openapi.json", "/static"],
            enabled=settings.rate_limit_enabled
        )
        logger.info(f"Rate limiting enabled: {settings.rate_limit_requests} req/{settings.rate_limit_window}s")
    
    # =================================
    # 요청 로깅 미들웨어
    # =================================
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        # 요청 ID 생성
        import secrets
        request_id = secrets.token_urlsafe(8)
        
        # 요청 로깅
        logger.info(f"[{request_id}] {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # 응답 시간 계산
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        
        # 응답 로깅
        logger.info(f"[{request_id}] Completed in {process_time:.3f}s - Status: {response.status_code}")
        
        return response
    
    # =================================
    # 전역 예외 핸들러
    # =================================
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        # 프로덕션에서는 상세 에러 숨김
        if settings.is_production:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"detail": str(exc), "type": type(exc).__name__}
            )
    
    # =================================
    # 정적 파일 서빙
    # =================================
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
    os.makedirs(os.path.join(static_dir, "images"), exist_ok=True)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # =================================
    # 헬스체크 엔드포인트
    # =================================
    @app.get("/")
    async def root():
        return {
            "message": "Marketing Platform API is running",
            "environment": settings.environment,
            "version": "0.1.0"
        }
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "environment": settings.environment,
            "debug": settings.debug
        }
    
    @app.get("/api/health")
    async def api_health_check():
        """API 상세 헬스체크"""
        health_status = {
            "status": "healthy",
            "checks": {
                "api": True,
                "database": False,
                "redis": False,
            }
        }
        
        # 데이터베이스 연결 확인 (선택적)
        try:
            # TODO: 실제 DB 연결 확인 로직 추가
            health_status["checks"]["database"] = True
        except Exception as e:
            logger.warning(f"Database health check failed: {e}")
        
        # Redis 연결 확인 (선택적)
        try:
            # TODO: 실제 Redis 연결 확인 로직 추가
            health_status["checks"]["redis"] = True
        except Exception as e:
            logger.warning(f"Redis health check failed: {e}")
        
        # 전체 상태 결정
        if not all(health_status["checks"].values()):
            health_status["status"] = "degraded"
        
        return health_status
    
    # =================================
    # API 라우터 등록
    # =================================
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["인증"])
    app.include_router(business_router, prefix="/api/v1", tags=["비즈니스"])
    app.include_router(content_router, prefix="/api/v1/content", tags=["콘텐츠"])
    app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["분석"])
    app.include_router(insights_router, prefix="/api/v1", tags=["인사이트"])
    app.include_router(consultation_router, prefix="/api/v1", tags=["AI 상담"])
    app.include_router(population_router, prefix="/api/v1/population", tags=["인구통계"])
    app.include_router(business_stores_router, prefix="/api/v1/business-stores", tags=["상가정보"])
    app.include_router(image_router)  # image_router는 이미 prefix가 설정되어 있음
    
    # 시작 로그
    logger.info(f"Application started in {settings.environment} mode")
    if settings.debug:
        logger.warning("Debug mode is enabled - not recommended for production")
    
    return app


# For compatibility with direct imports (like in start_server.py)
app = create_app()
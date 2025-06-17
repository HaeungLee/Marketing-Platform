#!/usr/bin/env python3
"""
Main FastAPI application module following Clean Architecture principles.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging

# API 라우터 임포트
from src.presentation.api.v1.auth import router as auth_router
from src.presentation.api.v1.business import router as business_router
from src.presentation.api.v1.content import router as content_router
from src.presentation.api.v1.analysis import router as analysis_router
from src.presentation.api.v1.insights import router as insights_router
from src.presentation.api.population import router as population_router
from src.presentation.api.image_router import router as image_router
from src.presentation.api.v1.business_stores import router as business_stores_router
# 테스트 라우터는 개발 환경에서만 필요할 경우 조건부로 임포트
# from src.presentation.api.v1.test import router as test_router

def create_app() -> FastAPI:
    """
    Factory function that creates and configures the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="Marketing Platform API",
        description="Marketing Platform backend API service",
        version="0.1.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000", 
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "https://localhost:3000",
            "https://127.0.0.1:3000",
            "*"  # 개발 환경에서는 모든 origin을 허용할 수 있지만, 프로덕션에서는 제거해야 함
        ],  # 프론트엔드 URL 명시적 지정
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
        expose_headers=["Content-Length", "Content-Type"],
    )
    
    # 정적 파일 서빙 (이미지 등)
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
    os.makedirs(os.path.join(static_dir, "images"), exist_ok=True)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/")
    async def root():
        return {"message": "Marketing Platform API is running"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
      # API 라우터 등록
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["인증"])
    app.include_router(business_router, prefix="/api/v1", tags=["비즈니스"])
    app.include_router(content_router, prefix="/api/v1/content", tags=["콘텐츠"])
    app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["분석"])
    app.include_router(insights_router, prefix="/api/v1", tags=["인사이트"])
    app.include_router(population_router, prefix="/api/v1/population", tags=["인구통계"])
    app.include_router(business_stores_router, prefix="/api/v1/business-stores", tags=["상가정보"])
    app.include_router(image_router)  # image_router는 이미 prefix가 설정되어 있음
    # 테스트 라우터는 개발 환경에서만 필요할 경우 조건부로 등록
    # app.include_router(test_router, prefix="/api/v1/test", tags=["테스트"])
    
    return app

# For compatibility with direct imports (like in start_server.py)
app = create_app()
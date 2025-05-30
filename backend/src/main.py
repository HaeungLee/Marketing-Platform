"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import settings
from presentation.api.v1 import auth, business, content, analysis
from infrastructure.ai.ollama_service import OllamaService


def create_app() -> FastAPI:
    """FastAPI 애플리케이션 생성"""
    app = FastAPI(
        title=settings.app_name,
        description="소상공인을 위한 AI 마케팅 플랫폼 API",
        version="1.0.0",
        debug=settings.debug
    )    # CORS 미들웨어 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 개발 환경에서는 모든 출처 허용
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # API 라우터 등록
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["인증"])
    app.include_router(business.router, prefix="/api/v1/business", tags=["비즈니스"])
    app.include_router(content.router, prefix="/api/v1/content", tags=["콘텐츠"])
    app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["분석"])
    
    # 글로벌 예외 처리
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error" if not settings.debug else str(exc),
                "type": "error"
            }
        )
    
    # 헬스 체크 엔드포인트
    @app.get("/health")
    async def health_check():
        """서버 상태 확인"""
        try:
            # Ollama 연결 확인
            ollama_service = OllamaService(settings.ollama_base_url)
            models = await ollama_service.get_available_models()
            await ollama_service.close()
            
            return {
                "status": "healthy",
                "version": "1.0.0",
                "ollama_models": models,
                "social_login_config": settings.is_social_login_configured
            }
        except Exception as e:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "error": str(e) if settings.debug else "Service unavailable"
                }
            )
    
    return app


# 애플리케이션 인스턴스
app = create_app()

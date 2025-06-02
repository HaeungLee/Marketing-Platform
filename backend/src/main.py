"""
FastAPI 메인 애플리케이션
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# 환경 변수 로드
load_dotenv()

from config.settings import settings
from presentation.api.v1 import auth, business, content, analysis
from infrastructure.ai.ollama_service import OllamaService
from infrastructure.monitoring.monitoring import MonitoringService, init_instrumentator

# 로깅 설정
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 글로벌 모니터링 서비스 인스턴스
monitoring_service = None


def create_app() -> FastAPI:
    """FastAPI 애플리케이션 생성"""
    app = FastAPI(
        title=settings.app_name,
        description="AI 마케팅 플랫폼 API",
        version="1.0.0",
        debug=settings.debug
    )

    # CORS 미들웨어 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Prometheus 메트릭 설정
    init_instrumentator(app)

    # 글로벌 변수 사용
    global monitoring_service

    # 모니터링 서비스 초기화
    monitoring_service = MonitoringService(
        app=app,
        discord_webhook_url=settings.discord_webhook_url
    )

    # 라우터 등록
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["인증"])
    app.include_router(business.router, prefix="/api/v1/business", tags=["비즈니스"])
    app.include_router(content.router, prefix="/api/v1/content", tags=["콘텐츠"])
    app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["분석"])

    @app.on_event("startup")
    async def startup_event():
        """애플리케이션 시작 시 실행되는 이벤트"""
        await monitoring_service.setup()
        logging.info("애플리케이션이 시작되었습니다.")
        logging.info(f"SendGrid API 키 설정 상태: {'설정됨' if settings.sendgrid_api_key else '설정되지 않음'}")
        logging.info(f"SMTP 사용자 설정 상태: {'설정됨' if settings.smtp_user else '설정되지 않음'}")

    @app.middleware("http")
    async def monitor_requests(request: Request, call_next):
        """HTTP 요청 모니터링 미들웨어"""
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # 에러 발생시 모니터링 서비스에 기록
            await monitoring_service.record_api_error(
                endpoint=request.url.path,
                error_type=type(e).__name__
            )
            raise

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

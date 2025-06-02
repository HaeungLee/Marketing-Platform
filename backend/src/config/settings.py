"""
애플리케이션 설정
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # 기본 설정
    app_name: str = "Marketing Platform API"
    debug: bool = True
    log_level: str = "INFO"
    
    # API URL 설정
    BASE_URL: str = "http://localhost:3000"
    
    # CORS 설정
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # 모니터링 설정
    discord_webhook_url: Optional[str] = None
    memory_threshold: int = 90
    cpu_threshold: int = 80
    error_threshold: int = 10
    
    # 구글 OAuth 설정
    google_client_id: str = "207390623047-cgtnd87rimflmcnrrhtal9k7u144ef8n.apps.googleusercontent.com"
    google_client_secret: str = "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"
    google_redirect_uri: str = "http://localhost:3000/auth/google/callback"

    # 카카오 OAuth 설정
    kakao_client_id: str = "58abcb4c758b2ac22d34496f4a506894"
    kakao_client_secret: str = "zWzdkvcAdZP0Se7WtJVMYE7GRa4pVToC"
    kakao_redirect_uri: str = "http://localhost:3000/auth/kakao/callback"

    # PostgreSQL 설정
    postgres_user: str = "postgres"
    postgres_password: str = "1234"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "marketing_platform"

    # PostgreSQL 연결 풀 설정
    mcp_min_connections: int = 5
    mcp_max_connections: int = 20
    mcp_pool_timeout: int = 30
    mcp_pool_recycle: int = 1800
    
    # 데이터베이스 URL (비동기)
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # 데이터베이스 URL (동기식)
    @property
    def sync_database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # Redis 설정
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT 설정
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # 외부 API 설정
    kakao_map_api_key: Optional[str] = None
    naver_client_id: Optional[str] = None
    naver_client_secret: Optional[str] = None
    kakao_client_id: Optional[str] = None
    google_client_id: Optional[str] = None
    google_api_key: Optional[str] = None  # Google Gemini API 키 추가
    
    # Ollama 설정
    ollama_base_url: str = "http://localhost:11434"
    ollama_models: str = "gemma3:1b"
    
    # 이메일 설정
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str= "sghnyyj@gmail.com"
    smtp_password: str = "ypai nsup rkxf pxem"
    
    # SendGrid 설정
    sendgrid_api_key: Optional[str] = None
    
    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/marketing_platform"
    
    # 이메일 설정
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
      # Redis 설정
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 정의되지 않은 환경변수 무시
    
    @property
    def is_social_login_configured(self) -> dict:
        """소셜 로그인 설정 상태 확인"""
        return {
            "google": bool(self.google_client_id),
            "naver": bool(self.naver_client_id and self.naver_client_secret),
            "kakao": bool(self.kakao_client_id)
        }


# 전역 설정 인스턴스
settings = Settings()

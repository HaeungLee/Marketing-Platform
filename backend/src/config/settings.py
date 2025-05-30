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
    
    # PostgreSQL 설정
    postgres_user: str = "postgres"
    postgres_password: str = "human1234"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "marketing_platform"
    
    # MCP 설정
    mcp_min_connections: int = 5
    mcp_max_connections: int = 20
    mcp_pool_timeout: int = 30
    mcp_pool_recycle: int = 1800
    
    # 데이터베이스 URL
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # Redis 설정
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT 설정
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS 설정
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # 외부 API 설정
    kakao_map_api_key: Optional[str] = None
    naver_client_id: Optional[str] = None
    naver_client_secret: Optional[str] = None
    kakao_client_id: Optional[str] = None
    google_client_id: Optional[str] = None
    
    # Ollama 설정
    ollama_base_url: str = "http://localhost:11434"
    ollama_models: str = "gemma3:1b"
    
    # 이메일 설정
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
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

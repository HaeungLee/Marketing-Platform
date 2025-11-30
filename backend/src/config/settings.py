"""
애플리케이션 설정

보안 주의사항:
- 모든 민감한 정보는 환경변수(.env)에서 관리됩니다
- 프로덕션 환경에서는 반드시 강력한 시크릿 키를 사용하세요
- .env 파일은 절대 Git에 커밋하지 마세요
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, field_validator
from typing import List, Optional
import os
import secrets


def generate_secret_key() -> str:
    """256비트의 안전한 랜덤 시크릿 키 생성"""
    return secrets.token_urlsafe(32)


class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스
    
    모든 민감한 설정은 환경변수에서 읽어옵니다.
    기본값은 개발 환경에서만 사용됩니다.
    """
    
    # =================================
    # 환경 설정
    # =================================
    environment: str = Field(default="development", description="실행 환경 (development/staging/production)")
    debug: bool = Field(default=False, description="디버그 모드")
    log_level: str = Field(default="INFO", description="로그 레벨")
    app_name: str = "Marketing Platform API"
    
    # =================================
    # 서버 URL 설정
    # =================================
    base_url: str = Field(default="http://localhost:3000", alias="BASE_URL")
    backend_url: str = Field(default="http://localhost:8000", description="백엔드 API URL")
    
    # =================================
    # CORS 설정 (환경변수로 관리)
    # =================================
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173",
        description="허용된 CORS origins (콤마로 구분)"
    )
    
    # =================================
    # 모니터링 설정
    # =================================
    discord_webhook_url: Optional[str] = Field(default=None, description="Discord 알림 웹훅 URL")
    memory_threshold: int = Field(default=90, description="메모리 알림 임계값 (%)")
    cpu_threshold: int = Field(default=80, description="CPU 알림 임계값 (%)")
    error_threshold: int = Field(default=10, description="에러 알림 임계값")
    
    # =================================
    # Google OAuth 설정 (환경변수 필수)
    # =================================
    google_client_id: Optional[str] = Field(default=None, description="Google OAuth Client ID")
    google_client_secret: Optional[str] = Field(default=None, description="Google OAuth Client Secret")
    google_redirect_uri: str = Field(default="http://localhost:3000/auth/google/callback")
    
    # =================================
    # Google AI API 설정 (환경변수 필수)
    # =================================
    google_api_key: Optional[str] = Field(default=None, description="Google Gemini API Key")

    # =================================
    # 카카오 OAuth 설정 (환경변수 필수)
    # =================================
    kakao_client_id: Optional[str] = Field(default=None, description="Kakao OAuth Client ID")
    kakao_client_secret: Optional[str] = Field(default=None, description="Kakao OAuth Client Secret")
    kakao_redirect_uri: str = Field(default="http://localhost:3000/auth/kakao/callback")

    # =================================
    # 네이버 OAuth 설정 (환경변수)
    # =================================
    naver_client_id: Optional[str] = Field(default=None, description="Naver OAuth Client ID")
    naver_client_secret: Optional[str] = Field(default=None, description="Naver OAuth Client Secret")

    # =================================
    # PostgreSQL 설정
    # =================================
    postgres_user: str = Field(default="postgres", description="PostgreSQL 사용자명")
    postgres_password: str = Field(default="postgres123", description="PostgreSQL 비밀번호")
    postgres_host: str = Field(default="localhost", description="PostgreSQL 호스트")
    postgres_port: str = Field(default="5432", description="PostgreSQL 포트")
    postgres_db: str = Field(default="marketing_platform", description="PostgreSQL 데이터베이스명")

    # PostgreSQL 연결 풀 설정
    mcp_min_connections: int = Field(default=5, description="최소 연결 수")
    mcp_max_connections: int = Field(default=20, description="최대 연결 수")
    mcp_pool_timeout: int = Field(default=30, description="연결 타임아웃 (초)")
    mcp_pool_recycle: int = Field(default=1800, description="연결 재사용 시간 (초)")
    
    # =================================
    # Redis 설정 (보안 강화)
    # =================================
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, description="Redis 비밀번호 (프로덕션 필수)")
    redis_ssl: bool = Field(default=False, description="Redis SSL 사용 여부")
    redis_url: Optional[str] = Field(default=None, description="Redis URL (설정시 개별 설정 무시)")
    
    # =================================
    # JWT 설정 (보안 강화)
    # =================================
    secret_key: str = Field(
        default_factory=generate_secret_key,
        description="JWT 시크릿 키 (프로덕션에서는 반드시 환경변수로 설정)"
    )
    jwt_algorithm: str = Field(default="HS256", alias="algorithm", description="JWT 알고리즘")
    access_token_expire_minutes: int = Field(default=30, description="액세스 토큰 만료 시간 (분)")
    refresh_token_expire_days: int = Field(default=7, description="리프레시 토큰 만료 시간 (일)")
    
    # JWT 보안 추가 설정
    jwt_issuer: str = Field(default="marketing-platform", description="JWT 발급자")
    jwt_audience: str = Field(default="marketing-platform-users", description="JWT 대상")
    
    # =================================
    # 외부 API 설정
    # =================================
    kakao_map_api_key: Optional[str] = Field(default=None, description="카카오맵 API Key")
    sbdata_api_key: Optional[str] = Field(default=None, description="소상공인진흥공단 API Key")
    kosis_api_key: Optional[str] = Field(default=None, description="통계청 KOSIS API Key")
    
    # =================================
    # 이메일 설정 (환경변수 필수)
    # =================================
    smtp_host: str = Field(default="smtp.gmail.com", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_user: Optional[str] = Field(default=None, alias="SMTP_USER", description="SMTP 사용자명")
    smtp_password: Optional[str] = Field(default=None, alias="SMTP_PASSWORD", description="SMTP 비밀번호")
    smtp_use_tls: bool = Field(default=True, description="SMTP TLS 사용 여부")
    
    # SendGrid 설정
    sendgrid_api_key: Optional[str] = Field(default=None, description="SendGrid API Key")
    
    # =================================
    # 파일 업로드 설정
    # =================================
    upload_dir: str = Field(default="static/images", description="업로드 디렉토리")
    max_upload_size: int = Field(default=10485760, description="최대 업로드 크기 (바이트)")
    
    # =================================
    # Rate Limiting 설정
    # =================================
    rate_limit_enabled: bool = Field(default=True, description="Rate Limiting 활성화")
    rate_limit_requests: int = Field(default=100, description="분당 최대 요청 수")
    rate_limit_window: int = Field(default=60, description="Rate Limit 윈도우 (초)")
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # 정의되지 않은 환경변수 무시
        case_sensitive=False,  # 환경변수 대소문자 구분 없음
    )
    
    # =================================
    # Computed Properties
    # =================================
    
    @property
    def database_url(self) -> str:
        """비동기 데이터베이스 URL"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def sync_database_url(self) -> str:
        """동기식 데이터베이스 URL"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def redis_connection_url(self) -> str:
        """Redis 연결 URL 생성"""
        if self.redis_url:
            return self.redis_url
        
        # 인증이 있는 경우
        if self.redis_password:
            auth = f":{self.redis_password}@"
        else:
            auth = ""
        
        # SSL 스킴
        scheme = "rediss" if self.redis_ssl else "redis"
        
        return f"{scheme}://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """CORS origins를 리스트로 반환"""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    @property
    def is_production(self) -> bool:
        """프로덕션 환경 여부"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """개발 환경 여부"""
        return self.environment.lower() == "development"
    
    @property
    def is_social_login_configured(self) -> dict:
        """소셜 로그인 설정 상태 확인"""
        return {
            "google": bool(self.google_client_id and self.google_client_secret),
            "naver": bool(self.naver_client_id and self.naver_client_secret),
            "kakao": bool(self.kakao_client_id and self.kakao_client_secret)
        }
    
    def validate_production_settings(self) -> List[str]:
        """프로덕션 환경에서 필수 설정 검증"""
        errors = []
        
        if self.is_production:
            # 필수 환경변수 확인
            if not self.google_api_key:
                errors.append("GOOGLE_API_KEY is required in production")
            if self.secret_key == generate_secret_key():
                errors.append("SECRET_KEY must be set explicitly in production")
            if not self.redis_password:
                errors.append("REDIS_PASSWORD is recommended in production")
            if self.debug:
                errors.append("DEBUG should be False in production")
            if "*" in self.cors_origins:
                errors.append("CORS_ORIGINS should not contain '*' in production")
                
        return errors


# 전역 설정 인스턴스
settings = Settings()

# 프로덕션 환경에서 설정 검증
if settings.is_production:
    validation_errors = settings.validate_production_settings()
    if validation_errors:
        import warnings
        for error in validation_errors:
            warnings.warn(f"Production configuration warning: {error}", RuntimeWarning)

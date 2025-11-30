"""
Security Headers 미들웨어

HTTP 보안 헤더를 추가하여 일반적인 웹 취약점으로부터 보호
- XSS (Cross-Site Scripting)
- Clickjacking
- Content-Type Sniffing
- 기타 보안 위협
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    보안 헤더를 추가하는 미들웨어
    
    추가되는 헤더:
    - X-Content-Type-Options: MIME 타입 스니핑 방지
    - X-Frame-Options: Clickjacking 방지
    - X-XSS-Protection: XSS 필터 활성화 (레거시 브라우저용)
    - Strict-Transport-Security: HTTPS 강제 (HSTS)
    - Content-Security-Policy: XSS 및 데이터 주입 공격 방지
    - Referrer-Policy: 리퍼러 정보 제어
    - Permissions-Policy: 브라우저 기능 제어
    """
    
    def __init__(
        self,
        app,
        enable_hsts: bool = True,
        hsts_max_age: int = 31536000,  # 1년
        enable_csp: bool = True,
        csp_policy: Optional[str] = None,
        exclude_paths: Optional[list] = None,
    ):
        super().__init__(app)
        self.enable_hsts = enable_hsts
        self.hsts_max_age = hsts_max_age
        self.enable_csp = enable_csp
        self.exclude_paths = exclude_paths or ["/docs", "/redoc", "/openapi.json"]
        
        # 기본 CSP 정책
        self.csp_policy = csp_policy or self._default_csp_policy()
    
    def _default_csp_policy(self) -> str:
        """기본 Content-Security-Policy 생성"""
        directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",  # React 등 SPA 지원
            "style-src 'self' 'unsafe-inline'",  # 인라인 스타일 허용
            "img-src 'self' data: https: blob:",  # 이미지 소스
            "font-src 'self' data:",
            "connect-src 'self' https://generativelanguage.googleapis.com",  # API 연결
            "frame-ancestors 'none'",  # Clickjacking 방지
            "base-uri 'self'",
            "form-action 'self'",
        ]
        return "; ".join(directives)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # 제외 경로 확인
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return response
        
        # =================================
        # 기본 보안 헤더 추가
        # =================================
        
        # MIME 타입 스니핑 방지
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Clickjacking 방지 (CSP frame-ancestors가 더 현대적이지만 호환성을 위해 유지)
        response.headers["X-Frame-Options"] = "DENY"
        
        # XSS 필터 (레거시 브라우저용, 현대 브라우저는 CSP 사용)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # 리퍼러 정책
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # 브라우저 기능 제한
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(self), "  # 상권 분석에 필요할 수 있음
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )
        
        # =================================
        # HSTS (HTTPS 강제)
        # =================================
        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = (
                f"max-age={self.hsts_max_age}; includeSubDomains"
            )
        
        # =================================
        # Content-Security-Policy
        # =================================
        if self.enable_csp:
            response.headers["Content-Security-Policy"] = self.csp_policy
        
        return response


class APISecurityMiddleware(BaseHTTPMiddleware):
    """
    API 전용 보안 미들웨어
    
    API 응답에 특화된 보안 설정 적용
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # API 경로에만 적용
        if request.url.path.startswith("/api"):
            # JSON API는 캐시하지 않음 (민감한 데이터 보호)
            if "Cache-Control" not in response.headers:
                response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
                response.headers["Pragma"] = "no-cache"
                response.headers["Expires"] = "0"
        
        return response


def get_security_headers_config(is_production: bool = False) -> Dict:
    """
    환경에 따른 보안 헤더 설정 반환
    
    Args:
        is_production: 프로덕션 환경 여부
    
    Returns:
        보안 헤더 미들웨어 설정 딕셔너리
    """
    if is_production:
        return {
            "enable_hsts": True,
            "hsts_max_age": 31536000,  # 1년
            "enable_csp": True,
            "csp_policy": None,  # 기본 정책 사용
        }
    else:
        # 개발 환경에서는 일부 제한 완화
        return {
            "enable_hsts": False,  # localhost에서는 HSTS 비활성화
            "hsts_max_age": 0,
            "enable_csp": True,
            "csp_policy": (
                "default-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "img-src 'self' data: https: blob:; "
                "connect-src 'self' http://localhost:* https://generativelanguage.googleapis.com; "
                "font-src 'self' data:; "
            ),
        }

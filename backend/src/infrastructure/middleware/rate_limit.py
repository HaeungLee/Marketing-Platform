"""
Rate Limiting 미들웨어

API 호출 제한을 통한 서비스 보호
- 사용자별/IP별 요청 제한
- Redis 기반 분산 환경 지원
- 메모리 기반 폴백
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Dict, Callable
from datetime import datetime
import time
import asyncio
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RateLimitExceeded(HTTPException):
    """Rate Limit 초과 예외"""
    def __init__(self, detail: str = "Too many requests", retry_after: int = 60):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers={"Retry-After": str(retry_after)}
        )
        self.retry_after = retry_after


class InMemoryRateLimiter:
    """
    인메모리 Rate Limiter
    
    Redis 없이 동작하는 간단한 구현.
    단일 서버 환경에서 사용.
    """
    
    def __init__(self, requests_per_minute: int = 100, window_seconds: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window_seconds = window_seconds
        self._requests: Dict[str, list] = defaultdict(list)
        self._lock = asyncio.Lock()
    
    async def is_allowed(self, key: str) -> tuple[bool, int]:
        """
        요청 허용 여부 확인
        
        Returns:
            (허용 여부, 남은 요청 수)
        """
        async with self._lock:
            now = time.time()
            window_start = now - self.window_seconds
            
            # 윈도우 내의 요청만 유지
            self._requests[key] = [
                ts for ts in self._requests[key] 
                if ts > window_start
            ]
            
            current_count = len(self._requests[key])
            remaining = max(0, self.requests_per_minute - current_count)
            
            if current_count >= self.requests_per_minute:
                return False, 0
            
            # 요청 기록
            self._requests[key].append(now)
            return True, remaining - 1
    
    async def get_remaining(self, key: str) -> int:
        """남은 요청 수 조회"""
        async with self._lock:
            now = time.time()
            window_start = now - self.window_seconds
            
            valid_requests = [
                ts for ts in self._requests[key]
                if ts > window_start
            ]
            
            return max(0, self.requests_per_minute - len(valid_requests))
    
    async def reset(self, key: str):
        """특정 키의 제한 초기화"""
        async with self._lock:
            self._requests.pop(key, None)
    
    async def cleanup(self):
        """만료된 엔트리 정리"""
        async with self._lock:
            now = time.time()
            window_start = now - self.window_seconds
            
            keys_to_remove = []
            for key, timestamps in self._requests.items():
                valid = [ts for ts in timestamps if ts > window_start]
                if not valid:
                    keys_to_remove.append(key)
                else:
                    self._requests[key] = valid
            
            for key in keys_to_remove:
                del self._requests[key]


class RedisRateLimiter:
    """
    Redis 기반 Rate Limiter
    
    분산 환경에서 사용 가능한 구현.
    Sliding Window 알고리즘 사용.
    """
    
    def __init__(
        self, 
        redis_client, 
        requests_per_minute: int = 100, 
        window_seconds: int = 60,
        key_prefix: str = "ratelimit:"
    ):
        self.redis = redis_client
        self.requests_per_minute = requests_per_minute
        self.window_seconds = window_seconds
        self.key_prefix = key_prefix
    
    async def is_allowed(self, key: str) -> tuple[bool, int]:
        """요청 허용 여부 확인"""
        try:
            full_key = f"{self.key_prefix}{key}"
            now = time.time()
            window_start = now - self.window_seconds
            
            # 파이프라인으로 원자적 실행
            pipe = self.redis.pipeline()
            
            # 1. 윈도우 밖의 오래된 요청 제거
            pipe.zremrangebyscore(full_key, 0, window_start)
            
            # 2. 현재 윈도우 내 요청 수 조회
            pipe.zcard(full_key)
            
            # 3. 새 요청 추가
            pipe.zadd(full_key, {str(now): now})
            
            # 4. TTL 설정 (윈도우 시간 + 여유)
            pipe.expire(full_key, self.window_seconds + 10)
            
            results = await pipe.execute()
            current_count = results[1]
            
            remaining = max(0, self.requests_per_minute - current_count)
            
            if current_count >= self.requests_per_minute:
                # 방금 추가한 요청 제거
                await self.redis.zrem(full_key, str(now))
                return False, 0
            
            return True, remaining
            
        except Exception as e:
            logger.error(f"Redis rate limiting error: {e}")
            # Redis 오류 시 허용 (fail-open)
            return True, self.requests_per_minute
    
    async def get_remaining(self, key: str) -> int:
        """남은 요청 수 조회"""
        try:
            full_key = f"{self.key_prefix}{key}"
            now = time.time()
            window_start = now - self.window_seconds
            
            # 윈도우 내 요청 수 조회
            count = await self.redis.zcount(full_key, window_start, now)
            return max(0, self.requests_per_minute - count)
            
        except Exception as e:
            logger.error(f"Redis rate limit check error: {e}")
            return self.requests_per_minute
    
    async def reset(self, key: str):
        """특정 키의 제한 초기화"""
        try:
            full_key = f"{self.key_prefix}{key}"
            await self.redis.delete(full_key)
        except Exception as e:
            logger.error(f"Redis rate limit reset error: {e}")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI Rate Limiting 미들웨어
    
    사용법:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=100,
            redis_client=redis  # Optional
        )
    """
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 100,
        window_seconds: int = 60,
        redis_client=None,
        key_func: Optional[Callable[[Request], str]] = None,
        exclude_paths: Optional[list] = None,
        enabled: bool = True
    ):
        super().__init__(app)
        self.enabled = enabled
        self.exclude_paths = exclude_paths or ["/health", "/docs", "/redoc", "/openapi.json"]
        
        # Rate Limiter 선택
        if redis_client:
            self.limiter = RedisRateLimiter(
                redis_client, 
                requests_per_minute, 
                window_seconds
            )
        else:
            self.limiter = InMemoryRateLimiter(
                requests_per_minute, 
                window_seconds
            )
        
        # 키 생성 함수
        self.key_func = key_func or self._default_key_func
        
        logger.info(
            f"Rate limiting initialized: {requests_per_minute} req/{window_seconds}s, "
            f"backend={'Redis' if redis_client else 'InMemory'}"
        )
    
    def _default_key_func(self, request: Request) -> str:
        """기본 키 생성: IP 주소 기반"""
        # X-Forwarded-For 헤더 확인 (프록시 뒤에 있을 때)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        else:
            ip = request.client.host if request.client else "unknown"
        
        return f"ip:{ip}"
    
    async def dispatch(self, request: Request, call_next):
        """미들웨어 실행"""
        # 비활성화 시 바로 통과
        if not self.enabled:
            return await call_next(request)
        
        # 제외 경로 확인
        path = request.url.path
        if any(path.startswith(excluded) for excluded in self.exclude_paths):
            return await call_next(request)
        
        # Rate Limit 키 생성
        key = self.key_func(request)
        
        # Rate Limit 확인
        allowed, remaining = await self.limiter.is_allowed(key)
        
        if not allowed:
            logger.warning(f"Rate limit exceeded for {key}")
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "retry_after": 60
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.limiter.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + 60)
                }
            )
        
        # 요청 처리
        response = await call_next(request)
        
        # Rate Limit 헤더 추가
        response.headers["X-RateLimit-Limit"] = str(self.limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
        
        return response


# 데코레이터 기반 Rate Limiting (특정 엔드포인트용)
def rate_limit(
    requests: int = 10,
    window: int = 60,
    key_func: Optional[Callable[[Request], str]] = None
):
    """
    엔드포인트별 Rate Limiting 데코레이터
    
    사용법:
        @router.get("/expensive")
        @rate_limit(requests=5, window=60)
        async def expensive_operation(request: Request):
            ...
    """
    # 엔드포인트별 limiter
    limiter = InMemoryRateLimiter(requests, window)
    
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            # 키 생성
            if key_func:
                key = key_func(request)
            else:
                ip = request.client.host if request.client else "unknown"
                key = f"{func.__name__}:{ip}"
            
            # Rate Limit 확인
            allowed, remaining = await limiter.is_allowed(key)
            
            if not allowed:
                raise RateLimitExceeded(
                    detail=f"Rate limit exceeded for {func.__name__}",
                    retry_after=window
                )
            
            return await func(request, *args, **kwargs)
        
        return wrapper
    return decorator

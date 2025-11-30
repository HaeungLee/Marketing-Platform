"""
구조화된 로깅 설정

JSON 형식의 구조화된 로그를 생성하여:
- 로그 분석 도구와의 호환성 향상
- 검색 및 필터링 용이
- 모니터링 시스템 연동 지원
"""
import logging
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
import os


class JSONFormatter(logging.Formatter):
    """JSON 형식으로 로그를 포맷하는 Formatter"""
    
    def __init__(
        self,
        include_timestamp: bool = True,
        include_level: bool = True,
        include_logger: bool = True,
        include_path: bool = True,
        extra_fields: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()
        self.include_timestamp = include_timestamp
        self.include_level = include_level
        self.include_logger = include_logger
        self.include_path = include_path
        self.extra_fields = extra_fields or {}
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {}
        
        if self.include_timestamp:
            log_data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        
        if self.include_level:
            log_data["level"] = record.levelname
        
        if self.include_logger:
            log_data["logger"] = record.name
        
        log_data["message"] = record.getMessage()
        
        if self.include_path:
            log_data["path"] = f"{record.pathname}:{record.lineno}"
        
        # 예외 정보 추가
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # 추가 필드
        if self.extra_fields:
            log_data.update(self.extra_fields)
        
        # record에 추가된 extra 데이터
        for key, value in record.__dict__.items():
            if key not in [
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "pathname", "process", "processName", "relativeCreated",
                "stack_info", "exc_info", "exc_text", "thread", "threadName",
                "message", "asctime"
            ]:
                try:
                    json.dumps(value)  # JSON 직렬화 가능 여부 확인
                    log_data[key] = value
                except (TypeError, ValueError):
                    log_data[key] = str(value)
        
        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """컬러 콘솔 출력을 위한 Formatter"""
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    level: str = "INFO",
    json_format: bool = False,
    log_file: Optional[str] = None,
    app_name: str = "marketing-platform",
    environment: str = "development",
) -> logging.Logger:
    """
    애플리케이션 로깅 설정
    
    Args:
        level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: JSON 형식 사용 여부
        log_file: 로그 파일 경로 (None이면 콘솔만)
        app_name: 애플리케이션 이름
        environment: 환경 (development, production, test)
    
    Returns:
        설정된 root logger
    """
    # 로그 레벨 설정
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # 기존 핸들러 제거
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.setLevel(log_level)
    
    # =================================
    # 콘솔 핸들러
    # =================================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if json_format:
        console_formatter = JSONFormatter(
            extra_fields={
                "app": app_name,
                "environment": environment,
            }
        )
    else:
        # 개발 환경에서는 컬러 포맷터 사용
        if environment == "development":
            console_formatter = ColoredFormatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        else:
            console_formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
    
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # =================================
    # 파일 핸들러 (옵션)
    # =================================
    if log_file:
        # 로그 디렉토리 생성
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        
        # 파일은 항상 JSON 형식
        file_formatter = JSONFormatter(
            extra_fields={
                "app": app_name,
                "environment": environment,
            }
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # =================================
    # 외부 라이브러리 로그 레벨 조정
    # =================================
    # 너무 verbose한 라이브러리 로그 줄이기
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    return root_logger


class RequestLogger:
    """
    요청/응답 로깅을 위한 컨텍스트 매니저
    
    Usage:
        with RequestLogger(request_id="abc123") as log:
            log.info("Processing request")
    """
    
    def __init__(
        self,
        request_id: str,
        logger: Optional[logging.Logger] = None,
    ):
        self.request_id = request_id
        self.logger = logger or logging.getLogger(__name__)
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.utcnow()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.error(f"Request failed: {exc_val}")
        return False
    
    def _log(self, level: int, message: str, **kwargs):
        extra = {
            "request_id": self.request_id,
            **kwargs,
        }
        self.logger.log(level, f"[{self.request_id}] {message}", extra=extra)
    
    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log(logging.ERROR, message, **kwargs)
    
    def get_duration_ms(self) -> float:
        if self.start_time:
            return (datetime.utcnow() - self.start_time).total_seconds() * 1000
        return 0


# logging.handlers import 필요
import logging.handlers

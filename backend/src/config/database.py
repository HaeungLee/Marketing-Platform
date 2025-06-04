"""
데이터베이스 설정
"""
from typing import Dict, Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from .settings import settings

# 동기식 엔진 설정
engine = create_engine(
    settings.sync_database_url,
    pool_pre_ping=True,
    pool_size=settings.mcp_min_connections,
    max_overflow=settings.mcp_max_connections - settings.mcp_min_connections,
    pool_timeout=settings.mcp_pool_timeout,
    pool_recycle=settings.mcp_pool_recycle
)

# 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    데이터베이스 세션을 가져오는 의존성 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from typing import Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from .settings import settings

# 엔진 설정
engine = create_async_engine(
    settings.database_url,
    poolclass=NullPool,
    echo=False
)

# 세션 설정
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncSession:
    """
    데이터베이스 세션을 가져오는 의존성 함수
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
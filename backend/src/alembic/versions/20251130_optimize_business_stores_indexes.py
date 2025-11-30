"""optimize business_stores indexes

Revision ID: 20251130_optimize
Revises: 75c45e0a3101
Create Date: 2025-11-30 20:30:00.000000

쿼리 패턴 분석 결과:
1. 위치 기반 조회: latitude, longitude + business_status
2. 지역 조회: sido_name, sigungu_name, dong_name + business_status
3. 업종 필터: business_name + business_status
4. 유니크 조회: store_number (이미 존재)

최적화:
- 개별 인덱스 10개 → 복합 인덱스 4개로 통합
- 지역 조회용 복합 인덱스 추가
- 쓰기 성능 개선 (인덱스 수 감소)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '20251130_optimize'
down_revision: Union[str, None] = '75c45e0a3101'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ===========================================
    # 1. 새로운 복합 인덱스 생성 (먼저 생성)
    # ===========================================
    
    # 지역 조회용 복합 인덱스 (sido_name → sigungu_name → dong_name)
    # 쿼리: WHERE sido_name = ? AND sigungu_name = ? AND dong_name ILIKE ?
    op.create_index(
        'ix_business_stores_region',
        'business_stores',
        ['sido_name', 'sigungu_name', 'dong_name'],
        unique=False
    )
    
    # 업종 + 상태 복합 인덱스
    # 쿼리: WHERE business_status = '영업' AND business_name ILIKE ?
    op.create_index(
        'ix_business_stores_business_status_name',
        'business_stores',
        ['business_status', 'business_name'],
        unique=False
    )
    
    # 위치 기반 조회용 복합 인덱스 (위경도 범위 쿼리)
    # 쿼리: Haversine 거리 계산 + business_status
    op.create_index(
        'ix_business_stores_geo_status',
        'business_stores',
        ['business_status', 'latitude', 'longitude'],
        unique=False
    )
    
    # 업종코드 + 상태 복합 인덱스 (통계 쿼리용)
    op.create_index(
        'ix_business_stores_code_status',
        'business_stores',
        ['business_code', 'business_status'],
        unique=False
    )
    
    # ===========================================
    # 2. 불필요한 개별 인덱스 제거
    # ===========================================
    
    # 복합 인덱스로 대체되는 개별 인덱스들 제거
    op.drop_index('ix_business_stores_sido_name', table_name='business_stores')
    op.drop_index('ix_business_stores_sigungu_name', table_name='business_stores')
    op.drop_index('ix_business_stores_dong_name', table_name='business_stores')
    op.drop_index('ix_business_stores_latitude', table_name='business_stores')
    op.drop_index('ix_business_stores_longitude', table_name='business_stores')
    op.drop_index('ix_business_stores_business_status', table_name='business_stores')
    op.drop_index('ix_business_stores_business_name', table_name='business_stores')
    op.drop_index('ix_business_stores_business_code', table_name='business_stores')
    
    # 유지되는 인덱스:
    # - ix_business_stores_store_number (unique) - 동기화용
    # - ix_business_stores_store_name - 검색용 (선택적 유지)


def downgrade() -> None:
    # ===========================================
    # 1. 원래 개별 인덱스 복원
    # ===========================================
    op.create_index('ix_business_stores_business_code', 'business_stores', ['business_code'], unique=False)
    op.create_index('ix_business_stores_business_name', 'business_stores', ['business_name'], unique=False)
    op.create_index('ix_business_stores_business_status', 'business_stores', ['business_status'], unique=False)
    op.create_index('ix_business_stores_dong_name', 'business_stores', ['dong_name'], unique=False)
    op.create_index('ix_business_stores_latitude', 'business_stores', ['latitude'], unique=False)
    op.create_index('ix_business_stores_longitude', 'business_stores', ['longitude'], unique=False)
    op.create_index('ix_business_stores_sido_name', 'business_stores', ['sido_name'], unique=False)
    op.create_index('ix_business_stores_sigungu_name', 'business_stores', ['sigungu_name'], unique=False)
    
    # ===========================================
    # 2. 새로운 복합 인덱스 제거
    # ===========================================
    op.drop_index('ix_business_stores_code_status', table_name='business_stores')
    op.drop_index('ix_business_stores_geo_status', table_name='business_stores')
    op.drop_index('ix_business_stores_business_status_name', table_name='business_stores')
    op.drop_index('ix_business_stores_region', table_name='business_stores')

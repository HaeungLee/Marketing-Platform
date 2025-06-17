from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Text
from sqlalchemy.sql import func
from src.config.database import Base


class BusinessStore(Base):
    """소상공인시장진흥공단 상가(상권) 정보 모델"""
    __tablename__ = "business_stores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 기본 정보
    store_number = Column(String(20), nullable=False, unique=True, index=True)  # 상가업소번호
    store_name = Column(String(200), nullable=False, index=True)  # 상호명
    business_code = Column(String(10), nullable=False, index=True)  # 업종코드
    business_name = Column(String(100), nullable=False, index=True)  # 업종명
    
    # 위치 정보
    longitude = Column(Float, nullable=False, index=True)  # 경도
    latitude = Column(Float, nullable=False, index=True)  # 위도
    jibun_address = Column(String(300))  # 지번주소
    road_address = Column(String(300))  # 도로명주소
    
    # 행정구역 정보
    sido_name = Column(String(50), nullable=False, index=True)  # 시도명
    sigungu_name = Column(String(50), nullable=False, index=True)  # 시군구명
    dong_name = Column(String(50), nullable=False, index=True)  # 행정동명
    
    # 상세 정보
    building_name = Column(String(200))  # 건물명
    floor_info = Column(String(50))  # 층정보
    room_info = Column(String(50))  # 호정보
    
    # 영업 정보
    open_date = Column(Date)  # 개업일자
    close_date = Column(Date, nullable=True)  # 폐업일자
    business_status = Column(String(20), nullable=False, index=True)  # 영업상태
    
    # 분류 정보
    standard_industry_code = Column(String(10))  # 표준산업분류코드
    commercial_category_code = Column(String(20))  # 상권업종분류코드
    
    # 메타데이터
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<BusinessStore(store_name='{self.store_name}', business_name='{self.business_name}')>"
    
    class Meta:
        indexes = [
            ('sido_name', 'sigungu_name', 'dong_name'),
            ('business_code', 'business_status'),
            ('longitude', 'latitude'),
        ] 
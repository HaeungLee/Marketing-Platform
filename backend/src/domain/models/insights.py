from sqlalchemy import Column, Integer, String, Date, DateTime, BigInteger, Float
from sqlalchemy.sql import func
from src.config.database import Base


class FloatingPopulation(Base):
    """유동인구 데이터 모델"""
    __tablename__ = "floating_population"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), nullable=False, index=True)
    measurement_time = Column(DateTime, nullable=False, index=True)
    region_type = Column(String(50), nullable=False)  # main_street, traditional_markets, public_facilities
    district = Column(String(50), nullable=False)
    admin_dong = Column(String(50), nullable=False)
    visitor_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    class Meta:
        indexes = [
            ('measurement_time', 'region_type'),
            ('district', 'admin_dong'),
        ]


class CardConsumption(Base):
    """카드 소비 데이터 모델"""
    __tablename__ = "card_consumption"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(Date, nullable=False, index=True)
    region_code = Column(String(20), nullable=False)
    admin_city_code = Column(String(20), nullable=False)
    business_type_code = Column(String(10), nullable=False)
    business_category_1 = Column(String(50), nullable=False)
    business_category_2 = Column(String(50), nullable=False)
    hour_range = Column(Integer, nullable=False)  # 0-23
    gender = Column(String(1), nullable=False)  # M, F
    age_group = Column(Integer, nullable=False)  # 1-9 (10대 단위)
    day_of_week = Column(Integer, nullable=False)  # 1-7
    amount = Column(BigInteger, nullable=False)
    transaction_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    class Meta:
        indexes = [
            ('transaction_date', 'business_type_code'),
            ('region_code', 'business_category_1'),
            ('age_group', 'gender'),
        ]


class BusinessCodes(Base):
    """업종 코드 분류 모델"""
    __tablename__ = "business_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    major_category_code = Column(String(10), nullable=False)
    major_category_name = Column(String(100), nullable=False)
    middle_category_code = Column(String(10), nullable=False)
    middle_category_name = Column(String(100), nullable=False)
    minor_category_code = Column(String(10), nullable=False, unique=True, index=True)
    minor_category_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class KTMovementData(Base):
    """KT 생활이동 데이터 모델"""
    __tablename__ = "kt_movement_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    departure_code = Column(String(20), nullable=False)
    arrival_code = Column(String(20), nullable=False)
    gender = Column(String(1), nullable=False)  # M, F
    age_group = Column(Integer, nullable=False)
    departure_place_type = Column(String(10), nullable=False)  # HE, WO, etc
    arrival_place_type = Column(String(10), nullable=False)
    total_movement_time = Column(Integer, nullable=False)  # minutes
    movement_distance = Column(Float, nullable=False)  # km
    population_count = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    class Meta:
        indexes = [
            ('departure_time', 'arrival_time'),
            ('departure_code', 'arrival_code'),
            ('age_group', 'gender'),
        ]


class SmallBusinessSales(Base):
    """소상공인 사업체당 매출액 데이터"""
    __tablename__ = "small_business_sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    region_code = Column(String(20), nullable=False)
    region_name = Column(String(100), nullable=False)
    business_type = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=True)  # 1, 2, 3, 4 or None for yearly
    sales_per_business = Column(BigInteger, nullable=False)  # 사업체당 매출액 (원)
    business_count = Column(Integer, nullable=False)  # 사업체 수
    total_sales = Column(BigInteger, nullable=False)  # 총 매출액
    created_at = Column(DateTime, server_default=func.now())
    
    class Meta:
        indexes = [
            ('region_code', 'year'),
            ('business_type', 'year'),
        ]

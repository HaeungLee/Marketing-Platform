from datetime import date, datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ==================== 유동인구 관련 스키마 ====================

class FloatingPopulationBase(BaseModel):
    device_id: str = Field(..., description="측정 기기 ID")
    measurement_time: datetime = Field(..., description="측정 시간")
    region_type: str = Field(..., description="지역 유형 (main_street, traditional_markets, public_facilities)")
    district: str = Field(..., description="자치구")
    admin_dong: str = Field(..., description="행정동")
    visitor_count: int = Field(..., description="방문자 수")


class FloatingPopulationResponse(FloatingPopulationBase):
    id: int = Field(..., description="고유 식별자")
    created_at: datetime = Field(..., description="생성 시간")

    class Config:
        from_attributes = True


# ==================== 카드 소비 관련 스키마 ====================

class CardConsumptionBase(BaseModel):
    transaction_date: date = Field(..., description="거래 날짜")
    region_code: str = Field(..., description="지역 코드")
    admin_city_code: str = Field(..., description="행정 시 코드")
    business_type_code: str = Field(..., description="업종 코드")
    business_category_1: str = Field(..., description="업종 대분류")
    business_category_2: str = Field(..., description="업종 소분류")
    hour_range: int = Field(..., ge=0, le=23, description="시간대 (0-23)")
    gender: str = Field(..., regex="^[MF]$", description="성별 (M/F)")
    age_group: int = Field(..., ge=1, le=9, description="연령대 (1-9, 10대 단위)")
    day_of_week: int = Field(..., ge=1, le=7, description="요일 (1-7)")
    amount: int = Field(..., description="소비 금액")
    transaction_count: int = Field(..., description="거래 건수")


class CardConsumptionResponse(CardConsumptionBase):
    id: int = Field(..., description="고유 식별자")
    created_at: datetime = Field(..., description="생성 시간")

    class Config:
        from_attributes = True


# ==================== 업종 코드 관련 스키마 ====================

class BusinessCodeBase(BaseModel):
    major_category_code: str = Field(..., description="대분류 코드")
    major_category_name: str = Field(..., description="대분류명")
    middle_category_code: str = Field(..., description="중분류 코드")
    middle_category_name: str = Field(..., description="중분류명")
    minor_category_code: str = Field(..., description="소분류 코드")
    minor_category_name: str = Field(..., description="소분류명")


class BusinessCodeResponse(BusinessCodeBase):
    id: int = Field(..., description="고유 식별자")

    class Config:
        from_attributes = True


# ==================== 인사이트 분석 결과 스키마 ====================

class TargetSegment(BaseModel):
    age_group: str = Field(..., description="연령대")
    percentage: float = Field(..., description="비율 (%)")
    population_count: int = Field(..., description="인구 수")
    consumption_index: float = Field(..., description="소비 지수")


class MarketingStrategy(BaseModel):
    strategy_type: str = Field(..., description="전략 유형")
    description: str = Field(..., description="전략 설명")
    expected_impact: str = Field(..., description="예상 효과")


class TargetCustomerAnalysisResult(BaseModel):
    primary_target: TargetSegment = Field(..., description="주 타겟층")
    secondary_target: TargetSegment = Field(..., description="부 타겟층")
    strategies: List[MarketingStrategy] = Field(..., description="추천 마케팅 전략")
    confidence_score: float = Field(..., ge=0, le=100, description="분석 신뢰도 (%)")
    data_source: str = Field(..., description="데이터 출처")
    analysis_date: datetime = Field(..., description="분석 일시")


class LocationScore(BaseModel):
    location: str = Field(..., description="지역명")
    total_score: float = Field(..., ge=0, le=100, description="종합 점수")
    population_score: float = Field(..., description="인구 밀도 점수")
    target_match_score: float = Field(..., description="타겟 매칭 점수")
    floating_pop_score: float = Field(..., description="유동인구 점수")
    consumption_score: float = Field(..., description="소비 패턴 점수")
    competition_score: float = Field(..., description="경쟁 강도 점수")
    cost_efficiency_score: float = Field(..., description="비용 효율성 점수")


class LocationRecommendation(BaseModel):
    recommended_areas: List[LocationScore] = Field(..., description="추천 지역 목록")
    analysis_metadata: Dict[str, Any] = Field(..., description="분석 메타데이터")
    confidence_level: float = Field(..., ge=0, le=100, description="신뢰도")


class TimingPattern(BaseModel):
    time_period: str = Field(..., description="시간대/요일")
    activity_index: float = Field(..., description="활동 지수")
    recommendation_score: float = Field(..., description="추천 점수")


class TimingRecommendation(BaseModel):
    best_days: List[TimingPattern] = Field(..., description="최적 요일")
    best_hours: List[TimingPattern] = Field(..., description="최적 시간대")
    seasonal_trends: Dict[str, float] = Field(..., description="계절별 트렌드")
    campaign_recommendations: List[str] = Field(..., description="캠페인 추천사항")
    data_confidence: float = Field(..., ge=0, le=100, description="데이터 신뢰도")


# ==================== 분석 요청 스키마 ====================

class TargetAnalysisRequest(BaseModel):
    business_type: str = Field(..., description="업종")
    region: str = Field(..., description="지역")
    target_age_range: Optional[str] = Field(None, description="타겟 연령대")


class LocationAnalysisRequest(BaseModel):
    business_type: str = Field(..., description="업종")
    budget: int = Field(..., ge=0, description="예산")
    target_age_range: Optional[str] = Field(None, description="타겟 연령대")
    preferred_regions: Optional[List[str]] = Field(None, description="선호 지역")


class TimingAnalysisRequest(BaseModel):
    business_type: str = Field(..., description="업종")
    region: str = Field(..., description="지역")
    target_age: str = Field(..., description="타겟 연령대")
    campaign_type: Optional[str] = Field(None, description="캠페인 유형")


# ==================== 필터 및 검색 스키마 ====================

class FloatingPopulationFilter(BaseModel):
    region_type: Optional[str] = Field(None, description="지역 유형")
    district: Optional[str] = Field(None, description="자치구")
    admin_dong: Optional[str] = Field(None, description="행정동")
    start_date: Optional[datetime] = Field(None, description="시작 날짜")
    end_date: Optional[datetime] = Field(None, description="종료 날짜")


class CardConsumptionFilter(BaseModel):
    business_category: Optional[str] = Field(None, description="업종 카테고리")
    region_code: Optional[str] = Field(None, description="지역 코드")
    age_group: Optional[int] = Field(None, description="연령대")
    gender: Optional[str] = Field(None, description="성별")
    start_date: Optional[date] = Field(None, description="시작 날짜")
    end_date: Optional[date] = Field(None, description="종료 날짜")


# ==================== 통계 및 집계 스키마 ====================

class ConsumptionStatistics(BaseModel):
    total_amount: int = Field(..., description="총 소비금액")
    total_transactions: int = Field(..., description="총 거래건수")
    avg_amount_per_transaction: float = Field(..., description="거래당 평균 금액")
    peak_hour: int = Field(..., description="피크 시간대")
    peak_day: str = Field(..., description="피크 요일")


class RegionPopulationSummary(BaseModel):
    region_name: str = Field(..., description="지역명")
    total_population: int = Field(..., description="총 인구")
    avg_floating_population: float = Field(..., description="평균 유동인구")
    dominant_age_group: str = Field(..., description="주요 연령대")
    business_density: float = Field(..., description="업체 밀도")

"""
데이터 분석 및 시각화 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import random

router = APIRouter()


# Request Models
class TargetAnalysisRequest(BaseModel):
    business_id: str
    business_category: str
    latitude: float
    longitude: float
    radius_km: float = Field(1.0, ge=0.1, le=10.0)
    product_type: Optional[str] = None
    price_range: Optional[str] = None


class CompetitorAnalysisRequest(BaseModel):
    business_category: str
    latitude: float
    longitude: float
    radius_km: float = Field(2.0, ge=0.5, le=20.0)


class TrendAnalysisRequest(BaseModel):
    business_category: str
    period_months: int = Field(12, ge=1, le=36)
    region: Optional[str] = None


# Response Models
class DemographicData(BaseModel):
    age_group: str
    gender: str
    percentage: float
    income_level: str
    lifestyle: List[str]


class TargetAudienceResponse(BaseModel):
    business_id: str
    analysis_date: datetime
    total_population: int
    demographics: List[DemographicData]
    peak_hours: List[Dict[str, Any]]
    seasonal_trends: Dict[str, float]
    recommendations: List[str]


class CompetitorInfo(BaseModel):
    name: str
    category: str
    distance_km: float
    rating: float
    price_level: int
    strengths: List[str]
    weaknesses: List[str]


class CompetitorAnalysisResponse(BaseModel):
    analysis_date: datetime
    total_competitors: int
    competitors: List[CompetitorInfo]
    market_saturation: str
    opportunities: List[str]
    threats: List[str]


class TrendData(BaseModel):
    month: str
    search_volume: int
    interest_score: float
    related_keywords: List[str]


class TrendAnalysisResponse(BaseModel):
    category: str
    analysis_period: str
    trend_direction: str
    monthly_data: List[TrendData]
    insights: List[str]
    predictions: List[str]


class MarketInsight(BaseModel):
    title: str
    description: str
    impact: str
    confidence: float
    source: str


class DashboardResponse(BaseModel):
    business_id: str
    last_updated: datetime
    key_metrics: Dict[str, Any]
    recent_insights: List[MarketInsight]
    recommended_actions: List[str]
    performance_score: float


@router.post("/target-audience", response_model=TargetAudienceResponse)
async def analyze_target_audience(request: TargetAnalysisRequest):
    """
    타겟 고객층 분석
    
    비즈니스 위치와 업종을 바탕으로 주변 지역의 인구통계학적 데이터를 분석하여
    타겟 고객층을 식별하고 특성을 분석합니다.
    """
    try:
        # 샘플 데이터 생성 (실제로는 공공데이터 API 연동)
        demographics = []
        
        # 업종별 타겟층 샘플 데이터
        if "카페" in request.business_category or "cafe" in request.business_category.lower():
            demographics = [
                DemographicData(
                    age_group="20-29",
                    gender="여성",
                    percentage=35.2,
                    income_level="중간",
                    lifestyle=["카페 문화", "SNS 활동", "트렌드 민감"]
                ),
                DemographicData(
                    age_group="30-39",
                    gender="남성",
                    percentage=22.8,
                    income_level="중상",
                    lifestyle=["업무 미팅", "독서", "여유로운 시간"]
                ),
                DemographicData(
                    age_group="20-29",
                    gender="남성",
                    percentage=18.5,
                    income_level="중간",
                    lifestyle=["스터디", "모임", "디지털 기기"]
                )
            ]
        elif "음식점" in request.business_category:
            demographics = [
                DemographicData(
                    age_group="30-49",
                    gender="전체",
                    percentage=45.0,
                    income_level="중상",
                    lifestyle=["가족 식사", "회식", "맛집 탐방"]
                ),
                DemographicData(
                    age_group="20-29",
                    gender="전체",
                    percentage=30.0,
                    income_level="중간",
                    lifestyle=["데이트", "친구 모임", "배달 선호"]
                )
            ]
        else:
            # 기본 샘플 데이터
            demographics = [
                DemographicData(
                    age_group="25-40",
                    gender="전체",
                    percentage=40.0,
                    income_level="중간",
                    lifestyle=["편의성 중시", "품질 추구", "온라인 활동"]
                )
            ]
        
        # 피크 시간대 (업종별)
        peak_hours = [
            {"hour": 9, "traffic": 0.3, "description": "출근길"},
            {"hour": 12, "traffic": 0.8, "description": "점심시간"},
            {"hour": 15, "traffic": 0.5, "description": "오후 휴식"},
            {"hour": 18, "traffic": 0.7, "description": "퇴근길"},
            {"hour": 20, "traffic": 0.4, "description": "저녁시간"}
        ]
        
        # 계절별 트렌드
        seasonal_trends = {
            "spring": 1.1,
            "summer": 0.9,
            "autumn": 1.2,
            "winter": 0.8
        }
        
        # 추천사항
        recommendations = [
            f"주 고객층인 {demographics[0].age_group} {demographics[0].gender}를 타겟으로 한 마케팅 전략 수립",
            f"피크 시간대({max(peak_hours, key=lambda x: x['traffic'])['hour']}시)에 집중적인 프로모션 진행",
            "계절별 트렌드를 고려한 메뉴/상품 기획",
            "SNS 마케팅을 통한 젊은 층 고객 확보"
        ]
        
        return TargetAudienceResponse(
            business_id=request.business_id,
            analysis_date=datetime.now(),
            total_population=random.randint(5000, 20000),
            demographics=demographics,
            peak_hours=peak_hours,
            seasonal_trends=seasonal_trends,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"타겟 고객층 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/competitors", response_model=CompetitorAnalysisResponse)
async def analyze_competitors(request: CompetitorAnalysisRequest):
    """
    경쟁사 분석
    
    주변 지역의 동종 업체를 분석하여 시장 상황과 경쟁 환경을 파악합니다.
    """
    try:
        # 샘플 경쟁사 데이터
        competitors = [
            CompetitorInfo(
                name="스타벅스 강남점",
                category="카페",
                distance_km=0.3,
                rating=4.2,
                price_level=4,
                strengths=["브랜드 인지도", "다양한 메뉴", "편의시설"],
                weaknesses=["높은 가격", "혼잡함", "개성 부족"]
            ),
            CompetitorInfo(
                name="투썸플레이스",
                category="카페",
                distance_km=0.5,
                rating=4.0,
                price_level=4,
                strengths=["케이크 전문", "넓은 공간", "조용한 분위기"],
                weaknesses=["높은 가격", "주차 불편", "서비스 품질 편차"]
            ),
            CompetitorInfo(
                name="로컬 카페 '커피향기'",
                category="카페",
                distance_km=0.2,
                rating=4.5,
                price_level=2,
                strengths=["저렴한 가격", "친근한 서비스", "단골 고객"],
                weaknesses=["브랜드 인지도 낮음", "마케팅 부족", "시설 노후"]
            )
        ]
        
        # 시장 포화도 분석
        competitor_count = len(competitors)
        if competitor_count <= 2:
            market_saturation = "낮음"
        elif competitor_count <= 5:
            market_saturation = "보통"
        else:
            market_saturation = "높음"
        
        # 기회 요인
        opportunities = [
            "프랜차이즈 대비 차별화된 개성 있는 콘셉트 가능",
            "로컬 고객층 공략을 통한 안정적인 단골 확보",
            "합리적인 가격대로 가성비 어필",
            "SNS 마케팅을 통한 젊은 층 유입"
        ]
        
        # 위협 요인
        threats = [
            "대형 프랜차이즈의 브랜드 파워",
            "배달 앱을 통한 간접 경쟁 증가",
            "임대료 상승 압박",
            "코로나19 등 외부 환경 변화"
        ]
        
        return CompetitorAnalysisResponse(
            analysis_date=datetime.now(),
            total_competitors=len(competitors),
            competitors=competitors,
            market_saturation=market_saturation,
            opportunities=opportunities,
            threats=threats
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"경쟁사 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/trends", response_model=TrendAnalysisResponse)
async def analyze_trends(request: TrendAnalysisRequest):
    """
    트렌드 분석
    
    업종별 검색 트렌드와 시장 동향을 분석합니다.
    """
    try:
        # 샘플 월별 트렌드 데이터
        monthly_data = []
        base_date = datetime.now() - timedelta(days=30 * request.period_months)
        
        for i in range(request.period_months):
            month_date = base_date + timedelta(days=30 * i)
            search_volume = random.randint(1000, 5000)
            interest_score = random.uniform(0.3, 1.0)
            
            monthly_data.append(TrendData(
                month=month_date.strftime("%Y-%m"),
                search_volume=search_volume,
                interest_score=interest_score,
                related_keywords=[
                    f"{request.business_category} 추천",
                    f"{request.business_category} 맛집",
                    f"{request.business_category} 리뷰"
                ]
            ))
        
        # 트렌드 방향 분석
        recent_scores = [data.interest_score for data in monthly_data[-3:]]
        earlier_scores = [data.interest_score for data in monthly_data[:3]]
        
        if sum(recent_scores) > sum(earlier_scores):
            trend_direction = "상승"
        elif sum(recent_scores) < sum(earlier_scores):
            trend_direction = "하락"
        else:
            trend_direction = "유지"
        
        # 인사이트
        insights = [
            f"{request.business_category} 업종의 온라인 관심도가 {trend_direction} 추세",
            "모바일 검색 비율이 지속적으로 증가",
            "리뷰와 평점의 영향력이 확대",
            "배달/테이크아웃 관련 검색 증가"
        ]
        
        # 예측
        predictions = [
            "향후 3개월간 현재 트렌드 지속 예상",
            "시즌별 변동성 고려한 마케팅 전략 필요",
            "온라인 리뷰 관리의 중요성 증대",
            "개인화된 고객 서비스 트렌드 확산"
        ]
        
        return TrendAnalysisResponse(
            category=request.business_category,
            analysis_period=f"{request.period_months}개월",
            trend_direction=trend_direction,
            monthly_data=monthly_data,
            insights=insights,
            predictions=predictions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"트렌드 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/dashboard/{business_id}", response_model=DashboardResponse)
async def get_dashboard_data(business_id: str):
    """
    비즈니스 대시보드 데이터
    
    비즈니스의 종합적인 분석 결과와 인사이트를 제공합니다.
    """
    try:
        # 주요 지표
        key_metrics = {
            "target_audience_size": random.randint(5000, 20000),
            "competitor_count": random.randint(3, 15),
            "market_potential": random.uniform(0.6, 0.9),
            "trend_score": random.uniform(0.4, 0.8),
            "engagement_rate": random.uniform(0.02, 0.08),
            "content_performance": random.uniform(0.5, 0.9)
        }
        
        # 최근 인사이트
        recent_insights = [
            MarketInsight(
                title="타겟 고객층 변화 감지",
                description="20대 여성 고객의 방문 비율이 15% 증가했습니다.",
                impact="긍정적",
                confidence=0.85,
                source="인구통계 분석"
            ),
            MarketInsight(
                title="경쟁사 신규 진입",
                description="반경 500m 내에 동종 업체가 새로 개업했습니다.",
                impact="주의",
                confidence=0.95,
                source="경쟁사 모니터링"
            ),
            MarketInsight(
                title="계절적 수요 증가 예상",
                description="다음 달 해당 업종의 수요가 20% 증가할 것으로 예측됩니다.",
                impact="긍정적",
                confidence=0.75,
                source="트렌드 분석"
            )
        ]
        
        # 추천 액션
        recommended_actions = [
            "20대 여성을 타겟으로 한 인스타그램 마케팅 강화",
            "경쟁사 대비 차별화 요소 발굴 및 강화",
            "계절적 수요 증가에 대비한 재고 및 인력 준비",
            "고객 리뷰 관리 시스템 구축",
            "SNS 콘텐츠 게시 빈도 증가"
        ]
        
        # 종합 성과 점수 (0-100)
        performance_score = (
            key_metrics["market_potential"] * 30 +
            key_metrics["trend_score"] * 25 +
            key_metrics["engagement_rate"] * 100 * 25 +
            key_metrics["content_performance"] * 20
        )
        
        return DashboardResponse(
            business_id=business_id,
            last_updated=datetime.now(),
            key_metrics=key_metrics,
            recent_insights=recent_insights,
            recommended_actions=recommended_actions,
            performance_score=min(100, max(0, performance_score))
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"대시보드 데이터 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/sample-data/{data_type}")
async def get_sample_data(data_type: str):
    """
    샘플 데이터 제공
    
    차트 및 시각화를 위한 샘플 데이터를 제공합니다.
    """
    sample_data = {
        "age_distribution": {
            "labels": ["10대", "20대", "30대", "40대", "50대", "60대+"],
            "data": [5, 25, 30, 20, 15, 5],
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]
        },
        "time_traffic": {
            "labels": ["6시", "9시", "12시", "15시", "18시", "21시", "24시"],
            "data": [10, 30, 80, 50, 70, 40, 20],
            "colors": ["#667eea", "#764ba2"]
        },
        "seasonal_trends": {
            "labels": ["봄", "여름", "가을", "겨울"],
            "data": [110, 90, 120, 80],
            "colors": ["#56ab2f", "#f093fb", "#fad961", "#a8edea"]
        },
        "competitor_comparison": {
            "labels": ["가격", "품질", "서비스", "접근성", "브랜드"],
            "your_business": [80, 90, 85, 75, 60],
            "competitor_avg": [70, 75, 80, 85, 80]
        },
        "keyword_cloud": [
            {"text": "맛있는", "value": 100},
            {"text": "친절한", "value": 80},
            {"text": "저렴한", "value": 60},
            {"text": "깨끗한", "value": 70},
            {"text": "빠른", "value": 50},
            {"text": "신선한", "value": 90},
            {"text": "정성스러운", "value": 75},
            {"text": "편리한", "value": 55}
        ]
    }
    
    if data_type not in sample_data:
        raise HTTPException(
            status_code=404,
            detail=f"'{data_type}' 샘플 데이터를 찾을 수 없습니다."
        )
    
    return {
        "data_type": data_type,
        "data": sample_data[data_type],
        "generated_at": datetime.now().isoformat()
    }

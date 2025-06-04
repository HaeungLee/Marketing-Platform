from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class TargetCustomerAnalysis:
    """타겟 고객 분석 결과"""
    primary_target: str
    secondary_target: str
    strategy: List[str]
    confidence: int
    data_source: str
    region_analysis: Optional[Dict[str, Any]] = None

@dataclass
class LocationRecommendation:
    """입지 추천 결과"""
    recommended_areas: List[Dict[str, Any]]
    analysis_metadata: Dict[str, Any]
    reasons: List[str]

@dataclass
class MarketingTiming:
    """마케팅 타이밍 분석 결과"""
    best_days: List[str]
    best_hours: List[str]
    seasonal_trends: str
    confidence: int
    data_source: str
    detailed_analysis: Optional[Dict[str, Any]] = None

@dataclass
class BusinessInsight:
    """종합 비즈니스 인사이트"""
    target_customer: TargetCustomerAnalysis
    location: LocationRecommendation
    timing: MarketingTiming
    summary: Dict[str, Any]
    created_at: datetime

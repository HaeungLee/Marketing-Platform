from pytrends.request import TrendReq
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class PyTrendsService:
    """Google Trends 데이터 수집 서비스"""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='ko', tz=540)  # 한국어, UTC+9
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    async def get_business_trends(
        self, 
        business_keywords: List[str], 
        timeframe: str = 'today 12-m',
        geo: str = 'KR'
    ) -> Dict:
        """업종별 트렌드 데이터 조회"""
        
        try:
            # 비동기적으로 실행
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                self._fetch_trends_data,
                business_keywords, 
                timeframe, 
                geo
            )
            return result
            
        except Exception as e:
            logger.error(f"트렌드 데이터 조회 오류: {str(e)}")
            return {"error": str(e), "data": None}
    
    def _fetch_trends_data(
        self, 
        keywords: List[str], 
        timeframe: str, 
        geo: str
    ) -> Dict:
        """실제 트렌드 데이터 조회 (동기 함수)"""
        
        # 키워드는 최대 5개까지만 지원
        keywords = keywords[:5]
        
        try:
            # Interest over time
            self.pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
            
            # 시간별 관심도
            interest_over_time = self.pytrends.interest_over_time()
            
            # 지역별 관심도
            interest_by_region = self.pytrends.interest_by_region(
                resolution='REGION', 
                inc_low_vol=True, 
                inc_geo_code=True
            )
            
            # 관련 키워드
            related_queries = {}
            try:
                related_queries = self.pytrends.related_queries()
            except Exception as e:
                logger.warning(f"관련 키워드 조회 실패: {str(e)}")
            
            # 데이터 처리
            result = {
                "timeframe": timeframe,
                "geo": geo,
                "keywords": keywords,
                "interest_over_time": self._process_time_series(interest_over_time),
                "interest_by_region": self._process_regional_data(interest_by_region),
                "related_queries": self._process_related_queries(related_queries),
                "summary": self._generate_summary(interest_over_time, keywords)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"트렌드 데이터 처리 오류: {str(e)}")
            raise
    
    def _process_time_series(self, df: pd.DataFrame) -> List[Dict]:
        """시계열 데이터 처리"""
        if df.empty:
            return []
        
        # 'isPartial' 컬럼 제거
        if 'isPartial' in df.columns:
            df = df.drop('isPartial', axis=1)
        
        result = []
        for index, row in df.iterrows():
            data_point = {
                "date": index.strftime('%Y-%m-%d'),
                "values": {}
            }
            
            for keyword in df.columns:
                data_point["values"][keyword] = int(row[keyword]) if pd.notna(row[keyword]) else 0
                
            result.append(data_point)
        
        return result
    
    def _process_regional_data(self, df: pd.DataFrame) -> List[Dict]:
        """지역별 데이터 처리"""
        if df.empty:
            return []
        
        result = []
        for index, row in df.iterrows():
            region_data = {
                "region": index,
                "values": {}
            }
            
            for keyword in df.columns:
                region_data["values"][keyword] = int(row[keyword]) if pd.notna(row[keyword]) else 0
                
            result.append(region_data)
        
        # 관심도 높은 순으로 정렬
        result.sort(key=lambda x: sum(x["values"].values()), reverse=True)
        return result[:10]  # 상위 10개 지역만
    
    def _process_related_queries(self, related_queries: Dict) -> Dict:
        """관련 검색어 처리"""
        processed = {}
        
        for keyword, queries in related_queries.items():
            processed[keyword] = {
                "top": [],
                "rising": []
            }
            
            if queries.get('top') is not None and not queries['top'].empty:
                processed[keyword]["top"] = queries['top'].head(5).to_dict('records')
            
            if queries.get('rising') is not None and not queries['rising'].empty:
                processed[keyword]["rising"] = queries['rising'].head(5).to_dict('records')
        
        return processed
    
    def _generate_summary(self, df: pd.DataFrame, keywords: List[str]) -> Dict:
        """트렌드 요약 생성"""
        if df.empty:
            return {}
        
        # 'isPartial' 컬럼 제거
        if 'isPartial' in df.columns:
            df = df.drop('isPartial', axis=1)
        
        summary = {}
        
        for keyword in keywords:
            if keyword in df.columns:
                values = df[keyword].dropna()
                if len(values) > 0:
                    current_value = values.iloc[-1]
                    avg_value = values.mean()
                    max_value = values.max()
                    min_value = values.min()
                    
                    # 트렌드 방향 계산
                    if len(values) >= 4:
                        recent_trend = values.tail(4).mean()
                        previous_trend = values.head(-4).tail(4).mean() if len(values) >= 8 else avg_value
                        trend_direction = "상승" if recent_trend > previous_trend else "하락"
                    else:
                        trend_direction = "데이터 부족"
                    
                    summary[keyword] = {
                        "current_interest": int(current_value),
                        "average_interest": round(avg_value, 1),
                        "max_interest": int(max_value),
                        "min_interest": int(min_value),
                        "trend_direction": trend_direction,
                        "volatility": round(values.std(), 1) if len(values) > 1 else 0
                    }
        
        return summary
    
    async def get_business_type_trends(self, business_type: str) -> Dict:
        """특정 업종의 트렌드 분석"""
        
        # 업종별 관련 키워드 매핑
        business_keywords_map = {
            "카페": ["카페", "커피숍", "아메리카노", "원두", "테이크아웃"],
            "음식점": ["맛집", "음식점", "배달", "포장", "레스토랑"],
            "편의점": ["편의점", "24시간", "생활용품", "택배", "무인점포"],
            "미용실": ["미용실", "헤어샵", "염색", "펌", "헤어스타일"],
            "치킨": ["치킨", "후라이드", "양념치킨", "배달치킨", "통닭"],
            "베이커리": ["베이커리", "빵집", "디저트", "케이크", "크로아상"],
        }
        
        keywords = business_keywords_map.get(business_type, [business_type])
        
        try:
            trends_data = await self.get_business_trends(keywords)
            
            # 업종별 인사이트 추가
            if "summary" in trends_data and trends_data["summary"]:
                trends_data["business_insights"] = self._generate_business_insights(
                    business_type, 
                    trends_data["summary"]
                )
            
            return trends_data
            
        except Exception as e:
            logger.error(f"업종 트렌드 분석 오류: {str(e)}")
            return {"error": str(e)}
    
    def _generate_business_insights(self, business_type: str, summary: Dict) -> Dict:
        """업종별 비즈니스 인사이트 생성"""
        
        insights = {
            "market_status": "",
            "recommendations": [],
            "opportunity_keywords": [],
            "risk_factors": []
        }
        
        # 전체 관심도 평균 계산
        avg_interests = [data["average_interest"] for data in summary.values()]
        overall_avg = sum(avg_interests) / len(avg_interests) if avg_interests else 0
        
        # 시장 상태 분석
        if overall_avg >= 70:
            insights["market_status"] = "매우 활발한 시장"
            insights["recommendations"].append("경쟁이 치열하므로 차별화 전략 필요")
        elif overall_avg >= 50:
            insights["market_status"] = "안정적인 시장"
            insights["recommendations"].append("꾸준한 마케팅으로 시장 점유율 확대")
        elif overall_avg >= 30:
            insights["market_status"] = "성장 가능성이 있는 시장"
            insights["recommendations"].append("적극적인 마케팅으로 시장 진입 기회")
        else:
            insights["market_status"] = "틈새 시장"
            insights["recommendations"].append("특화된 서비스로 고객층 확보")
        
        # 상승 트렌드 키워드 찾기
        for keyword, data in summary.items():
            if data["trend_direction"] == "상승":
                insights["opportunity_keywords"].append(keyword)
            elif data["volatility"] > 20:
                insights["risk_factors"].append(f"{keyword} 키워드 변동성 높음")
        
        # 업종별 맞춤 추천
        business_specific_recommendations = {
            "카페": ["모바일 주문 시스템 도입", "시즌 메뉴 개발", "배달 서비스 강화"],
            "음식점": ["온라인 리뷰 관리", "배달앱 최적화", "포장 메뉴 개발"],
            "편의점": ["24시간 운영", "배달 서비스", "무인 결제 시스템"],
        }
        
        if business_type in business_specific_recommendations:
            insights["recommendations"].extend(
                business_specific_recommendations[business_type]
            )
        
        return insights 
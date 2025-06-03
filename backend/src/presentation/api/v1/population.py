"""
인구 통계 관련 API 엔드포인트
"""
import logging
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ....domain.schemas.population import (
    PopulationStatisticsResponse,
    LocationResponse
)
from ....domain.models.population import PopulationStatistics
from ....config.database import get_db

# 로거 설정
logger = logging.getLogger(__name__)
router = APIRouter(tags=["인구통계"])

@router.get("/locations", response_model=LocationResponse, status_code=status.HTTP_200_OK)
async def get_locations(
    province: Optional[str] = None,
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    행정구역 목록 조회
    - province: 시/도 이름 (예: '서울특별시')
    - city: 시/군/구 이름 (예: '종로구')
    """
    try:
        logger.info(f"[API] get_locations - province: {province}, city: {city}")
        
        # 1. 시/도 목록 조회 (항상 반환)
        try:
            provinces_result = db.query(PopulationStatistics.province)\
                .distinct()\
                .order_by(PopulationStatistics.province)\
                .all()
            provinces = [p[0] for p in provinces_result if p[0]]
            logger.info(f"Found {len(provinces)} provinces")
        except Exception as e:
            logger.error(f"Error fetching provinces: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "시/도 목록을 가져오는 중 오류가 발생했습니다."}
            )
        
        # 기본값으로 빈 딕셔너리 초기화
        cities = {}
        districts = {}
        
        # 2. 시/군/구 목록 조회 (province가 제공된 경우)
        if province:
            try:
                cities_result = db.query(PopulationStatistics.city)\
                    .filter(PopulationStatistics.province == province)\
                    .distinct()\
                    .order_by(PopulationStatistics.city)\
                    .all()
                cities_list = [c[0] for c in cities_result if c[0]]
                cities[province] = cities_list
                logger.info(f"Found {len(cities_list)} cities for province {province}")
                
                # 3. 읍면동 목록 조회 (province와 city가 모두 제공된 경우)
                if city:
                    try:
                        districts_result = db.query(PopulationStatistics.district)\
                            .filter(
                                PopulationStatistics.province == province,
                                PopulationStatistics.city == city
                            )\
                            .distinct()\
                            .order_by(PopulationStatistics.district)\
                            .all()
                        districts_list = [d[0] for d in districts_result if d[0]]
                        if province not in districts:
                            districts[province] = {}
                        districts[province][city] = districts_list
                        logger.info(f"Found {len(districts_list)} districts for {province} {city}")
                    except Exception as e:
                        logger.error(f"Error fetching districts: {str(e)}", exc_info=True)
                        districts[province] = {city: []}
            except Exception as e:
                logger.error(f"Error fetching cities: {str(e)}", exc_info=True)
                cities[province] = []
        
        # 4. 결과 반환
        return LocationResponse(
            provinces=provinces,
            cities=cities,
            districts=districts
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Failed to fetch location data: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "행정구역 정보를 가져오는 중 오류가 발생했습니다.",
                "error": str(e)
            }
        )

@router.get("/statistics", response_model=List[PopulationStatisticsResponse])
async def get_population_statistics(
    province: str | None = None,
    city: str | None = None,
    district: str | None = None,
    reference_date: date | None = None,
    db: Session = Depends(get_db)
):
    """인구 통계 데이터 조회"""
    try:
        logger.info(f"[API] get_population_statistics - province: {province}, city: {city}, district: {district}")
        
        query = db.query(PopulationStatistics)
        
        if province:
            logger.info(f"Filtering by province: {province}")
            query = query.filter(PopulationStatistics.province == province.strip())
        if city:
            logger.info(f"Filtering by city: {city}")
            query = query.filter(PopulationStatistics.city == city.strip())
        if district:
            logger.info(f"Filtering by district: {district}")
            query = query.filter(PopulationStatistics.district == district.strip())
        if reference_date:
            logger.info(f"Filtering by reference_date: {reference_date}")
            query = query.filter(PopulationStatistics.reference_date == reference_date)
        
        # 최신 데이터순으로 정렬
        query = query.order_by(PopulationStatistics.reference_date.desc())
        
        # SQL 쿼리 로깅
        logger.info(f"Executing SQL: {str(query.statement.compile(compile_kwargs={"literal_binds": True}))}")
        
        results = query.all()
        logger.info(f"Found {len(results)} matching records")
        
        if not results:
            error_msg = f"No data found for - Province: {province}, City: {city}, District: {district}"
            logger.warning(error_msg)
            raise HTTPException(status_code=404, detail=error_msg)
            
        # 결과 로깅 (첫 번째 레코드만 로그에 기록)
        if results:
            first_result = results[0]
            logger.info(f"First result - Province: {first_result.province}, City: {first_result.city}, District: {first_result.district}")
            
        return results
        
    except HTTPException as e:
        logger.error(f"HTTP Exception: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

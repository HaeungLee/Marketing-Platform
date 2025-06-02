"""
인구 통계 관련 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from domain.schemas.population import (
    PopulationStatisticsResponse,
    PopulationStatisticsFilter,
    LocationResponse
)
from domain.models.population import PopulationStatistics
from config.database import get_db

router = APIRouter(prefix="/population", tags=["population"])

@router.get("/locations", response_model=LocationResponse)
async def get_locations(
    province: str | None = None,
    city: str | None = None,
    db: Session = Depends(get_db)
):
    """행정구역 목록 조회"""
    try:
        query = db.query(PopulationStatistics)
        
        # 고유한 시/도 목록
        provinces = db.query(PopulationStatistics.province).distinct().all()
        provinces = [p[0] for p in provinces]
        
        # 특정 시/도가 선택된 경우
        cities = None
        districts = None
        
        if province:
            # 해당 시/도의 시/군/구 목록
            cities = db.query(PopulationStatistics.city)\
                .filter(PopulationStatistics.province == province)\
                .distinct().all()
            cities = [c[0] for c in cities]
            
            if city:
                # 해당 시/군/구의 읍/면/동 목록
                districts = db.query(PopulationStatistics.district)\
                    .filter(PopulationStatistics.province == province)\
                    .filter(PopulationStatistics.city == city)\
                    .distinct().all()
                districts = [d[0] for d in districts]
        
        return LocationResponse(
            provinces=provinces,
            cities=cities,
            districts=districts
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        query = db.query(PopulationStatistics)
        
        if province:
            query = query.filter(PopulationStatistics.province == province)
        if city:
            query = query.filter(PopulationStatistics.city == city)
        if district:
            query = query.filter(PopulationStatistics.district == district)
        if reference_date:
            query = query.filter(PopulationStatistics.reference_date == reference_date)
            
        # 최신 데이터순으로 정렬
        query = query.order_by(PopulationStatistics.reference_date.desc())
        
        results = query.all()
        if not results:
            raise HTTPException(status_code=404, detail="해당 지역의 인구 통계 데이터를 찾을 수 없습니다.")
            
        return results
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from domain.schemas.population import PopulationStatisticsResponse, PopulationStatisticsFilter
from domain.services.population_service import PopulationService
from interfaces.api.dependencies import get_db

router = APIRouter(prefix="/population", tags=["population"])

@router.get("/statistics", response_model=List[PopulationStatisticsResponse])
async def get_population_statistics(
    province: str | None = None,
    city: str | None = None,
    district: str | None = None,
    reference_date: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    filter_params = PopulationStatisticsFilter(
        province=province,
        city=city,
        district=district,
        reference_date=reference_date
    )
    population_service = PopulationService(db)
    return population_service.get_population_statistics(filter_params, skip, limit)

@router.get("/locations")
async def get_locations(db: Session = Depends(get_db)):
    population_service = PopulationService(db)
    return population_service.get_unique_locations()

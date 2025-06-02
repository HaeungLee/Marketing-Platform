from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.domain.models.population import PopulationStatistics
from src.domain.schemas.population import PopulationStatisticsFilter

class PopulationService:
    def __init__(self, db: Session):
        self.db = db

    def get_population_statistics(
        self,
        filter_params: PopulationStatisticsFilter,
        skip: int = 0,
        limit: int = 100
    ) -> List[PopulationStatistics]:
        query = self.db.query(PopulationStatistics)
        
        # Apply filters
        conditions = []
        if filter_params.province:
            conditions.append(PopulationStatistics.province == filter_params.province)
        if filter_params.city:
            conditions.append(PopulationStatistics.city == filter_params.city)
        if filter_params.district:
            conditions.append(PopulationStatistics.district == filter_params.district)
        if filter_params.reference_date:
            conditions.append(PopulationStatistics.reference_date == filter_params.reference_date)
        
        if conditions:
            query = query.filter(and_(*conditions))
        
        return query.offset(skip).limit(limit).all()

    def get_unique_locations(self) -> dict:
        provinces = self.db.query(PopulationStatistics.province).distinct().all()
        provinces = [p[0] for p in provinces]

        result = {
            "provinces": provinces,
            "cities": {},
            "districts": {}
        }

        for province in provinces:
            cities = self.db.query(PopulationStatistics.city)\
                .filter(PopulationStatistics.province == province)\
                .distinct().all()
            cities = [c[0] for c in cities]
            result["cities"][province] = cities

            result["districts"][province] = {}
            for city in cities:
                districts = self.db.query(PopulationStatistics.district)\
                    .filter(
                        PopulationStatistics.province == province,
                        PopulationStatistics.city == city
                    ).distinct().all()
                districts = [d[0] for d in districts]
                result["districts"][province][city] = districts

        return result

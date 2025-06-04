from datetime import date
from pydantic import BaseModel, Field

class PopulationStatisticsBase(BaseModel):
    administrative_code: str = Field(..., description="행정기관코드")
    reference_date: date = Field(..., description="기준연월")
    province: str = Field(..., description="시도명")
    city: str = Field(..., description="시군구명")
    district: str = Field(..., description="읍면동명")
    age_0_9_male: int = Field(..., description="0~9세 남자")
    age_10_19_male: int = Field(..., description="10~19세 남자")
    age_20_29_male: int = Field(..., description="20~29세 남자")
    age_30_39_male: int = Field(..., description="30~39세 남자")
    age_40_49_male: int = Field(..., description="40~49세 남자")
    age_50_59_male: int = Field(..., description="50~59세 남자")
    age_60_69_male: int = Field(..., description="60~69세 남자")
    age_70_79_male: int = Field(..., description="70~79세 남자")
    age_80_89_male: int = Field(..., description="80~89세 남자")
    age_90_99_male: int = Field(..., description="90~99세 남자")
    age_100_plus_male: int = Field(..., description="100세 이상 남자")
    age_0_9_female: int = Field(..., description="0~9세 여자")
    age_10_19_female: int = Field(..., description="10~19세 여자")
    age_20_29_female: int = Field(..., description="20~29세 여자")
    age_30_39_female: int = Field(..., description="30~39세 여자")
    age_40_49_female: int = Field(..., description="40~49세 여자")
    age_50_59_female: int = Field(..., description="50~59세 여자")
    age_60_69_female: int = Field(..., description="60~69세 여자")
    age_70_79_female: int = Field(..., description="70~79세 여자")
    age_80_89_female: int = Field(..., description="80~89세 여자")
    age_90_99_female: int = Field(..., description="90~99세 여자")
    age_100_plus_female: int = Field(..., description="100세 이상 여자")
    total_population: int = Field(..., description="총인구수")
    total_male: int = Field(..., description="남자총합")
    total_female: int = Field(..., description="여자총합")

    class Config:
        from_attributes = True

class PopulationStatisticsResponse(PopulationStatisticsBase):
    id: int = Field(..., description="고유 식별자")

class PopulationStatisticsFilter(BaseModel):
    province: str | None = Field(None, description="시도명")
    city: str | None = Field(None, description="시군구명")
    district: str | None = Field(None, description="읍면동명")
    reference_date: date | None = Field(None, description="기준연월")

class LocationResponse(BaseModel):
    provinces: list[str] = Field(..., description="시도명 목록")
    cities: dict[str, list[str]] = Field(..., description="시도별 시군구명 목록")
    districts: dict[str, dict[str, list[str]]] = Field(..., description="시도, 시군구별 읍면동명 목록")

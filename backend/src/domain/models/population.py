from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class PopulationStatistics(Base):
    __tablename__ = "population_statistics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    administrative_code = Column(String(20), nullable=False, index=True)
    reference_date = Column(Date, nullable=False, index=True)
    province = Column(String(20), nullable=False)
    city = Column(String(20), nullable=False)
    district = Column(String(20), nullable=False)
    
    # Age groups - Male
    age_0_9_male = Column(Integer, nullable=False)
    age_10_19_male = Column(Integer, nullable=False)
    age_20_29_male = Column(Integer, nullable=False)
    age_30_39_male = Column(Integer, nullable=False)
    age_40_49_male = Column(Integer, nullable=False)
    age_50_59_male = Column(Integer, nullable=False)
    age_60_69_male = Column(Integer, nullable=False)
    age_70_79_male = Column(Integer, nullable=False)
    age_80_89_male = Column(Integer, nullable=False)
    age_90_99_male = Column(Integer, nullable=False)
    age_100_plus_male = Column(Integer, nullable=False)
    
    # Age groups - Female
    age_0_9_female = Column(Integer, nullable=False)
    age_10_19_female = Column(Integer, nullable=False)
    age_20_29_female = Column(Integer, nullable=False)
    age_30_39_female = Column(Integer, nullable=False)
    age_40_49_female = Column(Integer, nullable=False)
    age_50_59_female = Column(Integer, nullable=False)
    age_60_69_female = Column(Integer, nullable=False)
    age_70_79_female = Column(Integer, nullable=False)
    age_80_89_female = Column(Integer, nullable=False)
    age_90_99_female = Column(Integer, nullable=False)
    age_100_plus_female = Column(Integer, nullable=False)
    
    # Totals
    total_population = Column(Integer, nullable=False)
    total_male = Column(Integer, nullable=False)
    total_female = Column(Integer, nullable=False)

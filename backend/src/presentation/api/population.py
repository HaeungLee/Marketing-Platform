from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import asyncpg
import os
from datetime import datetime

router = APIRouter(tags=["population"])

# 데이터베이스 연결 설정
DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', '1234')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'marketing_platform')}"

async def get_db_connection():
    try:
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@router.get("/locations")
async def get_locations(
    province: Optional[str] = Query(None, description="시도명"),
    city: Optional[str] = Query(None, description="시군구명")
):
    """지역 정보를 조회합니다."""
    
    conn = await get_db_connection()
    try:
        if province is None:
            # 모든 시도 반환
            provinces_query = "SELECT DISTINCT province FROM population_statistics ORDER BY province"
            provinces_result = await conn.fetch(provinces_query)
            provinces = [row['province'] for row in provinces_result]
            
            return {
                "provinces": provinces,
                "cities": [],
                "districts": []
            }
        elif city is None:
            # 특정 시도의 시군구 반환
            cities_query = "SELECT DISTINCT city FROM population_statistics WHERE province = $1 ORDER BY city"
            cities_result = await conn.fetch(cities_query, province)
            cities = [row['city'] for row in cities_result]
            
            return {
                "provinces": [],
                "cities": cities,
                "districts": []
            }
        else:
            # 특정 시군구의 읍면동 반환
            districts_query = "SELECT DISTINCT district FROM population_statistics WHERE province = $1 AND city = $2 ORDER BY district"
            districts_result = await conn.fetch(districts_query, province, city)
            districts = [row['district'] for row in districts_result]
            
            return {
                "provinces": [],
                "cities": [],
                "districts": districts
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch locations: {str(e)}")
    finally:
        await conn.close()

@router.get("/statistics")
async def get_population_statistics(
    province: Optional[str] = Query(None, description="시도명"),
    city: Optional[str] = Query(None, description="도시명"),
    district: Optional[str] = Query(None, description="구/군명"),
    year: Optional[int] = Query(None, description="연도"),
    limit: int = Query(100, description="결과 제한")
):
    """인구 통계 데이터를 조회합니다."""
    
    conn = await get_db_connection()
    try:
        # 기본 쿼리
        query = """
            SELECT 
                administrative_code,
                reference_date,
                province,
                city,
                district,
                total_population,
                total_male,
                total_female,
                (age_0_9_male + age_0_9_female) as age_0_9_total,
                (age_10_19_male + age_10_19_female) as age_10_19_total,
                (age_20_29_male + age_20_29_female) as age_20_29_total,
                (age_30_39_male + age_30_39_female) as age_30_39_total,
                (age_40_49_male + age_40_49_female) as age_40_49_total,
                (age_50_59_male + age_50_59_female) as age_50_59_total,
                (age_60_69_male + age_60_69_female) as age_60_69_total,
                (age_70_79_male + age_70_79_female) as age_70_79_total,
                (age_80_89_male + age_80_89_female) as age_80_89_total,
                (age_90_99_male + age_90_99_female) as age_90_99_total,
                age_0_9_male, age_0_9_female,
                age_10_19_male, age_10_19_female,
                age_20_29_male, age_20_29_female,
                age_30_39_male, age_30_39_female,
                age_40_49_male, age_40_49_female,
                age_50_59_male, age_50_59_female,
                age_60_69_male, age_60_69_female,
                age_70_79_male, age_70_79_female,
                age_80_89_male, age_80_89_female,
                age_90_99_male, age_90_99_female,
                age_100_plus_male, age_100_plus_female
            FROM population_statistics
            WHERE 1=1
        """
        
        params = []
        param_count = 0
        
        if province:
            param_count += 1
            query += f" AND province = ${param_count}"
            params.append(province)
        
        if city:
            param_count += 1
            query += f" AND city = ${param_count}"
            params.append(city)
            
        if district:
            param_count += 1
            query += f" AND district = ${param_count}"
            params.append(district)
            
        if year:
            param_count += 1
            query += f" AND EXTRACT(YEAR FROM reference_date) = ${param_count}"
            params.append(year)
        
        query += f" ORDER BY reference_date DESC, city, district LIMIT ${param_count + 1}"
        params.append(limit)
        
        rows = await conn.fetch(query, *params)
        
        # 결과를 딕셔너리로 변환
        result = []
        for row in rows:
            result.append({
                "administrative_code": row["administrative_code"],
                "reference_date": row["reference_date"].isoformat() if row["reference_date"] else None,
                "province": row["province"],
                "city": row["city"], 
                "district": row["district"],
                "total_population": row["total_population"],
                "total_male": row["total_male"],
                "total_female": row["total_female"],
                "age_groups": {
                    "age_0_9": row["age_0_9_total"],
                    "age_10_19": row["age_10_19_total"],
                    "age_20_29": row["age_20_29_total"],
                    "age_30_39": row["age_30_39_total"],
                    "age_40_49": row["age_40_49_total"],
                    "age_50_59": row["age_50_59_total"],
                    "age_60_69": row["age_60_69_total"],
                    "age_70_79": row["age_70_79_total"],
                    "age_80_89": row["age_80_89_total"],
                    "age_90_99": row["age_90_99_total"],
                },
                "gender_breakdown": {
                    "age_0_9_male": row["age_0_9_male"],
                    "age_0_9_female": row["age_0_9_female"],
                    "age_10_19_male": row["age_10_19_male"],
                    "age_10_19_female": row["age_10_19_female"],
                    "age_20_29_male": row["age_20_29_male"],
                    "age_20_29_female": row["age_20_29_female"],
                    "age_30_39_male": row["age_30_39_male"],
                    "age_30_39_female": row["age_30_39_female"],
                    "age_40_49_male": row["age_40_49_male"],
                    "age_40_49_female": row["age_40_49_female"],
                    "age_50_59_male": row["age_50_59_male"],
                    "age_50_59_female": row["age_50_59_female"],
                    "age_60_69_male": row["age_60_69_male"],
                    "age_60_69_female": row["age_60_69_female"],
                    "age_70_79_male": row["age_70_79_male"],
                    "age_70_79_female": row["age_70_79_female"],
                    "age_80_89_male": row["age_80_89_male"],
                    "age_80_89_female": row["age_80_89_female"],
                    "age_90_99_male": row["age_90_99_male"],
                    "age_90_99_female": row["age_90_99_female"],
                    "age_100_plus_male": row["age_100_plus_male"],
                    "age_100_plus_female": row["age_100_plus_female"]
                }
            })
        
        return {
            "data": result,
            "total_count": len(result),
            "filters": {
                "province": province,
                "city": city,
                "district": district, 
                "year": year
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    finally:
        await conn.close()

@router.get("/age-distribution")
async def get_age_distribution(
    city: Optional[str] = Query(None, description="도시명"),
    top_districts: int = Query(10, description="상위 구/군 수")
):
    """연령대별 인구 분포를 조회합니다."""
    
    conn = await get_db_connection()
    try:
        query = """
            SELECT 
                city,
                district,
                total_population,
                (age_0_9_male + age_0_9_female) as age_0_9,
                (age_10_19_male + age_10_19_female) as age_10_19,
                (age_20_29_male + age_20_29_female) as age_20_29,
                (age_30_39_male + age_30_39_female) as age_30_39,
                (age_40_49_male + age_40_49_female) as age_40_49,
                (age_50_59_male + age_50_59_female) as age_50_59,
                (age_60_69_male + age_60_69_female) as age_60_69,
                (age_70_79_male + age_70_79_female) as age_70_79
            FROM population_statistics
            WHERE 1=1
        """
        
        params = []
        param_count = 0
        
        if city:
            param_count += 1
            query += f" AND city = ${param_count}"
            params.append(city)
        
        query += f" ORDER BY total_population DESC LIMIT ${param_count + 1}"
        params.append(top_districts)
        
        rows = await conn.fetch(query, *params)
        
        result = []
        for row in rows:
            result.append({
                "city": row["city"],
                "district": row["district"],
                "total_population": row["total_population"],
                "age_distribution": {
                    "0-9세": row["age_0_9"],
                    "10-19세": row["age_10_19"],
                    "20-29세": row["age_20_29"],
                    "30-39세": row["age_30_39"],
                    "40-49세": row["age_40_49"],
                    "50-59세": row["age_50_59"],
                    "60-69세": row["age_60_69"],
                    "70-79세": row["age_70_79"],
                }
            })
        
        return {
            "data": result,
            "total_count": len(result)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    finally:
        await conn.close()

@router.get("/income-distribution")
async def get_income_distribution(
    year: Optional[int] = Query(None, description="연도"),
    region: Optional[str] = Query(None, description="지역명")
):
    """소득 분포 데이터를 조회합니다."""
    
    conn = await get_db_connection()
    try:
        query = """
            SELECT 
                year,
                region,
                total_households,
                under_50,
                from_50_to_100,
                from_100_to_200,
                from_200_to_300,
                from_300_to_400,
                from_400_to_500,
                from_500_to_600,
                from_600_to_700,
                from_700_to_800,
                over_800
            FROM income_distribution
            WHERE 1=1
        """
        
        params = []
        param_count = 0
        
        if year:
            param_count += 1
            query += f" AND year = ${param_count}"
            params.append(year)
            
        if region:
            param_count += 1
            query += f" AND region ILIKE ${param_count}"
            params.append(f"%{region}%")
        
        query += " ORDER BY year DESC, total_households DESC"
        
        rows = await conn.fetch(query, *params)
        
        result = []
        for row in rows:
            result.append({
                "year": row["year"],
                "region": row["region"],
                "total_households": row["total_households"],
                "income_brackets": {
                    "50만원미만": row["under_50"],
                    "50-100만원": row["from_50_to_100"],
                    "100-200만원": row["from_100_to_200"],
                    "200-300만원": row["from_200_to_300"],
                    "300-400만원": row["from_300_to_400"],
                    "400-500만원": row["from_400_to_500"],
                    "500-600만원": row["from_500_to_600"],
                    "600-700만원": row["from_600_to_700"],
                    "700-800만원": row["from_700_to_800"],
                    "800만원이상": row["over_800"],
                }
            })
        
        return {
            "data": result,
            "total_count": len(result)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    finally:
        await conn.close()

@router.get("/summary")
async def get_population_summary():
    """인구 통계 요약 정보를 제공합니다."""
    
    conn = await get_db_connection()
    try:
        # 전체 통계
        summary_query = """
            SELECT 
                COUNT(*) as total_records,
                SUM(total_population) as total_population,
                AVG(total_population) as avg_population_per_district,
                COUNT(DISTINCT city) as total_cities,
                COUNT(DISTINCT district) as total_districts
            FROM population_statistics
        """
        
        # 상위 지역
        top_regions_query = """
            SELECT city, district, total_population
            FROM population_statistics
            ORDER BY total_population DESC
            LIMIT 10
        """
        
        summary_row = await conn.fetchrow(summary_query)
        top_regions = await conn.fetch(top_regions_query)
        
        return {
            "summary": {
                "total_records": summary_row["total_records"],
                "total_population": summary_row["total_population"],
                "avg_population_per_district": round(summary_row["avg_population_per_district"], 0) if summary_row["avg_population_per_district"] else 0,
                "total_cities": summary_row["total_cities"],
                "total_districts": summary_row["total_districts"]
            },
            "top_regions": [
                {
                    "city": row["city"],
                    "district": row["district"],
                    "population": row["total_population"]
                } for row in top_regions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    finally:
        await conn.close()

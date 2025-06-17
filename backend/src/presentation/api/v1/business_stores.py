from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List, Dict
import asyncpg
from datetime import datetime
import math
import logging

from ....config.settings import Settings
from ....infrastructure.api.business_store_client import BusinessStoreAPIClient
from ....domain.models.business_store import BusinessStore

router = APIRouter(tags=["business-stores"])
logger = logging.getLogger(__name__)

# 데이터베이스 연결 설정
settings = Settings()
DATABASE_URL = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")

async def get_db_connection():
    try:
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@router.get("/nearby")
async def get_nearby_stores(
    latitude: float = Query(..., description="위도"),
    longitude: float = Query(..., description="경도"), 
    radius_km: float = Query(1.0, description="반경 (km)"),
    business_type: Optional[str] = Query(None, description="업종 필터"),
    limit: int = Query(100, description="결과 제한")
):
    """주변 상가 정보 조회 (좌표 기반)"""
    
    conn = await get_db_connection()
    try:
        # 위도/경도를 이용한 거리 계산 쿼리 (서브쿼리로 수정)
        # Haversine 공식을 사용한 거리 계산
        distance_query = """
            SELECT * FROM (
                SELECT *,
                    (6371 * acos(
                        cos(radians($1)) * 
                        cos(radians(latitude)) * 
                        cos(radians(longitude) - radians($2)) + 
                        sin(radians($1)) * 
                        sin(radians(latitude))
                    )) as distance
                FROM business_stores
                WHERE business_status = '영업'
        """
        
        params = [latitude, longitude]
        param_count = 2
        
        if business_type:
            param_count += 1
            distance_query += f" AND business_name ILIKE ${param_count}"
            params.append(f"%{business_type}%")
        
        distance_query += f"""
            ) as stores_with_distance
            WHERE distance <= ${param_count + 1}
            ORDER BY distance ASC
            LIMIT ${param_count + 2}
        """
        
        params.extend([radius_km, limit])
        
        rows = await conn.fetch(distance_query, *params)
        
        # 결과 포맷
        stores = []
        for row in rows:
            stores.append({
                "id": row["id"],
                "store_name": row["store_name"],
                "business_name": row["business_name"],
                "business_code": row["business_code"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "road_address": row["road_address"],
                "jibun_address": row["jibun_address"],
                "sido_name": row["sido_name"],
                "sigungu_name": row["sigungu_name"],
                "dong_name": row["dong_name"],
                "building_name": row["building_name"],
                "floor_info": row["floor_info"],
                "business_status": row["business_status"],
                "open_date": row["open_date"].isoformat() if row["open_date"] else None,
                "distance_km": round(row["distance"], 2)
            })
            
        return {
            "stores": stores,
            "search_location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "search_radius_km": radius_km,
            "total_count": len(stores),
            "business_type_filter": business_type
        }
        
    except Exception as e:
        logger.error(f"주변 상가 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch nearby stores: {str(e)}")
    finally:
        await conn.close()

@router.get("/by-region")
async def get_stores_by_region(
    sido_name: Optional[str] = Query(None, description="시도명"),
    sigungu_name: Optional[str] = Query(None, description="시군구명"),
    dong_name: Optional[str] = Query(None, description="동명"),
    business_type: Optional[str] = Query(None, description="업종"),
    page: int = Query(1, description="페이지 번호"),
    page_size: int = Query(50, description="페이지 크기")
):
    """지역별 상가 정보 조회"""
    
    conn = await get_db_connection()
    try:
        # 기본 쿼리
        base_query = """
            SELECT *
            FROM business_stores
            WHERE business_status = '영업'
        """
        
        params = []
        param_count = 0
        
        if sido_name:
            param_count += 1
            base_query += f" AND sido_name = ${param_count}"
            params.append(sido_name)
            
        if sigungu_name:
            param_count += 1  
            base_query += f" AND sigungu_name = ${param_count}"
            params.append(sigungu_name)
            
        if dong_name:
            param_count += 1
            base_query += f" AND dong_name ILIKE ${param_count}"
            params.append(f"%{dong_name}%")
            
        if business_type:
            param_count += 1
            base_query += f" AND business_name ILIKE ${param_count}"
            params.append(f"%{business_type}%")
        
        # 전체 개수 조회
        count_query = base_query.replace("SELECT *", "SELECT COUNT(*)")
        total_count = await conn.fetchval(count_query, *params)
        
        # 페이징 처리
        offset = (page - 1) * page_size
        base_query += f" ORDER BY store_name LIMIT ${param_count + 1} OFFSET ${param_count + 2}"
        params.extend([page_size, offset])
        
        rows = await conn.fetch(base_query, *params)
        
        # 결과 포맷
        stores = []
        for row in rows:
            stores.append({
                "id": row["id"],
                "store_name": row["store_name"],
                "business_name": row["business_name"],
                "business_code": row["business_code"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "road_address": row["road_address"],
                "sido_name": row["sido_name"],
                "sigungu_name": row["sigungu_name"],
                "dong_name": row["dong_name"],
                "business_status": row["business_status"],
                "open_date": row["open_date"].isoformat() if row["open_date"] else None
            })
            
        return {
            "stores": stores,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": math.ceil(total_count / page_size)
            },
            "filters": {
                "sido_name": sido_name,
                "sigungu_name": sigungu_name,
                "dong_name": dong_name,
                "business_type": business_type
            }
        }
        
    except Exception as e:
        logger.error(f"지역별 상가 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch stores by region: {str(e)}")
    finally:
        await conn.close()

@router.get("/statistics")
async def get_business_statistics(
    sido_name: Optional[str] = Query(None, description="시도명"),
    sigungu_name: Optional[str] = Query(None, description="시군구명")
):
    """상가 통계 정보 조회"""
    
    conn = await get_db_connection()
    try:
        # 업종별 통계
        business_stats_query = """
            SELECT 
                business_name,
                COUNT(*) as store_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
            FROM business_stores
            WHERE business_status = '영업'
        """
        
        params = []
        param_count = 0
        
        if sido_name:
            param_count += 1
            business_stats_query += f" AND sido_name = ${param_count}"
            params.append(sido_name)
            
        if sigungu_name:
            param_count += 1
            business_stats_query += f" AND sigungu_name = ${param_count}"
            params.append(sigungu_name)
            
        business_stats_query += """
            GROUP BY business_name
            ORDER BY store_count DESC
            LIMIT 20
        """
        
        business_stats = await conn.fetch(business_stats_query, *params)
        
        # 지역별 통계 (시군구별)
        region_stats_query = """
            SELECT 
                sigungu_name,
                COUNT(*) as store_count
            FROM business_stores
            WHERE business_status = '영업'
        """
        
        if sido_name:
            region_stats_query += f" AND sido_name = ${1 if sido_name and not sigungu_name else ''}"
            
        region_stats_query += """
            GROUP BY sigungu_name
            ORDER BY store_count DESC
            LIMIT 20
        """
        
        region_params = [sido_name] if sido_name and not sigungu_name else []
        region_stats = await conn.fetch(region_stats_query, *region_params)
        
        return {
            "business_type_stats": [
                {
                    "business_name": row["business_name"],
                    "store_count": row["store_count"],
                    "percentage": row["percentage"]
                }
                for row in business_stats
            ],
            "region_stats": [
                {
                    "region_name": row["sigungu_name"],
                    "store_count": row["store_count"]
                }
                for row in region_stats
            ],
            "filters": {
                "sido_name": sido_name,
                "sigungu_name": sigungu_name
            }
        }
        
    except Exception as e:
        logger.error(f"상가 통계 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch business statistics: {str(e)}")
    finally:
        await conn.close()

@router.post("/sync-data")
async def sync_business_data(
    sido_cd: str = Query(..., description="시도코드"),
    sigungu_cd: Optional[str] = Query(None, description="시군구코드")
):
    """공공데이터 API에서 상가 정보 동기화"""
    
    try:
        # API 클라이언트로 데이터 조회
        api_client = BusinessStoreAPIClient()
        stores_data = await api_client.get_stores_by_region(
            sido_cd=sido_cd,
            sigungu_cd=sigungu_cd
        )
        
        if not stores_data:
            return {
                "message": "조회된 데이터가 없습니다",
                "synced_count": 0
            }
        
        # 데이터베이스에 저장
        conn = await get_db_connection()
        synced_count = 0
        
        try:
            for store in stores_data:
                # 중복 확인 (상가업소번호 기준)
                existing_store = await conn.fetchrow(
                    "SELECT id FROM business_stores WHERE store_number = $1",
                    store['store_number']
                )
                
                if existing_store:
                    # 업데이트
                    await conn.execute("""
                        UPDATE business_stores SET
                            store_name = $2, business_code = $3, business_name = $4,
                            longitude = $5, latitude = $6, jibun_address = $7, road_address = $8,
                            sido_name = $9, sigungu_name = $10, dong_name = $11,
                            building_name = $12, floor_info = $13, room_info = $14,
                            open_date = $15, close_date = $16, business_status = $17,
                            standard_industry_code = $18, commercial_category_code = $19,
                            updated_at = NOW()
                        WHERE store_number = $1
                    """, 
                        store['store_number'], store['store_name'], store['business_code'],
                        store['business_name'], store['longitude'], store['latitude'],
                        store['jibun_address'], store['road_address'], store['sido_name'],
                        store['sigungu_name'], store['dong_name'], store['building_name'],
                        store['floor_info'], store['room_info'], store['open_date'],
                        store['close_date'], store['business_status'], 
                        store['standard_industry_code'], store['commercial_category_code']
                    )
                else:
                    # 신규 삽입
                    await conn.execute("""
                        INSERT INTO business_stores (
                            store_number, store_name, business_code, business_name,
                            longitude, latitude, jibun_address, road_address,
                            sido_name, sigungu_name, dong_name, building_name,
                            floor_info, room_info, open_date, close_date, business_status,
                            standard_industry_code, commercial_category_code
                        ) VALUES (
                            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19
                        )
                    """,
                        store['store_number'], store['store_name'], store['business_code'],
                        store['business_name'], store['longitude'], store['latitude'],
                        store['jibun_address'], store['road_address'], store['sido_name'],
                        store['sigungu_name'], store['dong_name'], store['building_name'],
                        store['floor_info'], store['room_info'], store['open_date'],
                        store['close_date'], store['business_status'],
                        store['standard_industry_code'], store['commercial_category_code']
                    )
                
                synced_count += 1
                
        finally:
            await conn.close()
            
        return {
            "message": f"상가 정보 동기화 완료",
            "synced_count": synced_count,
            "total_fetched": len(stores_data)
        }
        
    except Exception as e:
        logger.error(f"데이터 동기화 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data sync failed: {str(e)}") 
"""
가상 데이터를 business_stores 테이블에 적재하는 스크립트
"""
import pandas as pd
import asyncpg
import asyncio
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://marketing_user:marketing_password@localhost:5432/marketing_db"

async def load_sample_business_data():
    """가상 상가 데이터를 데이터베이스에 적재"""
    
    try:
        # CSV 파일 읽기
        df = pd.read_csv('sbiz_가상데이터.csv')
        logger.info(f"CSV 파일에서 {len(df)}개 레코드 로드")
        
        # 데이터베이스 연결
        conn = await asyncpg.connect(DATABASE_URL)
        logger.info("데이터베이스 연결 성공")
        
        # 기존 데이터 삭제 (테스트용)
        await conn.execute("DELETE FROM business_stores WHERE store_number LIKE '116801%'")
        logger.info("기존 테스트 데이터 삭제")
        
        # 데이터 변환 및 삽입
        inserted_count = 0
        
        for _, row in df.iterrows():
            try:
                # 필드 매핑 (CSV -> DB)
                store_data = {
                    'store_number': row['bizesId'],
                    'store_name': row['bizesNm'],
                    'business_code': row['indsLclsCd'],
                    'business_name': row['indsLclsNm'],
                    'longitude': float(row['lon']),
                    'latitude': float(row['lat']),
                    'jibun_address': row['lnmadr'],
                    'road_address': row['rdnmadr'],
                    'sido_name': row['ctprvnNm'],
                    'sigungu_name': row['signguNm'],
                    'dong_name': row['adongNm'],
                    'building_name': row['bldNm'] if pd.notna(row['bldNm']) else None,
                    'floor_info': row['flrInfo'] if pd.notna(row['flrInfo']) else None,
                    'room_info': row['hoInfo'] if pd.notna(row['hoInfo']) else None,
                    'business_status': row['trdStateNm'],
                    'standard_industry_code': row['ksicCd'],
                    'commercial_category_code': row['ctgryThreeNm']
                }
                
                # 개업일자 변환
                open_date = None
                if pd.notna(row['opnDt']) and row['opnDt']:
                    try:
                        open_date = datetime.strptime(str(row['opnDt']), '%Y%m%d').date()
                    except:
                        pass
                
                # 폐업일자 변환
                close_date = None
                if pd.notna(row['clsDt']) and row['clsDt']:
                    try:
                        close_date = datetime.strptime(str(row['clsDt']), '%Y%m%d').date()
                    except:
                        pass
                
                # 데이터베이스 삽입
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
                    store_data['store_number'], store_data['store_name'], 
                    store_data['business_code'], store_data['business_name'],
                    store_data['longitude'], store_data['latitude'],
                    store_data['jibun_address'], store_data['road_address'],
                    store_data['sido_name'], store_data['sigungu_name'], store_data['dong_name'],
                    store_data['building_name'], store_data['floor_info'], store_data['room_info'],
                    open_date, close_date, store_data['business_status'],
                    store_data['standard_industry_code'], store_data['commercial_category_code']
                )
                
                inserted_count += 1
                
                if inserted_count % 10 == 0:
                    logger.info(f"진행률: {inserted_count}/{len(df)}")
                    
            except Exception as e:
                logger.error(f"행 {inserted_count + 1} 처리 오류: {e}")
                continue
        
        # 삽입 결과 확인
        total_count = await conn.fetchval("SELECT COUNT(*) FROM business_stores")
        
        logger.info(f"✅ 데이터 적재 완료!")
        logger.info(f"   - 삽입된 레코드: {inserted_count}개")
        logger.info(f"   - 전체 레코드: {total_count}개")
        
        # 샘플 데이터 확인
        logger.info("\n📋 삽입된 데이터 샘플:")
        sample_rows = await conn.fetch("""
            SELECT store_name, business_name, sido_name, sigungu_name, business_status
            FROM business_stores 
            WHERE store_number LIKE '116801%'
            LIMIT 5
        """)
        
        for row in sample_rows:
            logger.info(f"   - {row['store_name']} ({row['business_name']}) - {row['sido_name']} {row['sigungu_name']} - {row['business_status']}")
        
        # 업종별 통계
        logger.info("\n📊 업종별 분포:")
        business_stats = await conn.fetch("""
            SELECT business_name, COUNT(*) as count
            FROM business_stores 
            WHERE store_number LIKE '116801%'
            GROUP BY business_name
            ORDER BY count DESC
        """)
        
        for row in business_stats:
            logger.info(f"   - {row['business_name']}: {row['count']}개")
            
    except Exception as e:
        logger.error(f"❌ 데이터 적재 실패: {e}")
        raise
    finally:
        if 'conn' in locals():
            await conn.close()
            logger.info("데이터베이스 연결 종료")

async def verify_data_integration():
    """적재된 데이터가 API에서 정상 조회되는지 확인"""
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        logger.info("\n🔍 데이터 통합 검증:")
        
        # 1. 전체 개수 확인
        total_count = await conn.fetchval("SELECT COUNT(*) FROM business_stores")
        logger.info(f"   - 전체 상가 수: {total_count:,}개")
        
        # 2. 지역별 분포
        region_stats = await conn.fetch("""
            SELECT sido_name, sigungu_name, COUNT(*) as count
            FROM business_stores
            GROUP BY sido_name, sigungu_name
            ORDER BY count DESC
            LIMIT 10
        """)
        
        logger.info("   - 지역별 상위 10개:")
        for row in region_stats:
            logger.info(f"     {row['sido_name']} {row['sigungu_name']}: {row['count']}개")
        
        # 3. GPS 좌표 기반 근처 상가 테스트 (강남역 기준)
        gangnam_lat, gangnam_lon = 37.4979, 127.0276
        nearby_stores = await conn.fetch("""
            SELECT store_name, business_name,
                   (6371 * acos(
                       cos(radians($1)) * 
                       cos(radians(latitude)) * 
                       cos(radians(longitude) - radians($2)) + 
                       sin(radians($1)) * 
                       sin(radians(latitude))
                   )) as distance
            FROM business_stores
            WHERE business_status = '영업'
            HAVING distance <= 1.0
            ORDER BY distance
            LIMIT 10
        """, gangnam_lat, gangnam_lon)
        
        logger.info(f"\n   - 강남역 반경 1km 내 상가 ({len(nearby_stores)}개):")
        for row in nearby_stores:
            logger.info(f"     {row['store_name']} ({row['business_name']}) - {row['distance']:.2f}km")
        
        # 4. 업종별 통계
        business_stats = await conn.fetch("""
            SELECT business_name, COUNT(*) as count,
                   ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
            FROM business_stores
            WHERE business_status = '영업'
            GROUP BY business_name
            ORDER BY count DESC
            LIMIT 10
        """)
        
        logger.info("\n   - 업종별 상위 10개:")
        for row in business_stats:
            logger.info(f"     {row['business_name']}: {row['count']}개 ({row['percentage']}%)")
            
        logger.info("\n✅ 데이터 통합 검증 완료!")
        
    except Exception as e:
        logger.error(f"❌ 검증 실패: {e}")
        raise
    finally:
        await conn.close()

async def main():
    """메인 실행 함수"""
    logger.info("🏪 가상 상가 데이터 적재 및 검증 시작")
    logger.info("=" * 60)
    
    # 1. 데이터 적재
    await load_sample_business_data()
    
    # 2. 통합 검증
    await verify_data_integration()
    
    logger.info("\n💡 다음 단계:")
    logger.info("   1. 백엔드 서버 시작: cd backend && python run.py")
    logger.info("   2. API 테스트: http://localhost:8000/docs")
    logger.info("   3. 프론트엔드에서 지도 연동 테스트")
    logger.info("   4. 실제 API 연동 계획 수립")
    logger.info("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 
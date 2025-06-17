#!/usr/bin/env python3
"""
소상공인시장진흥공단 API를 사용해서 실제 상가 데이터를 수집하고 DB에 저장하는 스크립트
"""
import asyncio
import asyncpg
from src.infrastructure.api.business_store_client import BusinessStoreAPIClient
from src.config.settings import Settings

async def load_business_data():
    """실제 상가 데이터 로드"""
    settings = Settings()
    db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    # API 클라이언트 초기화
    client = BusinessStoreAPIClient()
    
    # DB 연결
    conn = await asyncpg.connect(db_url)
    
    try:
        print("📍 실제 상가 데이터 수집 시작...")
        
        # 주요 지역별로 데이터 수집 (서울 각 구별로)
        seoul_districts = [
            ("11", "11680", "강남구"),    # 서울 강남구
            ("11", "11740", "강동구"),    # 서울 강동구
            ("11", "11305", "강북구"),    # 서울 강북구
            ("11", "11500", "강서구"),    # 서울 강서구
            ("11", "11620", "관악구"),    # 서울 관악구
            ("11", "11215", "광진구"),    # 서울 광진구
            ("11", "11530", "구로구"),    # 서울 구로구
            ("11", "11545", "금천구"),    # 서울 금천구
            ("11", "11350", "노원구"),    # 서울 노원구
            ("11", "11320", "도봉구"),    # 서울 도봉구
            ("11", "11230", "동대문구"),  # 서울 동대문구
            ("11", "11590", "동작구"),    # 서울 동작구
            ("11", "11440", "마포구"),    # 서울 마포구
            ("11", "11410", "서대문구"),  # 서울 서대문구
            ("11", "11650", "서초구"),    # 서울 서초구
            ("11", "11200", "성동구"),    # 서울 성동구
            ("11", "11290", "성북구"),    # 서울 성북구
            ("11", "11710", "송파구"),    # 서울 송파구
            ("11", "11470", "양천구"),    # 서울 양천구
            ("11", "11560", "영등포구"),  # 서울 영등포구
            ("11", "11170", "용산구"),    # 서울 용산구
            ("11", "11380", "은평구"),    # 서울 은평구
            ("11", "11110", "종로구"),    # 서울 종로구
            ("11", "11140", "중구"),      # 서울 중구
            ("11", "11260", "중랑구"),    # 서울 중랑구
        ]
        
        total_stores = 0
        
        for sido_cd, sigungu_cd, district_name in seoul_districts:
            try:
                print(f"📦 {district_name} 데이터 수집 중...")
                
                # API에서 상가 데이터 조회
                stores = await client.get_stores_by_region(
                    sido_cd=sido_cd,
                    sigungu_cd=sigungu_cd,
                    num_of_rows=1000  # 구별로 최대 1000개
                )
                
                if not stores:
                    print(f"⚠️  {district_name}: 데이터 없음")
                    continue
                
                # DB에 저장
                stored_count = 0
                for store in stores:
                    try:
                        # 중복 확인 후 삽입
                        insert_sql = """
                        INSERT INTO business_stores (
                            store_number, store_name, business_code, business_name,
                            longitude, latitude, jibun_address, road_address,
                            sido_name, sigungu_name, dong_name, building_name,
                            floor_info, room_info, open_date, close_date,
                            business_status, standard_industry_code, commercial_category_code
                        ) VALUES (
                            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                            $11, $12, $13, $14, $15, $16, $17, $18, $19
                        ) 
                        ON CONFLICT (store_number) DO UPDATE SET
                            store_name = EXCLUDED.store_name,
                            business_code = EXCLUDED.business_code,
                            business_name = EXCLUDED.business_name,
                            longitude = EXCLUDED.longitude,
                            latitude = EXCLUDED.latitude,
                            business_status = EXCLUDED.business_status
                        """
                        
                        await conn.execute(
                            insert_sql,
                            store.get('store_number'),
                            store.get('store_name'),
                            store.get('business_code'),
                            store.get('business_name'),
                            store.get('longitude'),
                            store.get('latitude'),
                            store.get('jibun_address'),
                            store.get('road_address'),
                            store.get('sido_name'),
                            store.get('sigungu_name'),
                            store.get('dong_name'),
                            store.get('building_name'),
                            store.get('floor_info'),
                            store.get('room_info'),
                            store.get('open_date'),
                            store.get('close_date'),
                            store.get('business_status', '영업'),
                            store.get('standard_industry_code'),
                            store.get('commercial_category_code')
                        )
                        stored_count += 1
                        
                    except Exception as e:
                        print(f"❌ 개별 상가 저장 오류: {e}")
                        continue
                
                total_stores += stored_count
                print(f"✅ {district_name}: {stored_count}개 상가 저장됨")
                
                # API 호출 제한을 위한 잠시 대기
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ {district_name} 처리 오류: {e}")
                continue
        
        print(f"\n🎉 전체 {total_stores}개 상가 데이터 수집 완료!")
        
        # 최종 통계 확인
        stats = await conn.fetch("""
            SELECT 
                COUNT(*) as total_stores,
                COUNT(DISTINCT business_name) as unique_businesses,
                COUNT(DISTINCT sigungu_name) as districts
            FROM business_stores
        """)
        
        if stats:
            stat = stats[0]
            print(f"📊 DB 통계:")
            print(f"   - 총 상가 수: {stat['total_stores']:,}개")
            print(f"   - 업종 수: {stat['unique_businesses']:,}개")
            print(f"   - 지역 수: {stat['districts']:,}개")
        
    except Exception as e:
        print(f"❌ 데이터 로드 오류: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(load_business_data()) 
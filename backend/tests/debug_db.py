import asyncpg
import asyncio

async def test_db():
    try:
        conn = await asyncpg.connect(
            host='localhost',
            port=5432, 
            database='marketing_platform',
            user='postgres',
            password='postgres'
        )
        print('✅ 데이터베이스 연결 성공')
        
        # 테스트 쿼리
        result = await conn.fetch('SELECT province, city, district FROM population_statistics LIMIT 3')
        print(f'✅ 쿼리 테스트 성공: {len(result)}개 결과')
        for row in result:
            print(f'  - {row["province"]} {row["city"]} {row["district"]}')
            
        await conn.close()
    except Exception as e:
        print(f'❌ 오류: {e}')
        import traceback
        traceback.print_exc()

asyncio.run(test_db())

import asyncpg
import asyncio
import os

async def check_table_data():
    DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', '1234')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'marketing_platform')}"
    
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # 테이블에 데이터가 있는지 확인
        count_query = "SELECT COUNT(*) FROM population_statistics"
        count_result = await conn.fetchval(count_query)
        print(f"Total records in population_statistics: {count_result}")
        
        if count_result > 0:
            # 몇 개 샘플 데이터 조회
            sample_query = "SELECT * FROM population_statistics LIMIT 3"
            sample_result = await conn.fetch(sample_query)
            print("\nSample data:")
            for row in sample_result:
                print(f"Province: {row['province']}, City: {row['city']}, District: {row['district']}, Total Population: {row.get('total_population', 'N/A')}")
        
        # 테이블 구조 확인
        columns_query = """
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'population_statistics'
            ORDER BY ordinal_position
        """
        columns_result = await conn.fetch(columns_query)
        print(f"\nTable columns ({len(columns_result)} total):")
        for row in columns_result:
            print(f"- {row['column_name']}: {row['data_type']}")
        
        await conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_table_data())

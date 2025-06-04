import psycopg2
import json

try:
    # 데이터베이스 연결
    conn = psycopg2.connect(
        host='localhost',
        database='marketing_platform',
        user='postgres',
        password='1234'
    )
    cur = conn.cursor()

    # 테이블 구조 확인
    print('=== 테이블 구조 ===')
    cur.execute("""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'population_statistics' 
        ORDER BY ordinal_position;
    """)
    columns = cur.fetchall()
    for col in columns:
        print(f'{col[0]:30} {col[1]:20} {col[2]}')

    print('\n=== 샘플 데이터 (첫 번째 레코드) ===')
    cur.execute('SELECT * FROM population_statistics LIMIT 1;')
    sample = cur.fetchone()
    if sample:
        for i, col in enumerate(columns):
            print(f'{col[0]:30} = {sample[i]}')

    print('\n=== 특정 지역 데이터 확인 (서울 강남구) ===')
    cur.execute("""
        SELECT province, city, district, 
               age_10_19_male, age_10_19_female,
               age_50_59_male, age_50_59_female,
               age_60_69_male, age_60_69_female,
               age_70_79_male, age_70_79_female
        FROM population_statistics 
        WHERE province = '서울특별시' AND city = '강남구' 
        LIMIT 5;
    """)
    data = cur.fetchall()
    print("Province, City, District, age_10_19_M, age_10_19_F, age_50_59_M, age_50_59_F, age_60_69_M, age_60_69_F, age_70_79_M, age_70_79_F")
    for row in data:
        print(row)

    print('\n=== 연령대별 컬럼명 확인 ===')
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'population_statistics' 
        AND column_name LIKE 'age_%'
        ORDER BY column_name;
    """)
    age_columns = cur.fetchall()
    print("연령대 관련 컬럼들:")
    for col in age_columns:
        print(f"  {col[0]}")

    conn.close()
    
except Exception as e:
    print(f"Error: {e}")

import psycopg2

try:
    # 데이터베이스 연결
    conn = psycopg2.connect(
        host='localhost',
        database='marketing_platform',
        user='postgres',
        password='1234'
    )
    cur = conn.cursor()

    print('=== 테이블 존재 확인 ===')
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    tables = cur.fetchall()
    print("Available tables:")
    for table in tables:
        print(f"  {table[0]}")

    if ('population_statistics',) in tables:
        print('\n=== population_statistics 테이블 구조 ===')
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'population_statistics' 
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  {col[0]} ({col[1]})")

        print('\n=== 첫 번째 레코드 확인 ===')
        cur.execute('SELECT * FROM population_statistics LIMIT 1;')
        sample = cur.fetchone()
        if sample:
            print("Sample data:")
            for i, col in enumerate(columns):
                print(f"  {col[0]}: {sample[i]}")
        else:
            print("No data found")

    conn.close()
    
except psycopg2.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")

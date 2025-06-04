#!/usr/bin/env python3
"""
데이터베이스 상태 확인 스크립트
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sys

# 데이터베이스 연결 설정
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/marketing_platform"

def check_database():
    """데이터베이스 연결 및 데이터 확인"""
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("=== 데이터베이스 연결 성공 ===")
        
        # 테이블 존재 확인
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'population_statistics'
        """)
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ population_statistics 테이블 존재")
            
            # 데이터 개수 확인
            cursor.execute("SELECT COUNT(*) as count FROM population_statistics")
            count_result = cursor.fetchone()
            data_count = count_result['count']
            
            print(f"📊 데이터 개수: {data_count}개")
            
            if data_count > 0:
                # 샘플 데이터 확인
                cursor.execute("SELECT * FROM population_statistics LIMIT 3")
                sample_data = cursor.fetchall()
                
                print("\n=== 샘플 데이터 ===")
                for i, row in enumerate(sample_data, 1):
                    print(f"\n{i}번째 레코드:")
                    print(f"  ID: {row['id']}")
                    print(f"  시도: {row['sido']}")
                    print(f"  시군구: {row['sigungu']}")
                    print(f"  읍면동: {row['eup_myeon_dong']}")
                    print(f"  총인구: {row['total_population']}")
                    
                # 컬럼 구조 확인
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'population_statistics'
                    ORDER BY ordinal_position
                """)
                columns = cursor.fetchall()
                
                print("\n=== 테이블 구조 ===")
                for col in columns:
                    print(f"  {col['column_name']}: {col['data_type']}")
                    
            else:
                print("❌ 테이블에 데이터가 없습니다!")
                print("CSV 데이터를 임포트해야 합니다.")
                
        else:
            print("❌ population_statistics 테이블이 존재하지 않습니다!")
            
        cursor.close()
        conn.close()
        
        return data_count > 0
        
    except Exception as e:
        print(f"❌ 데이터베이스 오류: {str(e)}")
        return False

def import_csv_data():
    """CSV 데이터 임포트"""
    print("\n=== CSV 데이터 임포트 시작 ===")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # CSV 파일 경로
        csv_file_path = "D:/FinalProjects/Marketing-Platform/docs/population_with_total_columns.csv"
        
        # 기존 데이터 삭제
        cursor.execute("DELETE FROM population_statistics")
        print("기존 데이터 삭제 완료")
        
        # CSV 데이터 읽기 및 삽입
        import csv
        import datetime
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            insert_count = 0
            for row in csv_reader:
                # 날짜 파싱
                reference_date = datetime.datetime.strptime(row['기준연월'], '%Y-%m-%d').date()
                
                # 데이터 삽입
                cursor.execute("""
                    INSERT INTO population_statistics (
                        administrative_code, reference_date, sido, sigungu, eup_myeon_dong,
                        age_0_9_male, age_0_9_female, age_10_19_male, age_10_19_female,
                        age_20_29_male, age_20_29_female, age_30_39_male, age_30_39_female,
                        age_40_49_male, age_40_49_female, age_50_59_male, age_50_59_female,
                        age_60_69_male, age_60_69_female, age_70_79_male, age_70_79_female,
                        age_80_89_male, age_80_89_female, age_90_99_male, age_90_99_female,
                        age_100_plus_male, age_100_plus_female,
                        total_population, total_male, total_female
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['행정기관코드'], reference_date, row['시도명'], row['시군구명'], row['읍면동명'],
                    int(row['0~9세_남자']), int(row['0~9세_여자']), int(row['10~19세_남자']), int(row['10~19세_여자']),
                    int(row['20~29세_남자']), int(row['20~29세_여자']), int(row['30~39세_남자']), int(row['30~39세_여자']),
                    int(row['40~49세_남자']), int(row['40~49세_여자']), int(row['50~59세_남자']), int(row['50~59세_여자']),
                    int(row['60~69세_남자']), int(row['60~69세_여자']), int(row['70~79세_남자']), int(row['70~79세_여자']),
                    int(row['80~89세_남자']), int(row['80~89세_여자']), int(row['90~99세_남자']), int(row['90~99세_여자']),
                    int(row['100세 이상_남자']), int(row['100세 이상_여자']),
                    int(row['총인구수']), int(row['남자총합']), int(row['여자총합'])
                ))
                insert_count += 1
        
        conn.commit()
        print(f"✅ {insert_count}개 레코드 삽입 완료")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ CSV 임포트 오류: {str(e)}")
        return False

if __name__ == "__main__":
    print("인구 통계 데이터베이스 상태 확인")
    print("=" * 50)
    
    has_data = check_database()
    
    if not has_data:
        print("\n데이터가 없습니다. CSV 파일을 자동으로 임포트합니다...")
        success = import_csv_data()
        if success:
            print("\n=== 임포트 후 데이터 재확인 ===")
            check_database()
        else:
            print("CSV 임포트에 실패했습니다.")
    
    print("\n=== 완료 ===")

#!/usr/bin/env python3
"""
간단한 CSV 임포트 스크립트
"""

import psycopg2
import csv
import datetime
import sys

# 데이터베이스 연결 설정
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/marketing_platform"

def simple_import():
    """간단한 CSV 임포트"""
    try:
        # 데이터베이스 연결
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("데이터베이스 연결 성공")
        
        # 기존 데이터 삭제
        cursor.execute("DELETE FROM population_statistics")
        print("기존 데이터 삭제 완료")
        
        # CSV 파일 경로
        csv_file_path = "D:/FinalProjects/Marketing-Platform/docs/population_with_total_columns.csv"
        
        # CSV 파일 읽기
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # 첫 번째 줄(헤더) 읽기
            header = file.readline().strip()
            print(f"CSV 헤더: {header}")
            
            # 수동으로 데이터 파싱
            insert_count = 0
            for line_num, line in enumerate(file, 2):  # 2번째 줄부터
                try:
                    # CSV 라인 파싱
                    values = line.strip().split(',')
                    
                    if len(values) < 29:
                        print(f"라인 {line_num}: 컬럼 수 부족 (expected 29, got {len(values)})")
                        continue
                    
                    # 날짜 파싱
                    reference_date = datetime.datetime.strptime(values[1], '%Y-%m-%d').date()
                    
                    # 데이터 삽입
                    cursor.execute("""
                        INSERT INTO population_statistics (
                            administrative_code, reference_date, province, city, district,
                            age_0_9_male, age_0_9_female, age_10_19_male, age_10_19_female,
                            age_20_29_male, age_20_29_female, age_30_39_male, age_30_39_female,
                            age_40_49_male, age_40_49_female, age_50_59_male, age_50_59_female,
                            age_60_69_male, age_60_69_female, age_70_79_male, age_70_79_female,
                            age_80_89_male, age_80_89_female, age_90_99_male, age_90_99_female,
                            age_100_plus_male, age_100_plus_female,
                            total_population, total_male, total_female
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        values[0], reference_date, values[2], values[3], values[4],  # 행정코드, 날짜, 시도, 시군구, 읍면동
                        int(values[5]), int(values[6]), int(values[7]), int(values[8]),  # 0-9세
                        int(values[9]), int(values[10]), int(values[11]), int(values[12]),  # 20-29세
                        int(values[13]), int(values[14]), int(values[15]), int(values[16]),  # 40-49세
                        int(values[17]), int(values[18]), int(values[19]), int(values[20]),  # 60-69세
                        int(values[21]), int(values[22]), int(values[23]), int(values[24]),  # 80-89세
                        int(values[25]), int(values[26]),  # 100세 이상
                        int(values[27]), int(values[28]), int(values[29])  # 총인구, 남자총합, 여자총합
                    ))
                    
                    insert_count += 1
                    
                    if insert_count % 10 == 0:
                        print(f"진행 상황: {insert_count}개 레코드 삽입...")
                        
                except Exception as e:
                    print(f"라인 {line_num} 처리 중 오류: {str(e)}")
                    print(f"문제 라인: {line[:100]}...")
                    continue
        
        # 커밋
        conn.commit()
        print(f"✅ 총 {insert_count}개 레코드 삽입 완료")
        
        # 확인
        cursor.execute("SELECT COUNT(*) FROM population_statistics")
        count = cursor.fetchone()[0]
        print(f"최종 데이터 개수: {count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 오류: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== 간단한 CSV 임포트 ===")
    success = simple_import()
    
    if success:
        print("=== 임포트 성공! ===")
    else:
        print("=== 임포트 실패! ===")

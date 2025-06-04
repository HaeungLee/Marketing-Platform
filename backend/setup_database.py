#!/usr/bin/env python3
"""
데이터베이스 설정 및 데이터 import 스크립트
"""
import asyncio
import asyncpg
import pandas as pd
from datetime import datetime
import os
import sys

# 데이터베이스 연결 설정
DATABASE_URL = "postgresql://postgres:human1234@localhost:5432/marketing_platform"

async def create_table(connection):
    """인구 통계 테이블 생성"""
    create_table_sql = """
    DROP TABLE IF EXISTS population_statistics;
    
    CREATE TABLE population_statistics (
        id SERIAL PRIMARY KEY,
        administrative_code VARCHAR(20) NOT NULL,
        reference_date DATE NOT NULL,
        province VARCHAR(20) NOT NULL,
        city VARCHAR(20) NOT NULL,
        district VARCHAR(20) NOT NULL,
        -- Age groups - Male
        age_0_9_male INTEGER NOT NULL DEFAULT 0,
        age_10_19_male INTEGER NOT NULL DEFAULT 0,
        age_20_29_male INTEGER NOT NULL DEFAULT 0,
        age_30_39_male INTEGER NOT NULL DEFAULT 0,
        age_40_49_male INTEGER NOT NULL DEFAULT 0,
        age_50_59_male INTEGER NOT NULL DEFAULT 0,
        age_60_69_male INTEGER NOT NULL DEFAULT 0,
        age_70_79_male INTEGER NOT NULL DEFAULT 0,
        age_80_89_male INTEGER NOT NULL DEFAULT 0,
        age_90_99_male INTEGER NOT NULL DEFAULT 0,
        age_100_plus_male INTEGER NOT NULL DEFAULT 0,
        -- Age groups - Female
        age_0_9_female INTEGER NOT NULL DEFAULT 0,
        age_10_19_female INTEGER NOT NULL DEFAULT 0,
        age_20_29_female INTEGER NOT NULL DEFAULT 0,
        age_30_39_female INTEGER NOT NULL DEFAULT 0,
        age_40_49_female INTEGER NOT NULL DEFAULT 0,
        age_50_59_female INTEGER NOT NULL DEFAULT 0,
        age_60_69_female INTEGER NOT NULL DEFAULT 0,
        age_70_79_female INTEGER NOT NULL DEFAULT 0,
        age_80_89_female INTEGER NOT NULL DEFAULT 0,
        age_90_99_female INTEGER NOT NULL DEFAULT 0,
        age_100_plus_female INTEGER NOT NULL DEFAULT 0,
        -- Totals
        total_population INTEGER NOT NULL DEFAULT 0,
        total_male INTEGER NOT NULL DEFAULT 0,
        total_female INTEGER NOT NULL DEFAULT 0
    );
    
    -- 인덱스 생성
    CREATE INDEX ix_population_statistics_reference_date ON population_statistics(reference_date);
    CREATE INDEX ix_population_statistics_administrative_code ON population_statistics(administrative_code);
    CREATE INDEX ix_population_statistics_city_district ON population_statistics(city, district);
    """
    
    await connection.execute(create_table_sql)
    print("✅ population_statistics 테이블이 성공적으로 생성되었습니다.")

def parse_csv_data(csv_path):
    """CSV 데이터를 파싱하여 데이터베이스 형식으로 변환"""
    try:
        # CSV 파일 읽기 (한글 인코딩 처리)
        encodings = ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
                print(f"✅ CSV 파일을 {encoding} 인코딩으로 성공적으로 읽었습니다.")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise Exception("CSV 파일을 읽을 수 없습니다. 인코딩을 확인해주세요.")
        
        print(f"📊 CSV 파일 정보:")
        print(f"   - 행 수: {len(df)}")
        print(f"   - 열 수: {len(df.columns)}")
        print(f"   - 컬럼: {list(df.columns)}")
        
        # 데이터 변환
        records = []
        for _, row in df.iterrows():
            try:
                record = {
                    'administrative_code': str(row.get('행정구역코드', '00000')),
                    'reference_date': datetime(2023, 1, 1).date(),  # 기본 날짜
                    'province': str(row.get('시도', '인천')),
                    'city': str(row.get('시군구', row.get('city', '미정'))),
                    'district': str(row.get('읍면동', row.get('district', '전체'))),
                    
                    # 남성 연령대별 인구
                    'age_0_9_male': int(row.get('0~9세_남', row.get('age_0_9_male', 0)) or 0),
                    'age_10_19_male': int(row.get('10~19세_남', row.get('age_10_19_male', 0)) or 0),
                    'age_20_29_male': int(row.get('20~29세_남', row.get('age_20_29_male', 0)) or 0),
                    'age_30_39_male': int(row.get('30~39세_남', row.get('age_30_39_male', 0)) or 0),
                    'age_40_49_male': int(row.get('40~49세_남', row.get('age_40_49_male', 0)) or 0),
                    'age_50_59_male': int(row.get('50~59세_남', row.get('age_50_59_male', 0)) or 0),
                    'age_60_69_male': int(row.get('60~69세_남', row.get('age_60_69_male', 0)) or 0),
                    'age_70_79_male': int(row.get('70~79세_남', row.get('age_70_79_male', 0)) or 0),
                    'age_80_89_male': int(row.get('80~89세_남', row.get('age_80_89_male', 0)) or 0),
                    'age_90_99_male': int(row.get('90~99세_남', row.get('age_90_99_male', 0)) or 0),
                    'age_100_plus_male': int(row.get('100세이상_남', row.get('age_100_plus_male', 0)) or 0),
                    
                    # 여성 연령대별 인구
                    'age_0_9_female': int(row.get('0~9세_여', row.get('age_0_9_female', 0)) or 0),
                    'age_10_19_female': int(row.get('10~19세_여', row.get('age_10_19_female', 0)) or 0),
                    'age_20_29_female': int(row.get('20~29세_여', row.get('age_20_29_female', 0)) or 0),
                    'age_30_39_female': int(row.get('30~39세_여', row.get('age_30_39_female', 0)) or 0),
                    'age_40_49_female': int(row.get('40~49세_여', row.get('age_40_49_female', 0)) or 0),
                    'age_50_59_female': int(row.get('50~59세_여', row.get('age_50_59_female', 0)) or 0),
                    'age_60_69_female': int(row.get('60~69세_여', row.get('age_60_69_female', 0)) or 0),
                    'age_70_79_female': int(row.get('70~79세_여', row.get('age_70_79_female', 0)) or 0),
                    'age_80_89_female': int(row.get('80~89세_여', row.get('age_80_89_female', 0)) or 0),
                    'age_90_99_female': int(row.get('90~99세_여', row.get('age_90_99_female', 0)) or 0),
                    'age_100_plus_female': int(row.get('100세이상_여', row.get('age_100_plus_female', 0)) or 0),
                    
                    # 전체 합계
                    'total_male': int(row.get('총_남', row.get('total_male', 0)) or 0),
                    'total_female': int(row.get('총_여', row.get('total_female', 0)) or 0),
                    'total_population': int(row.get('총인구', row.get('total_population', 0)) or 0),
                }
                
                # 총인구가 0이거나 계산되지 않은 경우 계산
                if record['total_population'] == 0:
                    record['total_population'] = record['total_male'] + record['total_female']
                
                records.append(record)
                
            except Exception as e:
                print(f"⚠️  행 파싱 오류 (건너뜀): {e}")
                continue
        
        print(f"✅ {len(records)}개의 레코드가 성공적으로 파싱되었습니다.")
        return records
        
    except Exception as e:
        print(f"❌ CSV 파싱 오류: {e}")
        return []

async def insert_data(connection, records):
    """데이터베이스에 데이터 삽입"""
    if not records:
        print("❌ 삽입할 데이터가 없습니다.")
        return
    
    insert_sql = """
    INSERT INTO population_statistics (
        administrative_code, reference_date, province, city, district,
        age_0_9_male, age_10_19_male, age_20_29_male, age_30_39_male, age_40_49_male,
        age_50_59_male, age_60_69_male, age_70_79_male, age_80_89_male, age_90_99_male, age_100_plus_male,
        age_0_9_female, age_10_19_female, age_20_29_female, age_30_39_female, age_40_49_female,
        age_50_59_female, age_60_69_female, age_70_79_female, age_80_89_female, age_90_99_female, age_100_plus_female,
        total_population, total_male, total_female
    ) VALUES (
        $1, $2, $3, $4, $5,
        $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16,
        $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27,
        $28, $29, $30
    )
    """
    
    success_count = 0
    for record in records:
        try:
            await connection.execute(
                insert_sql,
                record['administrative_code'], record['reference_date'], record['province'], 
                record['city'], record['district'],
                record['age_0_9_male'], record['age_10_19_male'], record['age_20_29_male'], 
                record['age_30_39_male'], record['age_40_49_male'], record['age_50_59_male'], 
                record['age_60_69_male'], record['age_70_79_male'], record['age_80_89_male'], 
                record['age_90_99_male'], record['age_100_plus_male'],
                record['age_0_9_female'], record['age_10_19_female'], record['age_20_29_female'], 
                record['age_30_39_female'], record['age_40_49_female'], record['age_50_59_female'], 
                record['age_60_69_female'], record['age_70_79_female'], record['age_80_89_female'], 
                record['age_90_99_female'], record['age_100_plus_female'],
                record['total_population'], record['total_male'], record['total_female']
            )
            success_count += 1
        except Exception as e:
            print(f"⚠️  데이터 삽입 오류 (건너뜀): {e}")
            continue
    
    print(f"✅ {success_count}개의 레코드가 성공적으로 삽입되었습니다.")

async def verify_data(connection):
    """데이터 삽입 확인"""
    count_result = await connection.fetchval("SELECT COUNT(*) FROM population_statistics")
    sample_result = await connection.fetch("SELECT city, district, total_population FROM population_statistics LIMIT 5")
    
    print(f"\n📊 데이터베이스 확인:")
    print(f"   - 총 레코드 수: {count_result}")
    print(f"   - 샘플 데이터:")
    for row in sample_result:
        print(f"     {row['city']} {row['district']}: {row['total_population']:,}명")

async def main():
    """메인 함수"""
    print("🚀 인구 통계 데이터베이스 설정을 시작합니다...\n")
    
    try:
        # 데이터베이스 연결
        connection = await asyncpg.connect(DATABASE_URL)
        print("✅ 데이터베이스에 성공적으로 연결되었습니다.")
        
        # 테이블 생성
        await create_table(connection)
        
        # CSV 파일 처리
        csv_path = "../docs/population_with_total_columns.csv"
        if not os.path.exists(csv_path):
            print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
            return
        
        print(f"\n📂 CSV 파일 처리: {csv_path}")
        records = parse_csv_data(csv_path)
        
        if records:
            # 데이터 삽입
            print(f"\n💾 데이터베이스에 데이터를 삽입합니다...")
            await insert_data(connection, records)
            
            # 데이터 확인
            await verify_data(connection)
        
        await connection.close()
        print("\n🎉 데이터베이스 설정이 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

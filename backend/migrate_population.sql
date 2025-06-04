-- 인구통계 테이블 생성 및 데이터 마이그레이션 스크립트

-- 기존 테이블이 있다면 삭제
DROP TABLE IF EXISTS population_statistics;

-- 인구통계 테이블 생성
CREATE TABLE population_statistics (
    id SERIAL PRIMARY KEY,
    admin_code VARCHAR(20) NOT NULL,
    reference_date DATE NOT NULL,
    sido VARCHAR(50) NOT NULL,
    sigungu VARCHAR(50) NOT NULL,
    eup_myeon_dong VARCHAR(100) NOT NULL,
    male_0_9 INTEGER DEFAULT 0,
    female_0_9 INTEGER DEFAULT 0,
    male_10_19 INTEGER DEFAULT 0,
    female_10_19 INTEGER DEFAULT 0,
    male_20_29 INTEGER DEFAULT 0,
    female_20_29 INTEGER DEFAULT 0,
    male_30_39 INTEGER DEFAULT 0,
    female_30_39 INTEGER DEFAULT 0,
    male_40_49 INTEGER DEFAULT 0,
    female_40_49 INTEGER DEFAULT 0,
    male_50_59 INTEGER DEFAULT 0,
    female_50_59 INTEGER DEFAULT 0,
    male_60_69 INTEGER DEFAULT 0,
    female_60_69 INTEGER DEFAULT 0,
    male_70_79 INTEGER DEFAULT 0,
    female_70_79 INTEGER DEFAULT 0,
    male_80_89 INTEGER DEFAULT 0,
    female_80_89 INTEGER DEFAULT 0,
    male_90_99 INTEGER DEFAULT 0,
    female_90_99 INTEGER DEFAULT 0,
    male_100_plus INTEGER DEFAULT 0,
    female_100_plus INTEGER DEFAULT 0,
    total_population INTEGER DEFAULT 0,
    total_male INTEGER DEFAULT 0,
    total_female INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성 (성능 향상)
CREATE INDEX idx_population_sido ON population_statistics(sido);
CREATE INDEX idx_population_sigungu ON population_statistics(sigungu);
CREATE INDEX idx_population_admin_code ON population_statistics(admin_code);
CREATE INDEX idx_population_reference_date ON population_statistics(reference_date);

-- CSV 파일에서 임시 테이블로 데이터 로드
CREATE TEMP TABLE temp_population (
    admin_code VARCHAR(20),
    reference_date VARCHAR(20),
    sido VARCHAR(50),
    sigungu VARCHAR(50),
    eup_myeon_dong VARCHAR(100),
    male_0_9 INTEGER,
    female_0_9 INTEGER,
    male_10_19 INTEGER,
    female_10_19 INTEGER,
    male_20_29 INTEGER,
    female_20_29 INTEGER,
    male_30_39 INTEGER,
    female_30_39 INTEGER,
    male_40_49 INTEGER,
    female_40_49 INTEGER,
    male_50_59 INTEGER,
    female_50_59 INTEGER,
    male_60_69 INTEGER,
    female_60_69 INTEGER,
    male_70_79 INTEGER,
    female_70_79 INTEGER,
    male_80_89 INTEGER,
    female_80_89 INTEGER,
    male_90_99 INTEGER,
    female_90_99 INTEGER,
    male_100_plus INTEGER,
    female_100_plus INTEGER,
    total_population INTEGER,
    total_male INTEGER,
    total_female INTEGER
);

-- CSV 파일 데이터 복사 (절대 경로 사용)
COPY temp_population FROM 'D:\FinalProjects\Marketing-Platform\docs\population_with_total_columns.csv' 
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

-- 임시 테이블에서 실제 테이블로 데이터 이동 (날짜 변환 포함)
INSERT INTO population_statistics (
    admin_code, reference_date, sido, sigungu, eup_myeon_dong,
    male_0_9, female_0_9, male_10_19, female_10_19,
    male_20_29, female_20_29, male_30_39, female_30_39,
    male_40_49, female_40_49, male_50_59, female_50_59,
    male_60_69, female_60_69, male_70_79, female_70_79,
    male_80_89, female_80_89, male_90_99, female_90_99,
    male_100_plus, female_100_plus, total_population,
    total_male, total_female
)
SELECT 
    admin_code,
    TO_DATE(reference_date, 'YYYY-MM-DD') as reference_date,
    sido, sigungu, eup_myeon_dong,
    male_0_9, female_0_9, male_10_19, female_10_19,
    male_20_29, female_20_29, male_30_39, female_30_39,
    male_40_49, female_40_49, male_50_59, female_50_59,
    male_60_69, female_60_69, male_70_79, female_70_79,
    male_80_89, female_80_89, male_90_99, female_90_99,
    male_100_plus, female_100_plus, total_population,
    total_male, total_female
FROM temp_population;

-- 결과 확인
SELECT COUNT(*) as total_records FROM population_statistics;
SELECT sido, COUNT(*) as record_count FROM population_statistics GROUP BY sido ORDER BY sido;

-- 샘플 데이터 조회
SELECT * FROM population_statistics LIMIT 5;

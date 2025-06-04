#!/usr/bin/env python3
"""
빠른 실제 데이터 로딩 스크립트
docs 폴더의 CSV 데이터를 데이터베이스에 빠르게 로드
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
import logging
from typing import List, Dict
import asyncio
import asyncpg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuickDataLoader:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'marketing_platform',
            'user': 'postgres',
            'password': 'postgres'
        }
        
    async def create_tables(self):
        """필요한 테이블들을 빠르게 생성"""
        conn = await asyncpg.connect(**self.db_config)
        
        # 인구통계 테이블
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS population_demographics (
                id SERIAL PRIMARY KEY,
                admin_code VARCHAR(20),
                base_date DATE,
                sido_name VARCHAR(50),
                sigungu_name VARCHAR(50),
                emd_name VARCHAR(50),
                age_0_9_male INTEGER DEFAULT 0,
                age_0_9_female INTEGER DEFAULT 0,
                age_10_19_male INTEGER DEFAULT 0,
                age_10_19_female INTEGER DEFAULT 0,
                age_20_29_male INTEGER DEFAULT 0,
                age_20_29_female INTEGER DEFAULT 0,
                age_30_39_male INTEGER DEFAULT 0,
                age_30_39_female INTEGER DEFAULT 0,
                age_40_49_male INTEGER DEFAULT 0,
                age_40_49_female INTEGER DEFAULT 0,
                age_50_59_male INTEGER DEFAULT 0,
                age_50_59_female INTEGER DEFAULT 0,
                age_60_69_male INTEGER DEFAULT 0,
                age_60_69_female INTEGER DEFAULT 0,
                age_70_79_male INTEGER DEFAULT 0,
                age_70_79_female INTEGER DEFAULT 0,
                age_80_89_male INTEGER DEFAULT 0,
                age_80_89_female INTEGER DEFAULT 0,
                age_90_99_male INTEGER DEFAULT 0,
                age_90_99_female INTEGER DEFAULT 0,
                age_100_plus_male INTEGER DEFAULT 0,
                age_100_plus_female INTEGER DEFAULT 0,
                total_population INTEGER DEFAULT 0,
                total_male INTEGER DEFAULT 0,
                total_female INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 유동인구 테이블
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS floating_population (
                id SERIAL PRIMARY KEY,
                device_id VARCHAR(50),
                measurement_time TIMESTAMP,
                region_type VARCHAR(50),
                district VARCHAR(50),
                admin_dong VARCHAR(50),
                visitor_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 카드 소비 테이블
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS card_consumption (
                id SERIAL PRIMARY KEY,
                transaction_date DATE,
                region_code VARCHAR(20),
                admin_code VARCHAR(20),
                business_type_code VARCHAR(10),
                business_category_1 VARCHAR(50),
                business_category_2 VARCHAR(50),
                hour_range INTEGER,
                gender VARCHAR(10),
                age_group INTEGER,
                day_of_week INTEGER,
                amount BIGINT,
                transaction_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 업종 코드 테이블
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS business_codes (
                id SERIAL PRIMARY KEY,
                major_category_code VARCHAR(10),
                major_category_name VARCHAR(100),
                middle_category_code VARCHAR(10),
                middle_category_name VARCHAR(100),
                minor_category_code VARCHAR(10),
                minor_category_name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        logger.info("모든 테이블 생성 완료")
        await conn.close()
    
    async def load_population_data(self):
        """인구통계 데이터 로드"""
        logger.info("인구통계 데이터 로딩 시작...")
        
        population_file = "d:/FinalProjects/Marketing-Platform/docs/population_with_total_columns.csv"
        
        if not os.path.exists(population_file):
            logger.error(f"파일을 찾을 수 없습니다: {population_file}")
            return
            
        df = pd.read_csv(population_file, encoding='utf-8')
        logger.info(f"로드된 인구 데이터 행 수: {len(df)}")
        
        conn = await asyncpg.connect(**self.db_config)
        
        # 데이터 변환 및 삽입
        for _, row in df.iterrows():
            try:
                await conn.execute("""
                    INSERT INTO population_demographics (
                        admin_code, base_date, sido_name, sigungu_name, emd_name,
                        age_0_9_male, age_0_9_female, age_10_19_male, age_10_19_female,
                        age_20_29_male, age_20_29_female, age_30_39_male, age_30_39_female,
                        age_40_49_male, age_40_49_female, age_50_59_male, age_50_59_female,
                        age_60_69_male, age_60_69_female, age_70_79_male, age_70_79_female,
                        age_80_89_male, age_80_89_female, age_90_99_male, age_90_99_female,
                        age_100_plus_male, age_100_plus_female, total_population, total_male, total_female
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30)
                """, 
                    str(row['행정기관코드']), 
                    pd.to_datetime(row['기준연월']).date(),
                    row['시도명'], 
                    row['시군구명'], 
                    row['읍면동명'],
                    int(row['0~9세_남자']) if pd.notna(row['0~9세_남자']) else 0,
                    int(row['0~9세_여자']) if pd.notna(row['0~9세_여자']) else 0,
                    int(row['10~19세_남자']) if pd.notna(row['10~19세_남자']) else 0,
                    int(row['10~19세_여자']) if pd.notna(row['10~19세_여자']) else 0,
                    int(row['20~29세_남자']) if pd.notna(row['20~29세_남자']) else 0,
                    int(row['20~29세_여자']) if pd.notna(row['20~29세_여자']) else 0,
                    int(row['30~39세_남자']) if pd.notna(row['30~39세_남자']) else 0,
                    int(row['30~39세_여자']) if pd.notna(row['30~39세_여자']) else 0,
                    int(row['40~49세_남자']) if pd.notna(row['40~49세_남자']) else 0,
                    int(row['40~49세_여자']) if pd.notna(row['40~49세_여자']) else 0,
                    int(row['50~59세_남자']) if pd.notna(row['50~59세_남자']) else 0,
                    int(row['50~59세_여자']) if pd.notna(row['50~59세_여자']) else 0,
                    int(row['60~69세_남자']) if pd.notna(row['60~69세_남자']) else 0,
                    int(row['60~69세_여자']) if pd.notna(row['60~69세_여자']) else 0,
                    int(row['70~79세_남자']) if pd.notna(row['70~79세_남자']) else 0,
                    int(row['70~79세_여자']) if pd.notna(row['70~79세_여자']) else 0,
                    int(row['80~89세_남자']) if pd.notna(row['80~89세_남자']) else 0,
                    int(row['80~89세_여자']) if pd.notna(row['80~89세_여자']) else 0,
                    int(row['90~99세_남자']) if pd.notna(row['90~99세_남자']) else 0,
                    int(row['90~99세_여자']) if pd.notna(row['90~99세_여자']) else 0,
                    int(row['100세 이상_남자']) if pd.notna(row['100세 이상_남자']) else 0,
                    int(row['100세 이상_여자']) if pd.notna(row['100세 이상_여자']) else 0,
                    int(row['총인구수']) if pd.notna(row['총인구수']) else 0,
                    int(row['남자총합']) if pd.notna(row['남자총합']) else 0,
                    int(row['여자총합']) if pd.notna(row['여자총합']) else 0
                )
            except Exception as e:
                logger.error(f"데이터 삽입 오류: {e}, 행: {row['읍면동명']}")
                continue
        
        await conn.close()
        logger.info("인구통계 데이터 로딩 완료")

    async def load_business_codes(self):
        """업종 코드 데이터 로드"""
        logger.info("업종 코드 데이터 로딩 시작...")
        
        business_file = "d:/FinalProjects/Marketing-Platform/docs/소상공인시장진흥공단_상가(상권)정보 업종코드_20230228.csv"
        
        if not os.path.exists(business_file):
            logger.error(f"파일을 찾을 수 없습니다: {business_file}")
            return
            
        df = pd.read_csv(business_file, encoding='utf-8')
        logger.info(f"로드된 업종 코드 데이터 행 수: {len(df)}")
        
        conn = await asyncpg.connect(**self.db_config)
        
        for _, row in df.iterrows():
            try:
                await conn.execute("""
                    INSERT INTO business_codes (
                        major_category_code, major_category_name,
                        middle_category_code, middle_category_name,
                        minor_category_code, minor_category_name
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                """, 
                    row['대분류코드'], row['대분류명'],
                    row['중분류코드'], row['중분류명'],
                    row['소분류코드'], row['소분류명']
                )
            except Exception as e:
                logger.error(f"업종 코드 삽입 오류: {e}")
                continue
        
        await conn.close()
        logger.info("업종 코드 데이터 로딩 완료")

    async def load_floating_population_sample(self):
        """유동인구 샘플 데이터 로드"""
        logger.info("유동인구 데이터 로딩 시작...")
        
        floating_file = "d:/FinalProjects/Marketing-Platform/docs/유동인구/S-DoT_WALK_2025.04.21-04.27.csv"
        
        if not os.path.exists(floating_file):
            logger.error(f"파일을 찾을 수 없습니다: {floating_file}")
            return
            
        df = pd.read_csv(floating_file, encoding='utf-8')
        logger.info(f"로드된 유동인구 데이터 행 수: {len(df)}")
        
        conn = await asyncpg.connect(**self.db_config)
        
        # 샘플 데이터만 로드 (처음 1000개)
        sample_df = df.head(1000)
        
        for _, row in sample_df.iterrows():
            try:
                measurement_time = pd.to_datetime(row['측정시간'], format='%Y-%m-%d_%H:%M:%S')
                await conn.execute("""
                    INSERT INTO floating_population (
                        device_id, measurement_time, region_type, district, admin_dong, visitor_count
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                """, 
                    row['시리얼'], measurement_time, 
                    row['지역'], row['자치구'], row['행정동'],
                    int(row['방문자수']) if pd.notna(row['방문자수']) else 0
                )
            except Exception as e:
                logger.error(f"유동인구 데이터 삽입 오류: {e}")
                continue
        
        await conn.close()
        logger.info("유동인구 데이터 로딩 완료")

    async def load_card_consumption_sample(self):
        """카드 소비 샘플 데이터 로드"""
        logger.info("카드 소비 데이터 로딩 시작...")
        
        card_file = "d:/FinalProjects/Marketing-Platform/docs/카드소비 데이터_202503/tbsh_gyeonggi_day_202503_수원시.csv"
        
        if not os.path.exists(card_file):
            logger.error(f"파일을 찾을 수 없습니다: {card_file}")
            return
            
        df = pd.read_csv(card_file, encoding='utf-8')
        logger.info(f"로드된 카드 소비 데이터 행 수: {len(df)}")
        
        conn = await asyncpg.connect(**self.db_config)
        
        # 샘플 데이터만 로드 (처음 500개)
        sample_df = df.head(500)
        
        for _, row in sample_df.iterrows():
            try:
                transaction_date = pd.to_datetime(row['ta_ymd'], format='%Y%m%d').date()
                await conn.execute("""
                    INSERT INTO card_consumption (
                        transaction_date, region_code, admin_code, business_type_code,
                        business_category_1, business_category_2, hour_range, gender,
                        age_group, day_of_week, amount, transaction_count
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                """, 
                    transaction_date,
                    str(row['cty_rgn_no']), str(row['admi_cty_no']),
                    row['card_tpbuz_cd'], row['card_tpbuz_nm_1'], row['card_tpbuz_nm_2'],
                    int(row['hour']) if pd.notna(row['hour']) else 0,
                    row['sex'], int(row['age']) if pd.notna(row['age']) else 0,
                    int(row['day']) if pd.notna(row['day']) else 0,
                    int(row['amt']) if pd.notna(row['amt']) else 0,
                    int(row['cnt']) if pd.notna(row['cnt']) else 0
                )
            except Exception as e:
                logger.error(f"카드 소비 데이터 삽입 오류: {e}")
                continue
        
        await conn.close()
        logger.info("카드 소비 데이터 로딩 완료")

    async def run_all(self):
        """모든 데이터 로딩 실행"""
        logger.info("=== 빠른 데이터 로딩 시작 ===")
        
        await self.create_tables()
        await self.load_business_codes()
        await self.load_population_data()
        await self.load_floating_population_sample()
        await self.load_card_consumption_sample()
        
        logger.info("=== 모든 데이터 로딩 완료 ===")

if __name__ == "__main__":
    loader = QuickDataLoader()
    asyncio.run(loader.run_all())

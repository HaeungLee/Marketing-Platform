#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터베이스 연결 테스트 스크립트
"""

import asyncio
import asyncpg
import os

async def test_database_connection():
    """데이터베이스 연결 테스트"""
    
    # 연결 설정
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'marketing_platform',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    print("=== 데이터베이스 연결 테스트 ===\n")
    
    try:
        print("1. 연결 시도 중...")
        async with asyncpg.connect(**db_config) as conn:
            print("✅ 데이터베이스 연결 성공!")
            
            # 테이블 존재 확인
            print("\n2. 테이블 구조 확인...")
            tables_query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """
            tables = await conn.fetch(tables_query)
            print(f"📋 존재하는 테이블: {[table['table_name'] for table in tables]}")
            
            # population_statistics 테이블 확인
            if any(table['table_name'] == 'population_statistics' for table in tables):
                print("\n3. population_statistics 테이블 데이터 확인...")
                
                # 데이터 개수 확인
                count_query = "SELECT COUNT(*) as count FROM population_statistics"
                count_result = await conn.fetchrow(count_query)
                print(f"📊 총 데이터 개수: {count_result['count']}개")
                
                # 샘플 데이터 확인
                if count_result['count'] > 0:
                    sample_query = """
                        SELECT province, city, district, total_population 
                        FROM population_statistics 
                        ORDER BY total_population DESC 
                        LIMIT 5
                    """
                    samples = await conn.fetch(sample_query)
                    print("📋 샘플 데이터:")
                    for sample in samples:
                        print(f"  - {sample['province']} {sample['city']} {sample['district']}: {sample['total_population']:,}명")
                else:
                    print("⚠️ population_statistics 테이블에 데이터가 없습니다")
            else:
                print("❌ population_statistics 테이블이 존재하지 않습니다")
                
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        print(f"연결 설정: {db_config}")

if __name__ == "__main__":
    asyncio.run(test_database_connection())

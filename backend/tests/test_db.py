import sys
import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from config.database import Base, engine, SessionLocal
from domain.models.population import PopulationStatistics

def check_tables():
    print("데이터베이스 테이블 확인 중...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"사용 가능한 테이블: {tables}")
    
    if 'population_statistics' in tables:
        print("\npopulation_statistics 테이블이 존재합니다.")
        # 테이블 스키마 확인
        columns = inspector.get_columns('population_statistics')
        print("\n컬럼 정보:")
        for column in columns:
            print(f"- {column['name']} ({column['type']})")
    else:
        print("\npopulation_statistics 테이블이 존재하지 않습니다.")

def test_connection():
    print("데이터베이스 연결 테스트 중...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("데이터베이스 연결 성공!")
            return True
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("데이터베이스 연결 테스트")
    print("="*50)
    
    if test_connection():
        check_tables()
    
    print("\n테스트가 완료되었습니다.")

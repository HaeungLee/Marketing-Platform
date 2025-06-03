"""
데이터베이스 연결 및 테이블 존재 여부를 확인하는 스크립트
"""
import sys
import os
import io
from pathlib import Path

# Set stdout to support UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 프로젝트 루트 디렉토리를 시스템 경로에 추가
project_root = str(Path(__file__).parent.parent.absolute())
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))

from sqlalchemy import inspect
from config.settings import settings
from config.database import engine, SessionLocal
from domain.models.population import PopulationStatistics

def check_database():
    print("\n=== 데이터베이스 연결 확인 ===")
    # Print database URL with sensitive information masked
    db_url = settings.sync_database_url
    if '@' in db_url:
        # Mask password in the URL
        protocol_part = db_url.split('://')[0] + '://'
        auth_part = db_url.split('://')[1].split('@')[0]
        if ':' in auth_part:
            user = auth_part.split(':')[0]
            masked_url = f"{protocol_part}{user}:*****@{'@'.join(db_url.split('@')[1:])}"
        else:
            masked_url = db_url
    else:
        masked_url = db_url
    print(f"데이터베이스 URL: {masked_url}")
    
    try:
        # 연결 테스트
        with engine.connect() as conn:
            print("✅ 데이터베이스에 성공적으로 연결되었습니다.")
        
        # 테이블 존재 여부 확인
        inspector = inspect(engine)
        table_name = PopulationStatistics.__tablename__
        table_exists = inspector.has_table(table_name)
        
        if table_exists:
            print(f"✅ 테이블 '{table_name}'이(가) 존재합니다.")
            
            # 컬럼 정보 출력
            columns = inspector.get_columns(table_name)
            print("\n=== 테이블 컬럼 정보 ===")
            for column in columns:
                print(f"- {column['name']} ({column['type']})")
            
            # 샘플 데이터 개수 확인
            db = SessionLocal()
            try:
                count = db.query(PopulationStatistics).count()
                print(f"\n✅ 테이블에 {count}개의 레코드가 있습니다.")
                
                # 샘플 데이터 조회 (최대 5개)
                if count > 0:
                    print("\n=== 샘플 데이터 (최대 5개) ===")
                    samples = db.query(PopulationStatistics).limit(5).all()
                    for i, sample in enumerate(samples, 1):
                        try:
                            print(f"\n[{i}] {sample.province} {sample.city} {sample.district}")
                            print(f"   총 인구: {sample.total_population}명 (남: {sample.total_male}명, 여: {sample.total_female}명)")
                        except Exception as e:
                            print(f"\n[오류] 데이터를 표시하는 중 오류 발생: {str(e)}")
                            continue
            except Exception as e:
                print(f"\n❌ 테이블 쿼리 중 오류 발생: {str(e)}")
            finally:
                db.close()
        else:
            print(f"\n❌ 테이블 '{table_name}'이(가) 존재하지 않습니다.")
            print("\nAlembic 마이그레이션을 실행하세요:")
            print("1. cd backend/src")
            print("2. alembic upgrade head")
    
    except Exception as e:
        import traceback
        print(f"\n❌ 데이터베이스 연결 중 오류 발생: {str(e)}")
        print("\n에러 상세 정보:")
        print(traceback.format_exc())
        print("\n다음 사항을 확인하세요:")
        print("1. 데이터베이스 서버가 실행 중인지 확인하세요.")
        print("2. .env 파일에 올바른 데이터베이스 연결 정보가 설정되어 있는지 확인하세요.")
        print(f"3. 데이터베이스 URL: {settings.sync_database_url}")

if __name__ == "__main__":
    check_database()

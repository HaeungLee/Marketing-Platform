import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.config.settings import Settings
from src.config.database import get_db

# 테스트용 데이터베이스 설정
settings = Settings()
TEST_DATABASE_URL = f"postgresql://test:test@postgres17:5432/testdb"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_get_locations():
    """
    /api/v1/population/locations 엔드포인트 테스트
    """
    # 기본 locations 요청 테스트
    response = client.get("/api/v1/population/locations")
    print("Response status code:", response.status_code)
    print("Response content:", response.content)
    
    if response.status_code != 200:
        print("Error response:", response.text)
    
    assert response.status_code == 200
    data = response.json()
    
    # 응답 구조 검증
    assert "provinces" in data
    assert isinstance(data["provinces"], list)
    
    # 특정 시/도에 대한 시/군/구 요청 테스트
    if data["provinces"]:
        province = data["provinces"][0]
        response = client.get(f"/api/v1/population/locations?province={province}")
        assert response.status_code == 200
        data = response.json()
        assert "cities" in data
        
        # 시/군/구가 있는 경우 읍/면/동 요청 테스트
        if data["cities"]:
            city = data["cities"][0]
            response = client.get(
                f"/api/v1/population/locations?province={province}&city={city}"
            )
            assert response.status_code == 200
            data = response.json()
            assert "districts" in data

def test_database_connection():
    """
    데이터베이스 연결 테스트
    """
    try:
        # 세션 생성 테스트
        db = next(override_get_db())
        
        # 테이블 존재 여부 확인
        result = db.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'population_statistics')")
        assert result.scalar(), "population_statistics 테이블이 존재하지 않습니다."
        
        # 데이터 존재 여부 확인
        result = db.execute("SELECT COUNT(*) FROM population_statistics")
        count = result.scalar()
        print(f"population_statistics 테이블의 총 레코드 수: {count}")
        
        # 샘플 데이터 조회
        result = db.execute("SELECT DISTINCT province, city, district FROM population_statistics LIMIT 5")
        rows = result.fetchall()
        print("샘플 데이터:")
        for row in rows:
            print(f"  - {row.province}, {row.city}, {row.district}")
            
    except Exception as e:
        pytest.fail(f"데이터베이스 연결 테스트 실패: {str(e)}") 
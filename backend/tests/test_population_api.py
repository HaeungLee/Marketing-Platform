#!/usr/bin/env python3
"""
인구통계 API 테스트
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_locations_api():
    """locations API 테스트"""
    print("🔍 /api/v1/population/locations 테스트 중...")
    
    try:
        # 1. 모든 시도 조회
        response = requests.get(f"{BASE_URL}/api/v1/population/locations")
        print(f"   시도 조회 - 상태코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 시도 목록: {data.get('provinces', [])}")
            
            # 2. 특정 시도의 시군구 조회 (인천 테스트)
            if '인천' in data.get('provinces', []):
                response2 = requests.get(f"{BASE_URL}/api/v1/population/locations?province=인천")
                print(f"   인천 시군구 조회 - 상태코드: {response2.status_code}")
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    print(f"   ✅ 인천 시군구: {data2.get('cities', [])}")
                    
                    # 3. 특정 시군구의 읍면동 조회
                    cities = data2.get('cities', [])
                    if cities:
                        first_city = cities[0]
                        response3 = requests.get(f"{BASE_URL}/api/v1/population/locations?province=인천&city={first_city}")
                        print(f"   {first_city} 읍면동 조회 - 상태코드: {response3.status_code}")
                        
                        if response3.status_code == 200:
                            data3 = response3.json()
                            print(f"   ✅ {first_city} 읍면동: {data3.get('districts', [])[:5]}...")  # 처음 5개만 출력
                        else:
                            print(f"   ❌ 읍면동 조회 실패: {response3.text}")
                else:
                    print(f"   ❌ 시군구 조회 실패: {response2.text}")
        else:
            print(f"   ❌ 시도 조회 실패: {response.text}")
            
    except Exception as e:
        print(f"   ❌ API 테스트 실패: {e}")

def test_statistics_api():
    """statistics API 테스트"""
    print("\n🔍 /api/v1/population/statistics 테스트 중...")
    
    try:
        # 기본 통계 조회
        response = requests.get(f"{BASE_URL}/api/v1/population/statistics?limit=5")
        print(f"   통계 조회 - 상태코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 데이터 수: {len(data.get('data', []))}")
            
            if data.get('data'):
                sample = data['data'][0]
                print(f"   📊 샘플 데이터:")
                print(f"      지역: {sample.get('city')} {sample.get('district')}")
                print(f"      총인구: {sample.get('total_population'):,}명")
                print(f"      남성: {sample.get('total_male'):,}명, 여성: {sample.get('total_female'):,}명")
        else:
            print(f"   ❌ 통계 조회 실패: {response.text}")
            
    except Exception as e:
        print(f"   ❌ API 테스트 실패: {e}")

def test_summary_api():
    """summary API 테스트"""
    print("\n🔍 /api/v1/population/summary 테스트 중...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/population/summary")
        print(f"   요약 조회 - 상태코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 요약 정보 조회 성공")
            print(f"   📊 {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"   ❌ 요약 조회 실패: {response.text}")
            
    except Exception as e:
        print(f"   ❌ API 테스트 실패: {e}")

def main():
    print("🚀 인구통계 API 전체 테스트 시작\n")
    
    # 서버 연결 테스트
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 서버가 정상 작동 중입니다\n")
        else:
            print("❌ 서버 응답에 문제가 있습니다")
            return
    except Exception as e:
        print(f"❌ 서버에 연결할 수 없습니다: {e}")
        return
    
    # 각 API 테스트 실행
    test_locations_api()
    test_statistics_api()
    test_summary_api()
    
    print("\n🎉 API 테스트 완료!")

if __name__ == "__main__":
    main()

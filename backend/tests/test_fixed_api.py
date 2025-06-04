import requests
import json

# API 테스트 스크립트
BASE_URL = "http://localhost:8000/api/v1/population"

def test_locations():
    """지역 정보 API 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/locations")
        print(f"Locations API Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception in locations API: {str(e)}")

def test_statistics():
    """통계 API 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/statistics")
        print(f"\nStatistics API Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total records: {data.get('total_count', 0)}")
            if data.get('data'):
                print(f"First record: {json.dumps(data['data'][0], indent=2, ensure_ascii=False)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception in statistics API: {str(e)}")

def test_summary():
    """요약 API 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/summary")
        print(f"\nSummary API Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception in summary API: {str(e)}")

def test_age_distribution():
    """연령분포 API 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/age-distribution")
        print(f"\nAge Distribution API Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total records: {data.get('total_count', 0)}")
            if data.get('data'):
                print(f"First record: {json.dumps(data['data'][0], indent=2, ensure_ascii=False)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception in age distribution API: {str(e)}")

if __name__ == "__main__":
    print("=== Population API Test ===")
    test_locations()
    test_statistics()
    test_summary()
    test_age_distribution()
    print("\n=== Test Complete ===")

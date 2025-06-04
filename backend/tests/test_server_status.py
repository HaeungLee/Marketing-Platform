import requests

try:
    # 서버 상태 확인
    response = requests.get('http://localhost:8000/docs', timeout=5)
    print(f"Server is running! Status: {response.status_code}")
    
    # 간단한 locations API 테스트
    response = requests.get('http://localhost:8000/api/v1/population/locations', timeout=5)
    print(f"Locations API Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Provinces available: {len(data.get('provinces', []))}")
        
        # province가 포함된 statistics API 테스트
        response = requests.get('http://localhost:8000/api/v1/population/statistics?province=서울특별시', timeout=10)
        print(f"Statistics API with province Status: {response.status_code}")
        if response.status_code == 200:
            stats_data = response.json()
            print(f"Found {len(stats_data.get('data', []))} records")
            if stats_data.get('data'):
                first = stats_data['data'][0]
                print(f"First record location: {first.get('province')} {first.get('city')} {first.get('district')}")
        else:
            print(f"Statistics API error: {response.text}")
    
except requests.exceptions.ConnectioError:
    print("❌ Cannot connect to server. Is the backend running?")
except requests.exceptions.Timeout:
    print("⏰ Request timed out")
except Exception as e:
    print(f"Error: {e}")

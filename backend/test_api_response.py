import requests
import json

# 특정 지역의 통계 데이터 요청
try:
    response = requests.get('http://localhost:8000/api/v1/population/statistics?province=서울특별시&city=강남구&district=역삼동')
    print('Status Code:', response.status_code)
    print('Response Headers:', dict(response.headers))
    print('Response Body:')
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print('Error:', e)

print("\n" + "="*50 + "\n")

# 지역 목록 API 요청
try:
    response = requests.get('http://localhost:8000/api/v1/population/locations')
    print('Locations API Status Code:', response.status_code)
    print('Locations Response:')
    data = response.json()
    print(f"Provinces count: {len(data.get('provinces', []))}")
    print(f"First 5 provinces: {data.get('provinces', [])[:5]}")
    print(f"Cities structure: {type(data.get('cities', {}))}")
    print(f"Districts structure: {type(data.get('districts', {}))}")
except Exception as e:
    print('Locations Error:', e)

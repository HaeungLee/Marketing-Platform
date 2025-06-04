import requests
import json

# 테스트용 다른 설정들
test_cases = [
    {
        "name": "카페 강남구",
        "business_type": "카페",
        "region": "강남구",
        "budget": 50000000,
        "target_age": "20대"
    },
    {
        "name": "음식점 홍대",
        "business_type": "음식점", 
        "region": "홍대",
        "budget": 70000000,
        "target_age": "30대"
    },
    {
        "name": "미용실 신촌",
        "business_type": "미용실",
        "region": "신촌", 
        "budget": 30000000,
        "target_age": "20대"
    },
    {
        "name": "편의점 마포구",
        "business_type": "편의점",
        "region": "마포구",
        "budget": 100000000,
        "target_age": "40대"
    }
]

base_url = "http://localhost:8000/api/v1/insights"

print("=== 동적 데이터 변화 테스트 ===\n")

for case in test_cases:
    print(f"🔍 {case['name']} 테스트")
    print("-" * 40)
    
    # 타겟 고객 분석
    try:
        response = requests.get(f"{base_url}/target-customer", params={
            "business_type": case["business_type"],
            "region": case["region"]
        })
        if response.status_code == 200:
            data = response.json()
            print(f"타겟 고객: {data['primaryTarget']}")
            print(f"전략: {', '.join(data['strategy'][:2])}")
        else:
            print(f"타겟 고객 API 오류: {response.status_code}")
    except Exception as e:
        print(f"타겟 고객 API 연결 오류: {e}")
    
    # 입지 추천
    try:
        response = requests.get(f"{base_url}/optimal-location", params={
            "business_type": case["business_type"],
            "budget": case["budget"],
            "target_age": case["target_age"]
        })
        if response.status_code == 200:
            data = response.json()
            if data["recommendedAreas"]:
                area = data["recommendedAreas"][0]
                print(f"추천 입지: {area['area']} (ROI: {area['expectedROI']})")
        else:
            print(f"입지 추천 API 오류: {response.status_code}")
    except Exception as e:
        print(f"입지 추천 API 연결 오류: {e}")
    
    # 마케팅 타이밍
    try:
        response = requests.get(f"{base_url}/marketing-timing", params={
            "target_age": case["target_age"],
            "business_type": case["business_type"]
        })
        if response.status_code == 200:
            data = response.json()
            print(f"최적 시간: {', '.join(data['bestDays'][:2])}")
            print(f"트렌드: {data['seasonalTrends']}")
        else:
            print(f"마케팅 타이밍 API 오류: {response.status_code}")
    except Exception as e:
        print(f"마케팅 타이밍 API 연결 오류: {e}")
    
    print("\n")

print("✅ 동적 데이터 테스트 완료!")

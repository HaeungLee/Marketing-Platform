import requests
import json

# province 파라미터를 포함한 API 테스트
try:
    response = requests.get('http://localhost:8000/api/v1/population/statistics?province=서울특별시&city=강남구&district=역삼동')
    print('Status Code:', response.status_code)
    print('Response Body:')
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    if data.get('data'):
        print("\n=== 첫 번째 레코드의 gender_breakdown 확인 ===")
        first_record = data['data'][0]
        gender_breakdown = first_record.get('gender_breakdown', {})
        print("Gender breakdown keys:", list(gender_breakdown.keys()))
        
        # 특정 연령대 값 확인
        print(f"age_10_19_male: {gender_breakdown.get('age_10_19_male')}")
        print(f"age_50_59_male: {gender_breakdown.get('age_50_59_male')}")
        print(f"age_60_69_male: {gender_breakdown.get('age_60_69_male')}")
        print(f"age_70_79_male: {gender_breakdown.get('age_70_79_male')}")
        
except Exception as e:
    print('Error:', e)

#!/usr/bin/env python3
"""
특정 지역의 API 응답 구조 테스트
"""

import requests
import json

def test_specific_location_api():
    """특정 지역의 API 응답을 테스트합니다."""
    base_url = "http://localhost:8000/api/v1/population"
    
    print("=== Specific Location API Response Test ===")
    
    # 서울특별시 종로구 청운효자동 테스트
    try:
        response = requests.get(f"{base_url}/statistics", params={
            "city": "종로구",
            "district": "청운효자동"
        })
        print(f"Seoul Jongno Cheongwun-hyoja - Status: {response.status_code}")
        data = response.json()
        
        if data.get('data') and len(data['data']) > 0:
            first_record = data['data'][0]
            print(f"First record structure:")
            print(json.dumps(first_record, ensure_ascii=False, indent=2))
        else:
            print("No data found")
            print(f"Full response: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_specific_location_api()

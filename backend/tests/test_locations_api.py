#!/usr/bin/env python3
"""
API 응답 구조 테스트
"""

import requests
import json

def test_locations_api():
    """Locations API의 응답 구조를 테스트합니다."""
    base_url = "http://localhost:8000/api/v1/population"
    
    print("=== Locations API Response Structure Test ===")
    
    # 1. 전체 시/도 목록
    try:
        response = requests.get(f"{base_url}/locations")
        print(f"1. All provinces - Status: {response.status_code}")
        data = response.json()
        print(f"   Provinces count: {len(data.get('provinces', []))}")
        print(f"   Sample provinces: {data.get('provinces', [])[:3]}")
        print()
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. 특정 시/도의 시/군/구 목록 (서울특별시)
    try:
        response = requests.get(f"{base_url}/locations?province=서울특별시")
        print(f"2. Seoul cities - Status: {response.status_code}")
        data = response.json()
        print(f"   Cities count: {len(data.get('cities', []))}")
        print(f"   Sample cities: {data.get('cities', [])[:5]}")
        print()
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. 특정 시/군/구의 읍/면/동 목록 (서울특별시 강남구)
    try:
        response = requests.get(f"{base_url}/locations?province=서울특별시&city=강남구")
        print(f"3. Gangnam districts - Status: {response.status_code}")
        data = response.json()
        print(f"   Districts count: {len(data.get('districts', []))}")
        print(f"   Sample districts: {data.get('districts', [])[:5]}")
        print(f"   Full response: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_locations_api()

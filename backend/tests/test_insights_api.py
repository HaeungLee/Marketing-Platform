#!/usr/bin/env python3
"""
새로운 인사이트 API 빠른 테스트
"""

import requests
import json
import time

def test_insights_api():
    """인사이트 API 테스트"""
    base_url = "http://localhost:8000/api/v1/insights"
    
    print("=== 새로운 인사이트 API 테스트 ===")
    print("서버 준비 중...")
    time.sleep(3)
    
    # 1. 타겟 고객 분석 테스트
    print("\n1. 타겟 고객 분석 테스트")
    try:
        response = requests.get(f"{base_url}/target-customer", params={
            "business_type": "카페",
            "region": "강남구"
        })
        print(f"상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("응답 데이터:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"오류: {response.text}")
    except Exception as e:
        print(f"연결 오류: {e}")
    
    # 2. 최적 입지 추천 테스트
    print("\n2. 최적 입지 추천 테스트")
    try:
        response = requests.get(f"{base_url}/optimal-location", params={
            "business_type": "음식점",
            "budget": 50000000,
            "target_age": "30대"
        })
        print(f"상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("응답 데이터:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"오류: {response.text}")
    except Exception as e:
        print(f"연결 오류: {e}")
    
    # 3. 마케팅 타이밍 테스트
    print("\n3. 마케팅 타이밍 테스트")
    try:
        response = requests.get(f"{base_url}/marketing-timing", params={
            "target_age": "20대",
            "business_type": "카페"
        })
        print(f"상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("응답 데이터:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"오류: {response.text}")
    except Exception as e:
        print(f"연결 오류: {e}")
    
    # 4. 종합 분석 테스트
    print("\n4. 종합 분석 테스트")
    try:
        response = requests.get(f"{base_url}/comprehensive-analysis", params={
            "business_type": "미용실",
            "region": "홍대",
            "budget": 30000000,
            "target_age": "20대"
        })
        print(f"상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("응답 데이터:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"오류: {response.text}")
    except Exception as e:
        print(f"연결 오류: {e}")

if __name__ == "__main__":
    test_insights_api()

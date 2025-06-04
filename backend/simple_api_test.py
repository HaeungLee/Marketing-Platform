#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 API 테스트 스크립트
"""

import requests
import json
from urllib.parse import quote

def test_api():
    base_url = "http://localhost:8000/api/v1/insights"
    
    print("=== Insights API 테스트 시작 ===\n")
    
    # 1. 마케팅 타이밍 API 테스트 (데이터베이스 불필요)
    print("1. 마케팅 타이밍 API 테스트...")
    try:
        params = {
            'target_age': '30대',
            'business_type': '카페'
        }
        response = requests.get(f"{base_url}/marketing-timing", params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ 마케팅 타이밍 API 성공")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ 마케팅 타이밍 API 실패: {response.text}")
    except Exception as e:
        print(f"❌ 마케팅 타이밍 API 오류: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 2. 타겟 고객 분석 API 테스트 (데이터베이스 필요)
    print("2. 타겟 고객 분석 API 테스트...")
    try:
        params = {
            'business_type': '카페',
            'region': '강남구'
        }
        response = requests.get(f"{base_url}/target-customer", params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ 타겟 고객 분석 API 성공")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ 타겟 고객 분석 API 실패: {response.text}")
    except Exception as e:
        print(f"❌ 타겟 고객 분석 API 오류: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 3. 최적 입지 추천 API 테스트 (데이터베이스 필요)
    print("3. 최적 입지 추천 API 테스트...")
    try:
        params = {
            'business_type': '카페',
            'budget': 50000000,
            'target_age': '30대'
        }
        response = requests.get(f"{base_url}/optimal-location", params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ 최적 입지 추천 API 성공")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ 최적 입지 추천 API 실패: {response.text}")
    except Exception as e:
        print(f"❌ 최적 입지 추천 API 오류: {e}")

if __name__ == "__main__":
    test_api()

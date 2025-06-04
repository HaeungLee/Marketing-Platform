#!/usr/bin/env python3
"""
간단한 API 상태 확인
"""
import requests

try:
    response = requests.get("http://localhost:8000/", timeout=5)
    print(f"서버 상태: {response.status_code}")
    print(f"응답: {response.text}")
except Exception as e:
    print(f"연결 실패: {e}")

try:
    response = requests.get("http://localhost:8000/api/v1/population/summary", timeout=5)
    print(f"인구통계 API 상태: {response.status_code}")
    if response.status_code == 200:
        print("✅ 인구통계 API가 정상 작동합니다!")
    else:
        print(f"❌ 오류: {response.text}")
except Exception as e:
    print(f"인구통계 API 연결 실패: {e}")

# locations API도 테스트
try:
    response = requests.get("http://localhost:8000/api/v1/population/locations", timeout=5)
    print(f"지역정보 API 상태: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 지역정보 API가 정상 작동합니다! 시도 수: {len(data.get('provinces', []))}")
    else:
        print(f"❌ 오류: {response.text}")
except Exception as e:
    print(f"지역정보 API 연결 실패: {e}")

#!/usr/bin/env python3
"""
빠른 이미지 API 테스트
"""
import requests
import json

try:
    # API 헬스 체크
    response = requests.get("http://localhost:8000/")
    print(f"🔍 헬스 체크: {response.status_code}")
    if response.ok:
        print(f"✅ 서버 응답: {response.json()}")
    
    # 이미지 생성 테스트
    payload = {"prompt": "카페 전단지, 모던한 스타일"}
    print(f"\n🚀 이미지 생성 요청: {payload}")
    
    response = requests.post(
        "http://localhost:8000/api/images/generate",
        json=payload,
        timeout=30
    )
    
    print(f"📊 응답 상태: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"✅ 성공! Keys: {list(data.keys())}")
        print(f"🖼️ Has image_data: {bool(data.get('image_data'))}")
        print(f"📏 Image data length: {len(data.get('image_data', ''))}")
    else:
        print(f"❌ 오류: {response.text}")
        
except Exception as e:
    print(f"❌ 테스트 실패: {e}")

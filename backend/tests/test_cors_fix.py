#!/usr/bin/env python3
"""
CORS 및 API 엔드포인트 테스트 스크립트
"""
import requests
import json
import time
import sys

def test_simple_content_endpoint():
    """Simple Content Generation 엔드포인트 테스트"""
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("Simple Content Generation 엔드포인트 테스트")
    print("=" * 60)
    
    # 1. OPTIONS 요청 테스트
    print("\n1. OPTIONS 요청 테스트")
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{base_url}/api/v1/content/generate/simple", headers=headers, timeout=10)
        print(f"상태 코드: {response.status_code}")
        print("CORS 헤더:")
        for key, value in response.headers.items():
            if 'cors' in key.lower() or 'access-control' in key.lower():
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"OPTIONS 요청 실패: {e}")
    
    # 2. 실제 요청 테스트
    print("\n2. POST 요청 테스트")
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        data = {
            "prompt": "커피샵에서 아메리카노를 홍보하는 짧은 글을 작성해주세요",
            "content_type": "instagram",
            "tone": "친근한"
        }
        print(f"전송 데이터: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            f"{base_url}/api/v1/content/generate/simple",
            headers=headers,
            json=data,
            timeout=30  # AI 모델 응답을 위한 충분한 시간 제공
        )
        
        print(f"상태 코드: {response.status_code}")
        print("응답 헤더:")
        for key, value in response.headers.items():
            if 'cors' in key.lower() or 'access-control' in key.lower() or 'content-type' in key.lower():
                print(f"  {key}: {value}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n응답 내용 (요약):")
            print(f"제목: {result.get('title', '제목 없음')}")
            print(f"내용 (일부): {result.get('content', '내용 없음')[:100]}...")
            print(f"해시태그: {', '.join(result.get('hashtags', []))}")
        else:
            print(f"오류 응답: {response.text}")
    except Exception as e:
        print(f"POST 요청 실패: {e}")
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)

if __name__ == "__main__":
    print("백엔드 서버가 시작되었는지 확인하세요.")
    print("백엔드 시작 명령: python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
    
    input("\n엔터를 누르면 테스트를 시작합니다...")
    test_simple_content_endpoint()

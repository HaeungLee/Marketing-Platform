#!/usr/bin/env python3
"""
CORS 디버깅을 위한 테스트 파일
"""
import requests
import json
import time
from typing import Dict, Any

def test_cors_headers():
    """CORS 헤더를 직접 확인하는 테스트"""
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("CORS 디버깅 테스트 시작")
    print("=" * 60)
    
    # 1. 기본 헬스체크 테스트
    print("\n1. 헬스체크 테스트")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"상태 코드: {response.status_code}")
        print(f"응답 헤더:")
        for key, value in response.headers.items():
            if 'cors' in key.lower() or 'access-control' in key.lower() or 'origin' in key.lower():
                print(f"  {key}: {value}")
        print(f"응답 내용: {response.json()}")
    except Exception as e:
        print(f"헬스체크 실패: {e}")
    
    # 2. OPTIONS 요청 (프리플라이트) 테스트
    print("\n2. OPTIONS 요청 (프리플라이트) 테스트")
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{base_url}/api/v1/content/generate/simple", headers=headers)
        print(f"상태 코드: {response.status_code}")
        print(f"CORS 응답 헤더:")
        for key, value in response.headers.items():
            if 'cors' in key.lower() or 'access-control' in key.lower() or 'origin' in key.lower():
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"OPTIONS 요청 실패: {e}")
    
    # 3. 실제 POST 요청 테스트
    print("\n3. 실제 POST 요청 테스트")
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        data = {
            "prompt": "안녕하세요, 테스트 프롬프트입니다."
        }
        response = requests.post(
            f"{base_url}/api/v1/content/generate/simple", 
            headers=headers,
            json=data,
            timeout=30
        )
        print(f"상태 코드: {response.status_code}")
        print(f"CORS 응답 헤더:")
        for key, value in response.headers.items():
            if 'cors' in key.lower() or 'access-control' in key.lower() or 'origin' in key.lower():
                print(f"  {key}: {value}")
        
        if response.status_code == 200:
            print(f"응답 내용: {response.json()}")
        else:
            print(f"오류 응답: {response.text}")
    except Exception as e:
        print(f"POST 요청 실패: {e}")
    
    # 4. 모든 응답 헤더 출력
    print("\n4. 전체 응답 헤더 확인")
    try:
        response = requests.get(f"{base_url}/")
        print("모든 응답 헤더:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"헤더 확인 실패: {e}")

def test_different_origins():
    """다양한 Origin에서의 요청 테스트"""
    base_url = "http://localhost:8000"
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # 허용되지 않는 포트
        "https://localhost:3000",  # HTTPS
    ]
    
    print("\n" + "=" * 60)
    print("다양한 Origin 테스트")
    print("=" * 60)
    
    for origin in origins:
        print(f"\nOrigin: {origin}")
        try:
            headers = {'Origin': origin}
            response = requests.get(f"{base_url}/health", headers=headers)
            cors_header = response.headers.get('access-control-allow-origin', 'NOT_SET')
            print(f"  상태: {response.status_code}")
            print(f"  Access-Control-Allow-Origin: {cors_header}")
        except Exception as e:
            print(f"  오류: {e}")

def test_server_running():
    """서버가 실행 중인지 확인"""
    base_url = "http://localhost:8000"
    
    print("\n" + "=" * 60)
    print("서버 실행 상태 확인")
    print("=" * 60)
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"서버 상태: 실행 중 (상태 코드: {response.status_code})")
        print(f"응답: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("서버 상태: 실행되지 않음 (연결 거부)")
        return False
    except Exception as e:
        print(f"서버 확인 실패: {e}")
        return False

if __name__ == "__main__":
    # 서버 실행 상태 확인
    if not test_server_running():
        print("\n백엔드 서버가 실행되지 않았습니다.")
        print("다음 명령으로 서버를 시작하세요:")
        print("cd d:\\FinalProjects\\Marketing-Platform\\backend")
        print("python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
        exit(1)
    
    # CORS 테스트 실행
    test_cors_headers()
    test_different_origins()
    
    print("\n" + "=" * 60)
    print("CORS 디버깅 완료")
    print("=" * 60)

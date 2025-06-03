#!/usr/bin/env python3
"""
이미지 생성 API 테스트 스크립트
"""
import requests
import json
import time

def test_image_generation():
    """이미지 생성 API 테스트"""
    url = "http://127.0.0.1:8001/api/v1/content/generate-image"
    
    # 테스트 요청 데이터
    test_data = {
        "prompt": "A professional marketing image for a modern coffee shop with warm lighting and cozy atmosphere",
        "business_name": "Cozy Corner Cafe",
        "business_category": "카페/음료",
        "style": "professional"
    }
    
    print("=== 이미지 생성 API 테스트 ===")
    print(f"URL: {url}")
    print(f"Request Data: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    print()
    
    try:
        # API 호출
        print("이미지 생성 요청 중...")
        start_time = time.time()
        
        response = requests.post(url, json=test_data, timeout=60)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"응답 시간: {elapsed_time:.2f}초")
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 성공!")
            print(f"응답 데이터: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("success"):
                print(f"✅ 이미지가 성공적으로 생성되었습니다!")
                print(f"이미지 URL: {result.get('image_url')}")
                print(f"파일명: {result.get('filename')}")
                  # 이미지 파일 접근 테스트
                if result.get("image_url"):
                    image_url = f"http://127.0.0.1:8001{result['image_url']}"
                    print(f"이미지 접근 URL: {image_url}")
                    
                    try:
                        img_response = requests.get(image_url)
                        if img_response.status_code == 200:
                            print("✅ 이미지 파일에 성공적으로 접근했습니다!")
                            print(f"이미지 크기: {len(img_response.content)} bytes")
                        else:
                            print(f"❌ 이미지 접근 실패: {img_response.status_code}")
                    except Exception as e:
                        print(f"❌ 이미지 접근 오류: {e}")
            else:
                print(f"❌ 이미지 생성 실패: {result.get('error')}")
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(f"응답: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ 요청 시간 초과 (60초)")
    except requests.exceptions.ConnectionError:
        print("❌ 서버 연결 실패. 백엔드 서버가 실행 중인지 확인하세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def test_api_endpoints():
    """기본 API 엔드포인트 테스트"""
    base_url = "http://127.0.0.1:8001"
    
    print("\n=== API 엔드포인트 테스트 ===")
    
    # Health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code}")
    except:
        print("Root endpoint: 접근 불가")
    
    # API docs
    try:
        response = requests.get(f"{base_url}/docs")
        print(f"API docs: {response.status_code}")
    except:
        print("API docs: 접근 불가")

if __name__ == "__main__":
    test_api_endpoints()
    test_image_generation()

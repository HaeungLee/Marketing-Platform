#!/usr/bin/env python3
"""
이미지 생성 API 테스트 스크립트
"""
import requests
import json
import base64
from pathlib import Path

# API 엔드포인트
BASE_URL = "http://localhost:8000"
IMAGE_ENDPOINT = f"{BASE_URL}/api/images/generate"

def test_image_generation():
    """이미지 생성 API 테스트"""
    print("🎨 이미지 생성 API 테스트 시작...")
    
    # 테스트 프롬프트
    test_prompts = [
        "A beautiful sunset over a mountain landscape",
        "고양이와 강아지가 함께 노는 모습",
        "Abstract colorful digital art with geometric shapes"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n📝 테스트 {i}: {prompt}")
        
        try:
            # API 요청
            response = requests.post(
                IMAGE_ENDPOINT,
                json={"prompt": prompt},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                image_data = data.get("image_data")
                
                if image_data:
                    # Base64 이미지를 파일로 저장
                    output_file = f"test_image_{i}.png"
                    
                    # Base64 디코딩
                    try:
                        image_bytes = base64.b64decode(image_data)
                        with open(output_file, "wb") as f:
                            f.write(image_bytes)
                        print(f"✅ 성공: 이미지가 {output_file}에 저장되었습니다")
                    except Exception as e:
                        print(f"❌ Base64 디코딩 오류: {e}")
                else:
                    print("❌ 응답에 image_data가 없습니다")
            else:
                print(f"❌ API 오류 (상태 코드: {response.status_code})")
                print(f"응답: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 네트워크 오류: {e}")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")

def test_health_check():
    """헬스 체크 테스트"""
    print("\n🏥 헬스 체크 테스트...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 서버 상태: {data.get('status')}")
            print(f"버전: {data.get('version')}")
        else:
            print(f"❌ 헬스 체크 실패 (상태 코드: {response.status_code})")
    except Exception as e:
        print(f"❌ 헬스 체크 오류: {e}")

if __name__ == "__main__":
    # 헬스 체크 먼저 실행
    test_health_check()
    
    # 이미지 생성 테스트
    test_image_generation()
    
    print("\n🎯 테스트 완료!")

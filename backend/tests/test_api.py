#!/usr/bin/env python3
"""
API 테스트 스크립트
"""
import requests
import json
import time

def test_api_endpoint(url, description):
    """API 엔드포인트 테스트"""
    try:
        print(f"🔍 테스트 중: {description}")
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공 (상태코드: {response.status_code})")
            print(f"   📊 응답 데이터 미리보기:")
            print(f"   {json.dumps(data, ensure_ascii=False, indent=2)[:500]}...")
            return True
        else:
            print(f"   ❌ 실패 (상태코드: {response.status_code})")
            print(f"   오류 내용: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ 연결 실패: 서버가 실행되지 않았을 수 있습니다.")
        return False
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚀 인구 통계 API 테스트를 시작합니다...\n")
    
    base_url = "http://localhost:8000"
    
    # 테스트할 엔드포인트들
    test_cases = [
        (f"{base_url}/", "루트 엔드포인트"),
        (f"{base_url}/health", "헬스체크"),
        (f"{base_url}/api/population/summary", "인구 통계 요약"),
        (f"{base_url}/api/population/statistics", "인구 통계 데이터"),
        (f"{base_url}/api/population/statistics?city=인천", "인천시 인구 통계"),
        (f"{base_url}/api/population/age-distribution", "연령대별 분포"),
        (f"{base_url}/api/population/income-distribution", "소득 분포"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for url, description in test_cases:
        if test_api_endpoint(url, description):
            success_count += 1
        print()  # 빈 줄 추가
        time.sleep(1)  # 1초 대기
    
    print(f"📊 테스트 결과: {success_count}/{total_count} 성공")
    
    if success_count == total_count:
        print("🎉 모든 API 테스트가 성공했습니다!")
    elif success_count > 0:
        print("⚠️  일부 API가 작동하지 않습니다. 로그를 확인해주세요.")
    else:
        print("❌ 모든 API가 실패했습니다. 서버 상태를 확인해주세요.")

if __name__ == "__main__":
    main()

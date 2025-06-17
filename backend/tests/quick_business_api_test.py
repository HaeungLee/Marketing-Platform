"""
소상공인시장진흥공단 API 간단 테스트
빠른 연결 및 응답 확인용
"""

import requests
import json
from datetime import datetime

def quick_api_test():
    """빠른 API 연결 테스트"""
    
    # API 정보
    base_url = "https://apis.data.go.kr/B553077/api/open/sdsc2"
    api_key_encoded = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb%2FcuUI4dZSKEukcnq1me2b99jyFg%3D%3D"
    
    # 기본 파라미터
    params = {
        "serviceKey": api_key_encoded,
        "type": "json",
        "numOfRows": 3,
        "pageNo": 1
    }
    
    print("🔄 소상공인시장진흥공단 API 연결 테스트 시작...")
    print(f"📡 URL: {base_url}")
    print(f"🔑 API Key: {api_key_encoded[:20]}...")
    
    try:
        # API 호출
        response = requests.get(base_url, params=params, timeout=10)
        
        print(f"\n📊 응답 정보:")
        print(f"   - 상태 코드: {response.status_code}")
        print(f"   - 응답 크기: {len(response.content)} bytes")
        print(f"   - Content-Type: {response.headers.get('content-type', 'unknown')}")
        print(f"   - 실제 요청 URL: {response.url}")
        
        # 응답 내용 확인
        if response.status_code == 200:
            print("\n✅ API 호출 성공!")
            
            # JSON 파싱 시도
            try:
                data = response.json()
                print(f"📋 JSON 데이터 구조:")
                print(f"   - 타입: {type(data)}")
                
                if isinstance(data, dict):
                    print(f"   - 주요 키: {list(data.keys())}")
                    
                    # 첫 번째 레벨 구조 출력
                    for key, value in data.items():
                        print(f"   - {key}: {type(value).__name__}")
                        if isinstance(value, dict) and len(value) < 10:
                            for sub_key in list(value.keys())[:5]:
                                print(f"     └─ {sub_key}: {type(value[sub_key]).__name__}")
                        elif isinstance(value, list) and value:
                            print(f"     └─ 배열 길이: {len(value)}")
                            if isinstance(value[0], dict):
                                print(f"     └─ 첫 번째 항목 키: {list(value[0].keys())[:5]}")
                
                # 원본 데이터 샘플 저장
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"business_store_api_sample_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"\n💾 샘플 데이터 저장: {filename}")
                
                # 응답 일부 출력
                response_preview = json.dumps(data, ensure_ascii=False, indent=2)[:1000]
                print(f"\n📄 응답 데이터 미리보기 (처음 1000자):")
                print(response_preview + "...")
                
            except json.JSONDecodeError:
                print("⚠️  JSON 파싱 실패, 원시 텍스트로 확인:")
                print(response.text[:500] + "...")
                
        else:
            print(f"\n❌ API 호출 실패 (상태 코드: {response.status_code})")
            print(f"오류 내용: {response.text[:500]}")
            
            # 디코딩된 키로 재시도
            print("\n🔄 디코딩된 키로 재시도...")
            api_key_decoded = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg=="
            params["serviceKey"] = api_key_decoded
            
            response2 = requests.get(base_url, params=params, timeout=10)
            print(f"재시도 결과: {response2.status_code}")
            
            if response2.status_code == 200:
                print("✅ 디코딩된 키로 성공!")
                try:
                    data = response2.json()
                    print(f"데이터 타입: {type(data)}")
                    if isinstance(data, dict):
                        print(f"주요 키: {list(data.keys())}")
                except:
                    print("JSON 파싱 실패")
            else:
                print(f"❌ 재시도도 실패: {response2.text[:300]}")
    
    except requests.exceptions.Timeout:
        print("❌ 요청 타임아웃 (10초)")
    except requests.exceptions.RequestException as e:
        print(f"❌ 요청 오류: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")

if __name__ == "__main__":
    quick_api_test()

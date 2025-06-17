"""
새로운 API 키 간단 테스트
즉시 결과 확인용
"""

import requests
import json
import urllib.parse

def quick_test_new_key():
    print("🔑 새로운 API 키 즉시 테스트")
    print("="*40)
    
    # API 정보
    url = "https://apis.data.go.kr/B553077/api/open/sdsc2"
    key_encoded = "NIvbbY4jyxe6h7JNMil7S%2FOjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ%3D%3D"
    
    params = {
        "serviceKey": key_encoded,
        "type": "json",
        "numOfRows": 3,
        "pageNo": 1
    }
    
    print(f"URL: {url}")
    print(f"Key: {key_encoded[:20]}...")
    
    try:
        print("\n🔄 API 호출 중...")
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Size: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ 성공!")
            try:
                data = response.json()
                print(f"Data type: {type(data)}")
                if isinstance(data, dict):
                    print(f"Keys: {list(data.keys())}")
                    
                # 파일 저장
                with open("api_success_result.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("💾 Saved: api_success_result.json")
                
                # 간단 미리보기
                preview = str(data)[:300] + "..."
                print(f"Preview: {preview}")
                
            except:
                print("JSON 파싱 실패")
                print(f"Raw: {response.text[:200]}...")
        else:
            print("❌ 실패")
            print(f"Error: {response.text[:200]}")
            
            # 디코딩 키로 재시도
            print("\n🔄 디코딩 키로 재시도...")
            key_decoded = urllib.parse.unquote(key_encoded)
            params["serviceKey"] = key_decoded
            
            response2 = requests.get(url, params=params, timeout=10)
            print(f"Retry status: {response2.status_code}")
            
            if response2.status_code == 200:
                print("✅ 디코딩 키로 성공!")
                try:
                    data = response2.json()
                    with open("api_decoded_success_result.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    print("💾 Saved: api_decoded_success_result.json")
                except:
                    print("JSON 파싱 실패")
            else:
                print(f"재시도도 실패: {response2.text[:100]}")
    
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    quick_test_new_key()

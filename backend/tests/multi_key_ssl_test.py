"""
이전 API 키들과 새 API 키 비교 테스트
SSL 문제 해결과 함께 다양한 키 테스트
"""

import requests
import json
from datetime import datetime
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_multiple_api_keys():
    """여러 API 키로 테스트"""
    
    print("🔑 다중 API 키 테스트")
    print("=" * 50)
    
    # 테스트할 API 키들
    api_keys = {
        "이전키1_인코딩": "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb%2FcuUI4dZSKEukcnq1me2b99jyFg%3D%3D",
        "이전키1_디코딩": "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg==",
        "새키_인코딩": "NIvbbY4jyxe6h7JNMil7S%2FOjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ%3D%3D",
        "새키_디코딩": "NIvbbY4jyxe6h7JNMil7S/OjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ=="
    }
    
    # 간단한 엔드포인트
    base_url = "https://apis.data.go.kr/B553077/api/open"
    endpoint = "largeUpjongList"
    
    successful_keys = []
    
    for key_name, api_key in api_keys.items():
        print(f"\n🧪 테스트 키: {key_name}")
        print("-" * 30)
        
        url = f"{base_url}/{endpoint}"
        params = {
            "serviceKey": api_key,
            "type": "json"
        }
        
        # 다양한 설정으로 테스트
        configs = [
            {"verify": False, "name": "SSL_비활성화"},
            {"verify": True, "name": "SSL_활성화"}
        ]
        
        for config in configs:
            print(f"  🔒 {config['name']} 테스트")
            
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=10,
                    verify=config['verify'],
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
                
                print(f"    📡 상태: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"    ✅ 성공!")
                    successful_keys.append(f"{key_name} ({config['name']})")
                    
                    try:
                        data = response.json()
                        
                        # 기본 구조 확인
                        if "response" in data:
                            resp = data["response"]
                            if "header" in resp:
                                result_code = resp["header"].get("resultCode", "unknown")
                                result_msg = resp["header"].get("resultMsg", "unknown")
                                print(f"    📋 결과: {result_code} - {result_msg}")
                                
                                if result_code == "00":
                                    print(f"    🎉 정상 응답!")
                                    
                                    # 성공한 키로 상가 데이터 테스트
                                    test_store_data_with_key(api_key, config['verify'])
                                    return api_key, config['verify']
                                else:
                                    print(f"    ⚠️ API 오류: {result_msg}")
                    
                    except json.JSONDecodeError:
                        print(f"    ⚠️ JSON 파싱 실패")
                        print(f"    응답: {response.text[:100]}...")
                
                elif response.status_code == 401:
                    print(f"    🔑 인증 실패 (키 문제)")
                    
                elif response.status_code == 403:
                    print(f"    🚫 접근 금지 (권한 문제)")
                    
                else:
                    print(f"    ❌ HTTP 오류: {response.status_code}")
                    
            except requests.exceptions.SSLError as e:
                print(f"    🔒 SSL 오류: {str(e)[:100]}...")
                
            except requests.exceptions.ConnectionError as e:
                print(f"    🌐 연결 오류: {str(e)[:100]}...")
                
            except Exception as e:
                print(f"    ❌ 기타 오류: {str(e)[:100]}...")
    
    print(f"\n📊 테스트 결과 요약:")
    if successful_keys:
        print(f"✅ 성공한 키 설정: {len(successful_keys)}개")
        for key in successful_keys:
            print(f"   - {key}")
    else:
        print(f"❌ 모든 키 설정 실패")
        
        # 추가 진단
        print(f"\n🔍 추가 진단:")
        test_network_connectivity()
    
    return None, None

def test_store_data_with_key(api_key, verify_ssl):
    """성공한 키로 상가 데이터 테스트"""
    
    print(f"\n🏪 성공한 키로 상가 데이터 테스트")
    print("-" * 40)
    
    base_url = "https://apis.data.go.kr/B553077/api/open"
    
    store_endpoints = [
        {
            "name": "storeListInRadius",
            "desc": "반경내 상가조회",
            "params": {
                "serviceKey": api_key,
                "type": "json",
                "radius": "500",
                "cx": "126.978",  # 서울 시청
                "cy": "37.566",
                "numOfRows": 3
            }
        },
        {
            "name": "storeListInDong", 
            "desc": "행정동별 상가조회",
            "params": {
                "serviceKey": api_key,
                "type": "json",
                "divId": "adongCd", 
                "key": "1168010100",  # 강남구 역삼동
                "numOfRows": 3
            }
        }
    ]
    
    for endpoint_info in store_endpoints:
        endpoint = endpoint_info["name"]
        desc = endpoint_info["desc"]
        params = endpoint_info["params"]
        
        print(f"\n🔍 {desc} 테스트")
        
        try:
            url = f"{base_url}/{endpoint}"
            
            response = requests.get(
                url,
                params=params,
                timeout=15,
                verify=verify_ssl,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            print(f"   📡 상태: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ 성공!")
                
                try:
                    data = response.json()
                    
                    if "response" in data and "body" in data["response"]:
                        body = data["response"]["body"]
                        total_count = body.get("totalCount", 0)
                        print(f"   📊 총 상가 수: {total_count:,}개")
                        
                        # 실제 반환된 상가 데이터 확인
                        if "items" in body and body["items"]:
                            items = body["items"]
                            
                            # 아이템 구조 정규화
                            if isinstance(items, list):
                                actual_items = items
                            elif isinstance(items, dict) and "item" in items:
                                item_data = items["item"]
                                actual_items = item_data if isinstance(item_data, list) else [item_data]
                            else:
                                actual_items = []
                            
                            print(f"   📦 반환된 상가: {len(actual_items)}개")
                            
                            if actual_items and isinstance(actual_items[0], dict):
                                first_store = actual_items[0]
                                
                                # 상가 정보 출력
                                store_name = first_store.get("bizesNm", "정보없음")
                                store_type = first_store.get("indtyLclsNm", "정보없음")
                                address = first_store.get("rdnmAdr", first_store.get("lnmadr", "정보없음"))
                                
                                print(f"   🏷️ 첫 번째 상가:")
                                print(f"      상호: {store_name}")
                                print(f"      업종: {store_type}")
                                print(f"      주소: {address}")
                                
                                # 필드 정보
                                print(f"      필드 수: {len(first_store)}개")
                                print(f"      주요 필드: {list(first_store.keys())[:8]}")
                    
                    # 성공 데이터 저장
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"working_{endpoint}_{timestamp}.json"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"   💾 저장: {filename}")
                    
                except json.JSONDecodeError:
                    print(f"   ⚠️ JSON 파싱 실패")
            
            else:
                print(f"   ❌ 실패: {response.status_code}")
                print(f"   오류: {response.text[:100]}...")
        
        except Exception as e:
            print(f"   ❌ 오류: {e}")

def test_network_connectivity():
    """네트워크 연결성 테스트"""
    
    print(f"🌐 네트워크 연결성 진단")
    
    # 기본 연결 테스트
    test_urls = [
        "https://httpbin.org/get",  # 기본 HTTPS 테스트
        "https://apis.data.go.kr",  # 공공데이터 포털 기본 주소
        "http://apis.data.go.kr"    # HTTP 테스트
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5, verify=False)
            print(f"   ✅ {url}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {url}: {str(e)[:50]}...")

def main():
    """메인 테스트 실행"""
    print("🚀 종합 API 키 및 SSL 문제 해결 테스트")
    print("=" * 60)
    
    # 다중 키 테스트
    working_key, working_ssl = test_multiple_api_keys()
    
    if working_key:
        print(f"\n🎉 작동하는 설정을 찾았습니다!")
        print(f"   API 키: {working_key[:20]}...")
        print(f"   SSL 검증: {working_ssl}")
    else:
        print(f"\n❌ 모든 설정 실패")
        print(f"📝 권장사항:")
        print(f"   1. 공공데이터포털에서 API 키 재발급")
        print(f"   2. 네트워크 방화벽 설정 확인")
        print(f"   3. VPN 또는 프록시 사용 시 비활성화")
        print(f"   4. 다른 네트워크 환경에서 테스트")

if __name__ == "__main__":
    main()

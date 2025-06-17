"""
소상공인시장진흥공단 API SSL 문제 해결 및 인증키 테스트
다양한 SSL 설정과 인증키 형태로 테스트
"""

import requests
import json
import urllib3
from datetime import datetime
import ssl
import urllib.parse

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_with_ssl_fixes():
    """SSL 문제 해결을 위한 다양한 방법 테스트"""
    
    print("🔧 SSL 문제 해결 및 인증키 테스트")
    print("="*60)
    
    base_url = "https://apis.data.go.kr/B553077/api/open"
    
    # 다양한 인증키 형태 테스트
    api_keys = {
        "encoded": "NIvbbY4jyxe6h7JNMil7S%2FOjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ%3D%3D",
        "decoded": "NIvbbY4jyxe6h7JNMil7S/OjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ==",
        "manual_decode": urllib.parse.unquote("NIvbbY4jyxe6h7JNMil7S%2FOjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ%3D%3D")
    }
    
    # SSL 세션 설정들
    ssl_configs = [
        {
            "name": "기본_SSL",
            "verify": True,
            "headers": {'User-Agent': 'Mozilla/5.0'}
        },
        {
            "name": "SSL_검증_비활성화",
            "verify": False,
            "headers": {'User-Agent': 'Mozilla/5.0'}
        },
        {
            "name": "커스텀_헤더",
            "verify": False,
            "headers": {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
        }
    ]
    
    endpoint = "largeUpjongList"  # 가장 간단한 엔드포인트
    
    success_found = False
    
    for key_name, api_key in api_keys.items():
        for ssl_config in ssl_configs:
            print(f"\n🧪 테스트: {key_name} + {ssl_config['name']}")
            print("-" * 40)
            
            url = f"{base_url}/{endpoint}"
            params = {
                "serviceKey": api_key,
                "type": "json"
            }
            
            try:
                print(f"🔗 URL: {url}")
                print(f"🔑 키 타입: {key_name}")
                print(f"🔒 SSL 설정: {ssl_config['name']}")
                
                # 세션 생성
                session = requests.Session()
                
                # SSL 어댑터 설정 (더 관대한 SSL 설정)
                if not ssl_config['verify']:
                    session.verify = False
                    
                    # SSL 컨텍스트 설정
                    import ssl
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    
                    # TLS 버전 설정
                    context.minimum_version = ssl.TLSVersion.TLSv1
                    context.maximum_version = ssl.TLSVersion.TLSv1_3
                
                response = session.get(
                    url,
                    params=params,
                    timeout=15,
                    verify=ssl_config['verify'],
                    headers=ssl_config['headers']
                )
                
                print(f"📡 응답 상태: {response.status_code}")
                print(f"📏 응답 크기: {len(response.content):,} bytes")
                print(f"🌐 실제 URL: {response.url}")
                
                if response.status_code == 200:
                    print("✅ 성공!")
                    success_found = True
                    
                    try:
                        data = response.json()
                        
                        # 응답 구조 확인
                        if isinstance(data, dict):
                            print(f"📊 응답 키: {list(data.keys())}")
                            
                            if "response" in data:
                                resp = data["response"]
                                if "header" in resp:
                                    header = resp["header"]
                                    result_code = header.get("resultCode", "unknown")
                                    result_msg = header.get("resultMsg", "unknown")
                                    print(f"📋 결과: {result_code} - {result_msg}")
                                
                                if "body" in resp:
                                    body = resp["body"]
                                    total_count = body.get("totalCount", 0)
                                    print(f"📈 데이터 수: {total_count:,}개")
                        
                        # 성공한 설정 저장
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        success_filename = f"success_config_{timestamp}.json"
                        
                        success_config = {
                            "api_key_type": key_name,
                            "api_key": api_key,
                            "ssl_config": ssl_config,
                            "response_data": data,
                            "success_time": timestamp
                        }
                        
                        with open(success_filename, 'w', encoding='utf-8') as f:
                            json.dump(success_config, f, ensure_ascii=False, indent=2)
                        
                        print(f"💾 성공 설정 저장: {success_filename}")
                        
                        # 샘플 출력
                        sample = json.dumps(data, ensure_ascii=False, indent=2)[:400]
                        print(f"📄 응답 샘플:\n{sample}...")
                        
                        # 성공했으면 다른 엔드포인트도 테스트
                        if success_found:
                            test_other_endpoints(session, api_key, ssl_config)
                            return
                    
                    except json.JSONDecodeError:
                        print("⚠️ JSON 파싱 실패")
                        print(f"원시 응답: {response.text[:300]}...")
                
                else:
                    print(f"❌ HTTP 오류: {response.status_code}")
                    print(f"오류 내용: {response.text[:200]}...")
            
            except requests.exceptions.SSLError as e:
                print(f"🔒 SSL 오류: {e}")
                
            except requests.exceptions.ConnectionError as e:
                print(f"🌐 연결 오류: {e}")
                
            except requests.exceptions.Timeout:
                print("⏰ 타임아웃")
                
            except Exception as e:
                print(f"❌ 기타 오류: {e}")
    
    if not success_found:
        print(f"\n❌ 모든 설정 실패")
        print("🔍 추가 확인이 필요합니다:")
        print("   1. 인증키 유효성")
        print("   2. API 서비스 상태")
        print("   3. 네트워크 방화벽")

def test_other_endpoints(session, api_key, ssl_config):
    """성공한 설정으로 다른 엔드포인트들 테스트"""
    
    print(f"\n🎯 성공한 설정으로 다른 엔드포인트 테스트")
    print("=" * 50)
    
    base_url = "https://apis.data.go.kr/B553077/api/open"
    
    endpoints_to_test = [
        {
            "name": "middleUpjongList",
            "desc": "업종 중분류",
            "params": {"serviceKey": api_key, "type": "json"}
        },
        {
            "name": "storeListInRadius",
            "desc": "반경내 상가조회", 
            "params": {
                "serviceKey": api_key,
                "type": "json",
                "radius": "1000",
                "cx": "126.978",
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
    
    successful_endpoints = []
    
    for endpoint_info in endpoints_to_test:
        endpoint = endpoint_info["name"]
        desc = endpoint_info["desc"]
        params = endpoint_info["params"]
        
        print(f"\n🔍 테스트: {endpoint} ({desc})")
        print("-" * 30)
        
        try:
            url = f"{base_url}/{endpoint}"
            
            response = session.get(
                url,
                params=params,
                timeout=15,
                verify=ssl_config['verify'],
                headers=ssl_config['headers']
            )
            
            print(f"📡 상태: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 성공!")
                successful_endpoints.append(endpoint)
                
                try:
                    data = response.json()
                    
                    if "response" in data and "body" in data["response"]:
                        body = data["response"]["body"]
                        total_count = body.get("totalCount", 0)
                        print(f"   데이터 수: {total_count:,}개")
                        
                        # 실제 아이템 확인
                        if "items" in body and body["items"]:
                            items = body["items"]
                            if isinstance(items, list):
                                actual_items = items
                            elif isinstance(items, dict) and "item" in items:
                                actual_items = items["item"]
                                if not isinstance(actual_items, list):
                                    actual_items = [actual_items]
                            else:
                                actual_items = []
                            
                            print(f"   반환 아이템: {len(actual_items)}개")
                            
                            # 상가 정보의 경우 추가 정보 출력
                            if actual_items and "store" in endpoint.lower():
                                first_item = actual_items[0]
                                if isinstance(first_item, dict):
                                    store_name = first_item.get("bizesNm", "정보없음")
                                    store_type = first_item.get("indtyLclsNm", "정보없음")
                                    print(f"   첫 번째 상가: {store_name} ({store_type})")
                    
                    # 결과 저장
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{endpoint}_success_{timestamp}.json"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"   💾 저장: {filename}")
                
                except json.JSONDecodeError:
                    print("   ⚠️ JSON 파싱 실패")
            
            else:
                print(f"❌ 실패: {response.status_code}")
                print(f"   오류: {response.text[:150]}...")
        
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    print(f"\n📊 최종 결과:")
    print(f"   성공한 엔드포인트: {len(successful_endpoints)}개")
    for endpoint in successful_endpoints:
        print(f"   - {endpoint}")

def test_alternative_approach():
    """대안 접근 방법 테스트"""
    
    print(f"\n🔄 대안 접근 방법 테스트")
    print("=" * 40)
    
    # HTTP로 테스트 (HTTPS 문제 회피)
    http_base_url = "http://apis.data.go.kr/B553077/api/open"
    api_key = "NIvbbY4jyxe6h7JNMil7S/OjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ=="
    
    endpoint = "largeUpjongList"
    url = f"{http_base_url}/{endpoint}"
    
    params = {
        "serviceKey": api_key,
        "type": "json"
    }
    
    print(f"🔗 HTTP URL 테스트: {url}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📡 HTTP 응답: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ HTTP로 성공!")
            
            try:
                data = response.json()
                print(f"📊 데이터 타입: {type(data)}")
                
                # 샘플 저장
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"http_success_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"💾 HTTP 성공 데이터 저장: {filename}")
                
            except json.JSONDecodeError:
                print("⚠️ JSON 파싱 실패")
        else:
            print(f"❌ HTTP도 실패: {response.status_code}")
            print(f"내용: {response.text[:200]}...")
    
    except Exception as e:
        print(f"❌ HTTP 테스트 오류: {e}")

def main():
    """메인 테스트 실행"""
    test_with_ssl_fixes()
    test_alternative_approach()

if __name__ == "__main__":
    main()

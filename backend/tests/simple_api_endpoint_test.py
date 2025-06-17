"""
소상공인시장진흥공단 API 간단한 엔드포인트 확인 테스트
새 인증키로 가장 기본적인 API부터 테스트
"""

import requests
import json
from datetime import datetime

def quick_endpoint_test():
    """가장 간단한 엔드포인트부터 테스트"""
    
    print("🚀 소상공인시장진흥공단 API 간단 엔드포인트 테스트")
    print("🔑 새 인증키 사용")
    print("="*60)
    
    base_url = "https://apis.data.go.kr/B553077/api/open"
    api_key = "NIvbbY4jyxe6h7JNMil7S%2FOjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ%3D%3D"
    
    # 가장 간단한 엔드포인트들부터 테스트 (파라미터 불필요)
    simple_endpoints = [
        "largeUpjongList",    # 업종 대분류
        "middleUpjongList",   # 업종 중분류  
        "smallUpjongList"     # 업종 소분류
    ]
    
    successful_apis = []
    
    for endpoint in simple_endpoints:
        print(f"\n🔍 테스트: {endpoint}")
        print("-" * 30)
        
        url = f"{base_url}/{endpoint}"
        params = {
            "serviceKey": api_key,
            "type": "json"
        }
        
        try:
            print(f"📡 요청 URL: {url}")
            response = requests.get(url, params=params, timeout=10)
            
            print(f"📊 상태 코드: {response.status_code}")
            print(f"📏 응답 크기: {len(response.content):,} bytes")
            
            if response.status_code == 200:
                print("✅ 성공!")
                successful_apis.append(endpoint)
                
                try:
                    data = response.json()
                    
                    # 기본 구조 확인
                    if isinstance(data, dict) and "response" in data:
                        resp = data["response"]
                        
                        if "header" in resp:
                            header = resp["header"]
                            result_code = header.get("resultCode", "unknown")
                            result_msg = header.get("resultMsg", "unknown")
                            print(f"   결과 코드: {result_code}")
                            print(f"   결과 메시지: {result_msg}")
                        
                        if "body" in resp:
                            body = resp["body"]
                            total_count = body.get("totalCount", 0)
                            print(f"   전체 데이터 수: {total_count:,}개")
                            
                            # 아이템 확인
                            if "items" in body:
                                items = body["items"]
                                if isinstance(items, list):
                                    print(f"   반환된 아이템: {len(items)}개")
                                    if items:
                                        first_item = items[0]
                                        if isinstance(first_item, dict):
                                            print(f"   아이템 필드: {list(first_item.keys())}")
                                elif isinstance(items, dict) and "item" in items:
                                    item_list = items["item"]
                                    if isinstance(item_list, list):
                                        print(f"   반환된 아이템: {len(item_list)}개")
                                    else:
                                        print(f"   단일 아이템")
                    
                    # 샘플 저장
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"simple_{endpoint}_{timestamp}.json"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"   💾 저장: {filename}")
                    
                    # 샘플 출력
                    sample = json.dumps(data, ensure_ascii=False, indent=2)[:300]
                    print(f"   📄 샘플: {sample}...")
                    
                except json.JSONDecodeError:
                    print("   ⚠️ JSON 파싱 실패")
                    print(f"   원시 응답: {response.text[:200]}...")
            
            else:
                print(f"❌ 실패 (상태: {response.status_code})")
                print(f"   오류: {response.text[:200]}...")
                
                # 디코딩된 키로 재시도
                print("   🔄 디코딩된 키로 재시도...")
                decoded_key = "NIvbbY4jyxe6h7JNMil7S/OjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ=="
                params["serviceKey"] = decoded_key
                
                retry_response = requests.get(url, params=params, timeout=10)
                print(f"   재시도 상태: {retry_response.status_code}")
                
                if retry_response.status_code == 200:
                    print("   ✅ 디코딩된 키로 성공!")
                    successful_apis.append(f"{endpoint} (decoded)")
        
        except requests.exceptions.Timeout:
            print("❌ 타임아웃")
        except Exception as e:
            print(f"❌ 오류: {e}")
    
    # 성공한 API로 상가 데이터 테스트
    if successful_apis:
        print(f"\n🎉 성공한 API: {len(successful_apis)}개")
        for api in successful_apis:
            print(f"   - {api}")
        
        print(f"\n🏪 상가 데이터 API 테스트")
        test_store_apis()
    else:
        print(f"\n❌ 모든 API 실패")

def test_store_apis():
    """상가 데이터 API 테스트"""
    
    base_url = "https://apis.data.go.kr/B553077/api/open"
    api_key = "NIvbbY4jyxe6h7JNMil7S%2FOjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ%3D%3D"
    
    store_tests = [
        {
            "name": "반경내 상가 조회",
            "endpoint": "storeListInRadius",
            "params": {
                "serviceKey": api_key,
                "type": "json",
                "radius": "500",
                "cx": "126.978",   # 서울 시청 경도
                "cy": "37.566",    # 서울 시청 위도
                "numOfRows": 5
            }
        },
        {
            "name": "행정동별 상가 조회",
            "endpoint": "storeListInDong", 
            "params": {
                "serviceKey": api_key,
                "type": "json",
                "divId": "adongCd",
                "key": "1165010100",  # 서울 서초구 서초동
                "numOfRows": 5
            }
        },
        {
            "name": "업종별 상가 조회",
            "endpoint": "storeListInUpjong",
            "params": {
                "serviceKey": api_key,
                "type": "json", 
                "divId": "indsLclsCd",
                "key": "I",  # 숙박 및 음식점업
                "numOfRows": 5
            }
        }
    ]
    
    for test in store_tests:
        print(f"\n🔍 {test['name']}")
        print("-" * 30)
        
        url = f"{base_url}/{test['endpoint']}"
        
        try:
            response = requests.get(url, params=test['params'], timeout=15)
            
            print(f"📊 상태: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 성공!")
                
                try:
                    data = response.json()
                    
                    if "response" in data and "body" in data["response"]:
                        body = data["response"]["body"]
                        total_count = body.get("totalCount", 0)
                        print(f"   총 상가 수: {total_count:,}개")
                        
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
                            
                            print(f"   반환된 상가: {len(actual_items)}개")
                            
                            if actual_items and isinstance(actual_items[0], dict):
                                first_store = actual_items[0]
                                
                                # 주요 정보 출력
                                store_name = first_store.get("bizesNm", "정보없음")
                                store_type = first_store.get("indtyLclsNm", "정보없음")
                                address = first_store.get("rdnmAdr", first_store.get("lnmadr", "정보없음"))
                                
                                print(f"   📍 첫 번째 상가:")
                                print(f"      상호명: {store_name}")
                                print(f"      업종: {store_type}")
                                print(f"      주소: {address}")
                                
                                # 필드 목록
                                print(f"      필드 수: {len(first_store)}개")
                                print(f"      주요 필드: {list(first_store.keys())[:10]}")
                    
                    # 결과 저장
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"store_{test['endpoint']}_{timestamp}.json"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"   💾 저장: {filename}")
                    
                except json.JSONDecodeError:
                    print("   ⚠️ JSON 파싱 실패")
            
            else:
                print(f"❌ 실패: {response.status_code}")
                print(f"   오류: {response.text[:200]}...")
        
        except Exception as e:
            print(f"❌ 오류: {e}")

def main():
    quick_endpoint_test()

if __name__ == "__main__":
    main()

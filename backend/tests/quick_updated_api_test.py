"""
소상공인시장진흥공단 API 업데이트 버전 간단 테스트
HTTPS 및 변경사항 빠른 확인
"""

import requests
import json
from datetime import datetime

def test_updated_api():
    """업데이트된 API 간단 테스트"""
    
    print("🔄 소상공인시장진흥공단 API 업데이트 테스트")
    print("📅 2025년 6월 11일 업데이트 변경사항 확인")
    print("="*50)
    
    # HTTPS URL (업데이트된 주소)
    base_url = "https://apis.data.go.kr/B553077/api/open/sdsc2"
    api_key = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb%2FcuUI4dZSKEukcnq1me2b99jyFg%3D%3D"
    
    params = {
        "serviceKey": api_key,
        "type": "json",
        "numOfRows": 5,
        "pageNo": 1
    }
    
    print(f"🔗 요청 URL: {base_url}")
    print(f"🔒 HTTPS 사용: {'✅' if base_url.startswith('https://') else '❌'}")
    
    try:
        # HTTPS 요청
        response = requests.get(base_url, params=params, timeout=15, verify=True)
        
        print(f"\n📡 응답 정보:")
        print(f"   상태 코드: {response.status_code}")
        print(f"   HTTPS 확인: {'✅' if response.url.startswith('https://') else '❌'}")
        print(f"   응답 크기: {len(response.content):,} bytes")
        print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200:
            print("\n✅ API 호출 성공!")
            
            try:
                data = response.json()
                
                # 기본 구조 분석
                print(f"\n📊 데이터 구조:")
                if isinstance(data, dict):
                    print(f"   타입: Dictionary")
                    print(f"   주요 키: {list(data.keys())}")
                    
                    # 응답 데이터에서 아이템 찾기
                    items = []
                    if "response" in data and "body" in data["response"]:
                        body = data["response"]["body"]
                        if "items" in body:
                            if isinstance(body["items"], list):
                                items = body["items"]
                            elif isinstance(body["items"], dict) and "item" in body["items"]:
                                items = body["items"]["item"]
                                if not isinstance(items, list):
                                    items = [items]
                    
                    print(f"   찾은 아이템 수: {len(items)}")
                    
                    # 좌표 데이터 확인 (업데이트: 4,300 → 250,000)
                    if items:
                        print(f"\n🗺️ 좌표 데이터 분석:")
                        coord_fields_found = []
                        max_coord_length = 0
                        
                        for i, item in enumerate(items[:3]):  # 처음 3개만 확인
                            if isinstance(item, dict):
                                for key, value in item.items():
                                    # 좌표 관련 필드 찾기
                                    if any(coord_keyword in key.lower() for coord_keyword in ['coord', 'geom', 'polygon', 'wkt']):
                                        coord_fields_found.append(key)
                                        if value:
                                            coord_length = len(str(value))
                                            max_coord_length = max(max_coord_length, coord_length)
                                            
                                            print(f"   아이템 {i+1} - {key}: {coord_length:,} 문자")
                                            
                                            # POLYGON vs MULTIPOLYGON 확인
                                            value_str = str(value).upper()
                                            if "MULTIPOLYGON" in value_str:
                                                print(f"      ⚠️ MULTIPOLYGON 발견 (구 형식)")
                                            elif "POLYGON" in value_str:
                                                print(f"      ✅ POLYGON 확인 (신 형식)")
                                            
                                            # 좌표 샘플 출력
                                            sample = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                                            print(f"      샘플: {sample}")
                        
                        if coord_fields_found:
                            print(f"   발견된 좌표 필드: {set(coord_fields_found)}")
                            print(f"   최대 좌표 길이: {max_coord_length:,} 문자")
                            
                            # 업데이트 확인
                            if max_coord_length > 4300:
                                print(f"   ✅ 좌표 확장 적용됨 (4,300 → 250,000 한도)")
                            else:
                                print(f"   ⚠️ 기존 크기 범위 ({max_coord_length:,} ≤ 4,300)")
                        else:
                            print(f"   ⚠️ 좌표 필드를 찾을 수 없음")
                    
                    # 데이터 소스 확인 (상권정보시스템 → 소상공인365)
                    print(f"\n🏢 데이터 소스 분석:")
                    response_text = json.dumps(data, ensure_ascii=False).lower()
                    
                    if "소상공인365" in response_text or "sbiz365" in response_text:
                        print(f"   ✅ 소상공인365 데이터 소스 확인")
                    elif "상권정보시스템" in response_text:
                        print(f"   ⚠️ 기존 상권정보시스템 소스")
                    else:
                        print(f"   ℹ️ 데이터 소스 정보 확인 필요")
                    
                    # 응답 샘플 저장
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"updated_api_sample_{timestamp}.json"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"\n💾 응답 데이터 저장: {filename}")
                    
                    # 주요 업데이트 적용 상태 요약
                    print(f"\n📋 업데이트 적용 상태:")
                    print(f"   1. HTTPS 전환: ✅")
                    print(f"   2. 좌표 확장: {'✅' if max_coord_length > 4300 else '⚠️'}")
                    print(f"   3. POLYGON 형식: {'확인필요' if not coord_fields_found else '확인됨'}")
                    print(f"   4. 데이터 소스: {'소상공인365' if '소상공인365' in response_text else '확인필요'}")
                
            except json.JSONDecodeError:
                print("❌ JSON 파싱 실패")
                print(f"응답 내용: {response.text[:300]}...")
        
        else:
            print(f"\n❌ API 호출 실패 (상태: {response.status_code})")
            print(f"오류 내용: {response.text[:300]}")
            
            # 디코딩된 키로 재시도
            print(f"\n🔄 디코딩된 키로 재시도...")
            params["serviceKey"] = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg=="
            
            retry_response = requests.get(base_url, params=params, timeout=15)
            print(f"재시도 결과: {retry_response.status_code}")
            
            if retry_response.status_code == 200:
                print("✅ 디코딩된 키로 성공!")
    
    except requests.exceptions.Timeout:
        print("❌ 요청 타임아웃")
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL 오류: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_updated_api()

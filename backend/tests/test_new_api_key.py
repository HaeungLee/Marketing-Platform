"""
소상공인시장진흥공단 API 새 인증키 및 올바른 엔드포인트 테스트
실제 API 목록을 사용한 데이터 호출 테스트
인증키: NIvbbY4jyxe6h7JNMil7S%2FOjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ%3D%3D
"""

import requests
import json
from datetime import datetime
import time
from typing import Dict, Any, List, Optional

class NewBusinessStoreAPIClient:
    """새 인증키를 사용한 소상공인시장진흥공단 API 클라이언트"""
    
    def __init__(self):
        self.base_url = "https://apis.data.go.kr/B553077/api/open"
        self.api_key_encoded = "NIvbbY4jyxe6h7JNMil7S%2FOjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ%3D%3D"
        self.api_key_decoded = "NIvbbY4jyxe6h7JNMil7S/OjCzyhdcWfsxtd2IrRvcnm73dJHdlTHhVFJFCN6FxQr5HlUOJIwGpLIUR3qg7spQ=="
        
        # 사용 가능한 API 엔드포인트들
        self.endpoints = {
            "baroApi": "행정경계조회",
            "storeListInDong": "행정동 단위 상가업소 조회", 
            "storeOne": "단일 상가업소 조회",
            "storeListInBuilding": "건물 단위 상가업소 조회",
            "storeListInPnu": "지번 단위 상가업소 조회",
            "storeListInArea": "상권내 상가업소 조회",
            "storeListInRadius": "반경내 상가업소 조회",
            "storeListInRectangle": "사각형내 상가업소 조회",
            "storeListInPolygon": "다각형내 상가업소 조회",
            "storeListInUpjong": "업종별 상가업소 조회",
            "storeListByDate": "수정일자기준 상가업소 조회",
            "reqStoreModify": "상가업소정보 변경요청",
            "largeUpjongList": "상권정보 업종 대분류 조회",
            "middleUpjongList": "상권정보 업종 중분류 조회", 
            "smallUpjongList": "상권정보 업종 소분류 조회",
            "storeZoneInRectangle": "사각형내 상권조회"
        }
    
    def make_api_request(self, endpoint: str, params: Dict[str, Any] = None, use_decoded_key: bool = False) -> Optional[requests.Response]:
        """API 요청 실행"""
        try:
            # 기본 파라미터
            default_params = {
                "serviceKey": self.api_key_decoded if use_decoded_key else self.api_key_encoded,
                "type": "json",
                "numOfRows": 10,
                "pageNo": 1
            }
            
            if params:
                default_params.update(params)
            
            url = f"{self.base_url}/{endpoint}"
            
            print(f"🔗 요청 URL: {url}")
            print(f"🔑 사용 키: {'Decoded' if use_decoded_key else 'Encoded'}")
            print(f"📋 파라미터: {default_params}")
            
            response = requests.get(
                url,
                params=default_params,
                timeout=15,
                verify=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json'
                }
            )
            
            print(f"📡 응답 상태: {response.status_code}")
            print(f"📏 응답 크기: {len(response.content):,} bytes")
            
            return response
            
        except Exception as e:
            print(f"❌ 요청 오류: {e}")
            return None
    
    def test_basic_endpoints(self) -> Dict[str, Any]:
        """기본 엔드포인트들 테스트"""
        print("="*60)
        print("🧪 소상공인시장진흥공단 API 엔드포인트 테스트")
        print("="*60)
        
        results = {
            "test_timestamp": datetime.now().isoformat(),
            "api_key_used": "new_key",
            "successful_endpoints": [],
            "failed_endpoints": [],
            "endpoint_results": {}
        }
        
        # 테스트할 우선순위 엔드포인트 (파라미터가 필요 없는 것부터)
        priority_tests = [
            ("largeUpjongList", {}),  # 업종 대분류 - 파라미터 불필요
            ("middleUpjongList", {}),  # 업종 중분류 - 파라미터 불필요
            ("storeListInDong", {"divId": "adongCd", "key": "1165010100"}),  # 서울 서초구 서초동
            ("storeListInUpjong", {"divId": "indsLclsCd", "key": "Q"}),  # 보건업 및 사회복지서비스업
            ("storeListInRadius", {"radius": "500", "cx": "126.978", "cy": "37.566"}),  # 서울 시청 반경 500m
        ]
        
        for endpoint, test_params in priority_tests:
            print(f"\n🔍 테스트 중: {endpoint} - {self.endpoints.get(endpoint, '알 수 없는 API')}")
            
            # 먼저 인코딩된 키로 시도
            response = self.make_api_request(endpoint, test_params, use_decoded_key=False)
            
            if response and response.status_code == 200:
                success = self._process_successful_response(endpoint, response, results)
                if success:
                    results["successful_endpoints"].append(endpoint)
                    continue
            
            # 인코딩된 키 실패 시 디코딩된 키로 재시도
            print("🔄 디코딩된 키로 재시도...")
            response = self.make_api_request(endpoint, test_params, use_decoded_key=True)
            
            if response and response.status_code == 200:
                success = self._process_successful_response(endpoint, response, results)
                if success:
                    results["successful_endpoints"].append(endpoint)
                else:
                    results["failed_endpoints"].append(endpoint)
            else:
                print(f"❌ {endpoint} 실패")
                results["failed_endpoints"].append(endpoint)
                results["endpoint_results"][endpoint] = {
                    "status": "failed",
                    "error": f"Status: {response.status_code if response else 'None'}",
                    "response_text": response.text[:300] if response else "No response"
                }
            
            # API 호출 간격
            time.sleep(1)
        
        return results
    
    def _process_successful_response(self, endpoint: str, response: requests.Response, results: Dict[str, Any]) -> bool:
        """성공한 응답 처리"""
        try:
            print(f"✅ {endpoint} 성공!")
            
            # JSON 파싱
            data = response.json()
            
            # 기본 정보 출력
            print(f"   📊 데이터 타입: {type(data).__name__}")
            
            if isinstance(data, dict):
                print(f"   🔑 주요 키: {list(data.keys())}")
                
                # 표준 공공데이터 API 구조 확인
                if "response" in data:
                    resp = data["response"]
                    if "header" in resp:
                        header = resp["header"]
                        result_code = header.get("resultCode", "unknown")
                        result_msg = header.get("resultMsg", "unknown")
                        print(f"   📋 결과 코드: {result_code}")
                        print(f"   📝 결과 메시지: {result_msg}")
                        
                        if result_code != "00":
                            print(f"   ⚠️ API 오류: {result_msg}")
                            return False
                    
                    if "body" in resp:
                        body = resp["body"]
                        total_count = body.get("totalCount", 0)
                        print(f"   📈 총 데이터 수: {total_count:,}")
                        
                        # 아이템 확인
                        items = []
                        if "items" in body:
                            if isinstance(body["items"], list):
                                items = body["items"]
                            elif isinstance(body["items"], dict) and "item" in body["items"]:
                                items = body["items"]["item"]
                                if not isinstance(items, list):
                                    items = [items]
                        
                        print(f"   📦 반환된 아이템 수: {len(items)}")
                        
                        # 첫 번째 아이템 구조 분석
                        if items and isinstance(items[0], dict):
                            first_item = items[0]
                            print(f"   🏷️ 아이템 필드 수: {len(first_item)}")
                            print(f"   🔤 주요 필드: {list(first_item.keys())[:10]}")
                            
                            # 샘플 데이터 저장
                            sample_data = {
                                "endpoint": endpoint,
                                "total_count": total_count,
                                "sample_items": items[:3],  # 처음 3개만
                                "field_structure": {k: type(v).__name__ for k, v in first_item.items()}
                            }
                            
                            results["endpoint_results"][endpoint] = {
                                "status": "success",
                                "total_count": total_count,
                                "returned_items": len(items),
                                "sample_data": sample_data,
                                "response_size": len(response.content)
                            }
                            
                            return True
            
            print(f"   ⚠️ 예상과 다른 응답 구조")
            return False
            
        except json.JSONDecodeError:
            print(f"   ❌ JSON 파싱 실패")
            print(f"   📄 응답 내용: {response.text[:200]}...")
            return False
        except Exception as e:
            print(f"   ❌ 처리 오류: {e}")
            return False
    
    def save_results(self, results: Dict[str, Any]):
        """테스트 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 결과 저장
        filename = f"new_api_key_test_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 테스트 결과 저장: {filename}")
        
        # 요약 리포트 생성
        self._generate_summary_report(results, timestamp)
    
    def _generate_summary_report(self, results: Dict[str, Any], timestamp: str):
        """요약 리포트 생성"""
        report_filename = f"api_test_summary_{timestamp}.md"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("# 소상공인시장진흥공단 API 새 인증키 테스트 리포트\n\n")
            f.write(f"**테스트 일시:** {results['test_timestamp']}\n")
            f.write(f"**사용 인증키:** 새 키 (NIvbbY4j...)\n\n")
            
            f.write("## 테스트 결과 요약\n\n")
            f.write(f"- **성공한 엔드포인트:** {len(results['successful_endpoints'])}개\n")
            f.write(f"- **실패한 엔드포인트:** {len(results['failed_endpoints'])}개\n\n")
            
            if results['successful_endpoints']:
                f.write("### ✅ 성공한 API\n\n")
                for endpoint in results['successful_endpoints']:
                    description = self.endpoints.get(endpoint, '알 수 없음')
                    f.write(f"- **{endpoint}**: {description}\n")
                    
                    if endpoint in results['endpoint_results']:
                        result = results['endpoint_results'][endpoint]
                        total_count = result.get('total_count', 0)
                        returned_items = result.get('returned_items', 0)
                        f.write(f"  - 총 데이터: {total_count:,}개, 반환: {returned_items}개\n")
                f.write("\n")
            
            if results['failed_endpoints']:
                f.write("### ❌ 실패한 API\n\n")
                for endpoint in results['failed_endpoints']:
                    description = self.endpoints.get(endpoint, '알 수 없음')
                    f.write(f"- **{endpoint}**: {description}\n")
                f.write("\n")
            
            f.write("## 결론\n\n")
            if results['successful_endpoints']:
                f.write("✅ 새 인증키로 API 연결 성공\n")
                f.write("✅ 상가 데이터 정상 조회 가능\n")
                f.write("➡️ 프로덕션 환경에서 사용 가능\n\n")
            else:
                f.write("❌ API 연결 실패\n")
                f.write("➡️ 인증키 또는 파라미터 재확인 필요\n\n")
        
        print(f"📋 요약 리포트 생성: {report_filename}")


def main():
    """메인 테스트 실행"""
    print("🚀 소상공인시장진흥공단 API 새 인증키 테스트 시작")
    print("🔑 새 인증키: NIvbbY4j...spQ==")
    print("📡 HTTPS 엔드포인트 사용")
    
    client = NewBusinessStoreAPIClient()
    
    # 기본 엔드포인트 테스트
    results = client.test_basic_endpoints()
    
    # 결과 요약 출력
    print(f"\n" + "="*60)
    print("📊 최종 테스트 결과")
    print("="*60)
    print(f"✅ 성공: {len(results['successful_endpoints'])}개 API")
    print(f"❌ 실패: {len(results['failed_endpoints'])}개 API")
    
    if results['successful_endpoints']:
        print(f"\n🎉 사용 가능한 API:")
        for endpoint in results['successful_endpoints']:
            print(f"   - {endpoint}: {client.endpoints[endpoint]}")
    
    # 결과 저장
    client.save_results(results)
    
    return results['successful_endpoints']


if __name__ == "__main__":
    success_endpoints = main()

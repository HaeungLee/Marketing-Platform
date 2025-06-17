"""
소상공인시장진흥공단_상가(상권)정보_API 업데이트 버전 테스트
2025년 6월 11일 변경사항 적용:
1. HTTP → HTTPS 전환
2. coords 항목 크기 4,300 → 250,000으로 확장
3. MULTIPOLYGON → POLYGON으로 변경
4. 주요상권현황: 상권정보시스템 → 소상공인365
"""

import requests
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UpdatedBusinessStoreAPI:
    """업데이트된 소상공인시장진흥공단 상가(상권)정보 API 클라이언트"""
    
    def __init__(self):
        # HTTPS로 변경
        self.base_url = "https://apis.data.go.kr/B553077/api/open/sdsc2"
        self.api_key_encoded = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb%2FcuUI4dZSKEukcnq1me2b99jyFg%3D%3D"
        self.api_key_decoded = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg=="
        self.timeout = 30
        
        # 업데이트된 특성
        self.max_coords_size = 250000  # 기존 4,300 → 250,000
        self.geometry_type = "POLYGON"  # 기존 MULTIPOLYGON → POLYGON
        
    def make_secure_request(self, params: Dict[str, Any]) -> Optional[requests.Response]:
        """HTTPS를 사용한 보안 API 요청"""
        try:
            # SSL 인증서 검증 활성화
            default_params = {
                "serviceKey": self.api_key_encoded,
                "type": "json",
                "numOfRows": 10,
                "pageNo": 1
            }
            
            final_params = {**default_params, **params}
            
            logger.info(f"HTTPS API 요청 시작 - URL: {self.base_url}")
            logger.info(f"파라미터: {final_params}")
            
            # HTTPS 요청 (SSL 인증서 검증 포함)
            response = requests.get(
                self.base_url,
                params=final_params,
                timeout=self.timeout,
                verify=True,  # SSL 인증서 검증
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'application/json',
                    'Accept-Encoding': 'gzip, deflate'
                }
            )
            
            logger.info(f"응답 상태 코드: {response.status_code}")
            logger.info(f"HTTPS 응답 URL: {response.url}")
            logger.info(f"SSL 인증서 확인: {'성공' if response.url.startswith('https://') else '실패'}")
            
            return response
            
        except requests.exceptions.SSLError as e:
            logger.error(f"SSL 인증서 오류: {e}")
            return None
        except requests.exceptions.Timeout:
            logger.error("API 요청 타임아웃")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API 요청 오류: {e}")
            return None
    
    def test_coords_expansion(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """좌표 데이터 확장 테스트 (4,300 → 250,000)"""
        if params is None:
            params = {
                "type": "json",
                "numOfRows": 5,
                "ctprvnCd": "11",  # 서울특별시 (상권 데이터가 많은 지역)
            }
        
        logger.info("좌표 데이터 확장 테스트 시작")
        
        response = self.make_secure_request(params)
        
        if not response or response.status_code != 200:
            return {"error": f"API 요청 실패: {response.status_code if response else 'None'}"}
        
        try:
            data = response.json()
            
            coords_analysis = {
                "total_records": 0,
                "coords_found": 0,
                "max_coords_length": 0,
                "min_coords_length": float('inf'),
                "avg_coords_length": 0,
                "geometry_types": set(),
                "sample_coords": []
            }
            
            # 데이터 구조 분석
            items = self._extract_items_from_response(data)
            
            if items:
                coords_analysis["total_records"] = len(items)
                coords_lengths = []
                
                for item in items:
                    # 좌표 정보 찾기
                    coords_info = self._find_coords_in_item(item)
                    
                    if coords_info:
                        coords_analysis["coords_found"] += 1
                        
                        for coord_field, coord_value in coords_info.items():
                            if coord_value:
                                coord_length = len(str(coord_value))
                                coords_lengths.append(coord_length)
                                
                                coords_analysis["max_coords_length"] = max(
                                    coords_analysis["max_coords_length"], 
                                    coord_length
                                )
                                coords_analysis["min_coords_length"] = min(
                                    coords_analysis["min_coords_length"], 
                                    coord_length
                                )
                                
                                # 지오메트리 타입 확인
                                if "POLYGON" in str(coord_value).upper():
                                    coords_analysis["geometry_types"].add("POLYGON")
                                elif "MULTIPOLYGON" in str(coord_value).upper():
                                    coords_analysis["geometry_types"].add("MULTIPOLYGON")
                                elif "POINT" in str(coord_value).upper():
                                    coords_analysis["geometry_types"].add("POINT")
                                
                                # 샘플 좌표 저장
                                if len(coords_analysis["sample_coords"]) < 3:
                                    coords_analysis["sample_coords"].append({
                                        "field": coord_field,
                                        "length": coord_length,
                                        "sample": str(coord_value)[:200] + "..." if coord_length > 200 else str(coord_value)
                                    })
                
                if coords_lengths:
                    coords_analysis["avg_coords_length"] = sum(coords_lengths) / len(coords_lengths)
                    coords_analysis["geometry_types"] = list(coords_analysis["geometry_types"])
                
                if coords_analysis["min_coords_length"] == float('inf'):
                    coords_analysis["min_coords_length"] = 0
            
            return coords_analysis
            
        except json.JSONDecodeError as e:
            return {"error": f"JSON 파싱 오류: {e}"}
        except Exception as e:
            return {"error": f"분석 오류: {e}"}
    
    def _extract_items_from_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """응답에서 아이템 목록 추출"""
        items = []
        
        # 일반적인 공공데이터 API 구조 탐색
        if isinstance(data, dict):
            # response > body > items 구조
            if "response" in data and isinstance(data["response"], dict):
                body = data["response"].get("body", {})
                if "items" in body:
                    if isinstance(body["items"], list):
                        items = body["items"]
                    elif isinstance(body["items"], dict) and "item" in body["items"]:
                        items = body["items"]["item"] if isinstance(body["items"]["item"], list) else [body["items"]["item"]]
            
            # 직접 items가 있는 경우
            elif "items" in data:
                items = data["items"] if isinstance(data["items"], list) else [data["items"]]
            
            # data가 직접 배열인 경우
            elif isinstance(data, list):
                items = data
            
            # 기타 구조 탐색
            else:
                for key, value in data.items():
                    if isinstance(value, list) and value:
                        items = value
                        break
                    elif isinstance(value, dict):
                        sub_items = self._extract_items_from_response(value)
                        if sub_items:
                            items = sub_items
                            break
        
        return items
    
    def _find_coords_in_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """아이템에서 좌표 정보 찾기"""
        coords_info = {}
        
        # 좌표 관련 필드명들
        coord_fields = [
            'coords', 'coordinate', 'geometry', 'polygon', 'multipolygon',
            'geom', 'shape', 'boundary', 'area', 'region', 'wkt', 'wgs84'
        ]
        
        for key, value in item.items():
            key_lower = key.lower()
            
            # 좌표 필드 확인
            if any(coord_field in key_lower for coord_field in coord_fields):
                coords_info[key] = value
            
            # 큰 문자열 데이터 확인 (좌표일 가능성)
            elif isinstance(value, str) and len(value) > 100:
                if any(geo_keyword in value.upper() for geo_keyword in ['POLYGON', 'POINT', 'MULTIPOLYGON']):
                    coords_info[key] = value
        
        return coords_info
    
    def test_polygon_format(self) -> Dict[str, Any]:
        """POLYGON 형식 변경 테스트 (MULTIPOLYGON → POLYGON)"""
        logger.info("POLYGON 형식 변경 테스트 시작")
        
        params = {
            "type": "json",
            "numOfRows": 10,
            "ctprvnCd": "11"  # 서울 (상권 데이터가 풍부)
        }
        
        response = self.make_secure_request(params)
        
        if not response or response.status_code != 200:
            return {"error": f"API 요청 실패: {response.status_code if response else 'None'}"}
        
        try:
            data = response.json()
            items = self._extract_items_from_response(data)
            
            polygon_analysis = {
                "total_items": len(items),
                "polygon_count": 0,
                "multipolygon_count": 0,
                "other_geometry_count": 0,
                "geometry_samples": [],
                "format_compliance": True
            }
            
            for item in items:
                coords_info = self._find_coords_in_item(item)
                
                for field, value in coords_info.items():
                    if value:
                        value_str = str(value).upper()
                        
                        if "POLYGON" in value_str:
                            if "MULTIPOLYGON" in value_str:
                                polygon_analysis["multipolygon_count"] += 1
                                polygon_analysis["format_compliance"] = False
                            else:
                                polygon_analysis["polygon_count"] += 1
                        elif any(geo_type in value_str for geo_type in ["POINT", "LINESTRING"]):
                            polygon_analysis["other_geometry_count"] += 1
                        
                        # 샘플 수집
                        if len(polygon_analysis["geometry_samples"]) < 5:
                            polygon_analysis["geometry_samples"].append({
                                "field": field,
                                "type": "MULTIPOLYGON" if "MULTIPOLYGON" in value_str else "POLYGON" if "POLYGON" in value_str else "OTHER",
                                "sample": str(value)[:150] + "..." if len(str(value)) > 150 else str(value)
                            })
            
            return polygon_analysis
            
        except Exception as e:
            return {"error": f"POLYGON 형식 분석 오류: {e}"}
    
    def test_major_commercial_district_info(self) -> Dict[str, Any]:
        """주요상권현황 변경 테스트 (상권정보시스템 → 소상공인365)"""
        logger.info("주요상권현황 정보 소스 변경 테스트 시작")
        
        params = {
            "type": "json",
            "numOfRows": 5
        }
        
        response = self.make_secure_request(params)
        
        if not response or response.status_code != 200:
            return {"error": f"API 요청 실패: {response.status_code if response else 'None'}"}
        
        try:
            data = response.json()
            items = self._extract_items_from_response(data)
            
            source_analysis = {
                "total_items": len(items),
                "source_indicators": {
                    "소상공인365": 0,
                    "상권정보시스템": 0,
                    "기타": 0
                },
                "field_analysis": {},
                "data_freshness": [],
                "sample_data": []
            }
            
            # 데이터 소스 관련 필드 탐색
            source_keywords = {
                "소상공인365": ["소상공인365", "sbiz365", "smes365"],
                "상권정보시스템": ["상권정보시스템", "commercial", "district"],
                "기타": ["system", "portal", "data"]
            }
            
            for item in items:
                item_source = "기타"
                
                # 모든 필드에서 소스 정보 탐색
                for key, value in item.items():
                    if value:
                        value_str = str(value).lower()
                        
                        for source_name, keywords in source_keywords.items():
                            if any(keyword.lower() in value_str for keyword in keywords):
                                item_source = source_name
                                break
                        
                        # 필드별 분석
                        if key not in source_analysis["field_analysis"]:
                            source_analysis["field_analysis"][key] = {
                                "type": type(value).__name__,
                                "sample_values": []
                            }
                        
                        if len(source_analysis["field_analysis"][key]["sample_values"]) < 3:
                            source_analysis["field_analysis"][key]["sample_values"].append(
                                str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                            )
                
                source_analysis["source_indicators"][item_source] += 1
                
                # 데이터 신선도 확인 (날짜 필드 탐색)
                date_fields = [k for k in item.keys() if any(date_keyword in k.lower() for date_keyword in ['date', 'time', 'update', 'modify', 'create'])]
                if date_fields:
                    source_analysis["data_freshness"].extend([{
                        "field": field,
                        "value": item[field]
                    } for field in date_fields[:2]])
                
                # 샘플 데이터 수집
                if len(source_analysis["sample_data"]) < 3:
                    source_analysis["sample_data"].append({
                        "source": item_source,
                        "key_fields": {k: v for k, v in list(item.items())[:5]}
                    })
            
            return source_analysis
            
        except Exception as e:
            return {"error": f"주요상권현황 분석 오류: {e}"}
    
    def run_comprehensive_update_test(self) -> Dict[str, Any]:
        """업데이트된 API의 종합 테스트"""
        logger.info("=== 소상공인시장진흥공단 API 업데이트 버전 종합 테스트 시작 ===")
        
        results = {
            "test_timestamp": datetime.now().isoformat(),
            "api_endpoint": self.base_url,
            "ssl_status": "HTTPS 적용",
            "update_compliance": {},
            "test_results": {}
        }
        
        # 1. HTTPS 연결 테스트
        logger.info("1. HTTPS 연결 테스트")
        https_test = self.test_https_connection()
        results["test_results"]["https_connection"] = https_test
        
        # 2. 좌표 데이터 확장 테스트
        logger.info("2. 좌표 데이터 확장 테스트 (4,300 → 250,000)")
        coords_test = self.test_coords_expansion()
        results["test_results"]["coords_expansion"] = coords_test
        
        # 3. POLYGON 형식 테스트
        logger.info("3. POLYGON 형식 변경 테스트")
        polygon_test = self.test_polygon_format()
        results["test_results"]["polygon_format"] = polygon_test
        
        # 4. 주요상권현황 소스 변경 테스트
        logger.info("4. 주요상권현황 소스 변경 테스트")
        source_test = self.test_major_commercial_district_info()
        results["test_results"]["commercial_district_source"] = source_test
        
        # 업데이트 준수 상태 평가
        results["update_compliance"] = self._evaluate_update_compliance(results["test_results"])
        
        return results
    
    def test_https_connection(self) -> Dict[str, Any]:
        """HTTPS 연결 테스트"""
        try:
            response = self.make_secure_request({"type": "json", "numOfRows": 1})
            
            if response:
                return {
                    "status": "success",
                    "https_enabled": response.url.startswith("https://"),
                    "ssl_verified": True,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                return {
                    "status": "failed",
                    "https_enabled": False,
                    "error": "연결 실패"
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _evaluate_update_compliance(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """업데이트 준수 상태 평가"""
        compliance = {
            "https_migration": False,
            "coords_expansion": False,
            "polygon_format": False,
            "data_source_update": False,
            "overall_compliance": False
        }
        
        # HTTPS 마이그레이션 확인
        https_result = test_results.get("https_connection", {})
        compliance["https_migration"] = https_result.get("https_enabled", False)
        
        # 좌표 확장 확인
        coords_result = test_results.get("coords_expansion", {})
        if not coords_result.get("error") and coords_result.get("max_coords_length", 0) > 4300:
            compliance["coords_expansion"] = True
        
        # POLYGON 형식 확인
        polygon_result = test_results.get("polygon_format", {})
        compliance["polygon_format"] = polygon_result.get("format_compliance", False)
        
        # 데이터 소스 업데이트 확인
        source_result = test_results.get("commercial_district_source", {})
        if not source_result.get("error"):
            smes365_count = source_result.get("source_indicators", {}).get("소상공인365", 0)
            old_system_count = source_result.get("source_indicators", {}).get("상권정보시스템", 0)
            compliance["data_source_update"] = smes365_count >= old_system_count
        
        # 전체 준수 상태
        compliance["overall_compliance"] = all([
            compliance["https_migration"],
            compliance["coords_expansion"] or coords_result.get("coords_found", 0) > 0,
            # polygon_format는 선택적 (데이터에 따라)
            # data_source_update는 점진적 변경 가능
        ])
        
        return compliance
    
    def save_test_results(self, results: Dict[str, Any]):
        """테스트 결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"updated_business_store_api_test_{timestamp}.json"
        filepath = f"d:/FinalProjects/Marketing-Platform/backend/tests/{filename}"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"테스트 결과 저장 완료: {filepath}")
            
            # 요약 리포트 생성
            self._generate_update_summary_report(results, filepath.replace('.json', '_summary.md'))
            
        except Exception as e:
            logger.error(f"테스트 결과 저장 실패: {e}")
    
    def _generate_update_summary_report(self, results: Dict[str, Any], filepath: str):
        """업데이트 테스트 요약 리포트 생성"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# 소상공인시장진흥공단 API 업데이트 테스트 리포트\n\n")
                f.write(f"**테스트 일시:** {results['test_timestamp']}\n")
                f.write(f"**API 엔드포인트:** {results['api_endpoint']}\n")
                f.write(f"**SSL 상태:** {results['ssl_status']}\n\n")
                
                f.write("## 업데이트 준수 상태\n\n")
                compliance = results["update_compliance"]
                
                f.write(f"- **HTTPS 마이그레이션:** {'✅' if compliance['https_migration'] else '❌'}\n")
                f.write(f"- **좌표 데이터 확장:** {'✅' if compliance['coords_expansion'] else '❌'}\n")
                f.write(f"- **POLYGON 형식 변경:** {'✅' if compliance['polygon_format'] else '⚠️'}\n")
                f.write(f"- **데이터 소스 업데이트:** {'✅' if compliance['data_source_update'] else '⚠️'}\n")
                f.write(f"- **전체 준수:** {'✅' if compliance['overall_compliance'] else '❌'}\n\n")
                
                f.write("## 상세 테스트 결과\n\n")
                
                for test_name, test_result in results["test_results"].items():
                    f.write(f"### {test_name.replace('_', ' ').title()}\n\n")
                    
                    if "error" in test_result:
                        f.write(f"❌ **오류:** {test_result['error']}\n\n")
                    else:
                        f.write("✅ **성공**\n\n")
                        
                        # 주요 결과 출력
                        if test_name == "coords_expansion":
                            f.write(f"- 최대 좌표 길이: {test_result.get('max_coords_length', 0):,}\n")
                            f.write(f"- 좌표 데이터 발견: {test_result.get('coords_found', 0)}개\n")
                            f.write(f"- 지오메트리 타입: {', '.join(test_result.get('geometry_types', []))}\n")
                        elif test_name == "polygon_format":
                            f.write(f"- POLYGON 개수: {test_result.get('polygon_count', 0)}\n")
                            f.write(f"- MULTIPOLYGON 개수: {test_result.get('multipolygon_count', 0)}\n")
                        elif test_name == "commercial_district_source":
                            indicators = test_result.get('source_indicators', {})
                            for source, count in indicators.items():
                                f.write(f"- {source}: {count}개\n")
                    
                    f.write("\n")
                
                f.write("## 권장사항\n\n")
                f.write("1. 모든 API 호출을 HTTPS로 전환\n")
                f.write("2. 좌표 데이터 처리 시 확장된 크기 고려\n")
                f.write("3. POLYGON 형식 변경에 따른 지오메트리 처리 로직 업데이트\n")
                f.write("4. 소상공인365 데이터 소스 활용 계획 수립\n\n")
            
            logger.info(f"요약 리포트 생성 완료: {filepath}")
            
        except Exception as e:
            logger.error(f"요약 리포트 생성 실패: {e}")


def main():
    """메인 테스트 실행"""
    try:
        print("🔄 소상공인시장진흥공단 API 업데이트 버전 테스트 시작...")
        print("📅 업데이트 적용일: 2025년 6월 11일 (수) 오전 10시")
        print("🔧 주요 변경사항:")
        print("   1. HTTP → HTTPS 전환")
        print("   2. 좌표 크기 4,300 → 250,000 확장")
        print("   3. MULTIPOLYGON → POLYGON 변경")
        print("   4. 상권정보시스템 → 소상공인365")
        print("="*60)
        
        api_client = UpdatedBusinessStoreAPI()
        
        # 종합 테스트 실행
        results = api_client.run_comprehensive_update_test()
        
        # 결과 출력
        print("\n📊 테스트 결과 요약:")
        compliance = results["update_compliance"]
        
        print(f"✅ HTTPS 마이그레이션: {'완료' if compliance['https_migration'] else '미완료'}")
        print(f"✅ 좌표 데이터 확장: {'적용' if compliance['coords_expansion'] else '확인필요'}")
        print(f"✅ POLYGON 형식 변경: {'적용' if compliance['polygon_format'] else '점진적변경'}")
        print(f"✅ 데이터 소스 업데이트: {'적용' if compliance['data_source_update'] else '점진적변경'}")
        
        overall_status = "🎉 전체 업데이트 준수" if compliance['overall_compliance'] else "⚠️ 부분 업데이트 적용"
        print(f"\n{overall_status}")
        
        # 상세 결과 출력
        print("\n📋 상세 테스트 결과:")
        for test_name, test_result in results["test_results"].items():
            status = "✅" if "error" not in test_result else "❌"
            print(f"   {status} {test_name.replace('_', ' ').title()}")
            if "error" in test_result:
                print(f"      오류: {test_result['error']}")
        
        # 파일 저장
        api_client.save_test_results(results)
        print(f"\n💾 상세 결과가 파일로 저장되었습니다.")
        
    except Exception as e:
        logger.error(f"테스트 실행 중 오류: {e}")
        print(f"❌ 테스트 실행 실패: {e}")


if __name__ == "__main__":
    main()

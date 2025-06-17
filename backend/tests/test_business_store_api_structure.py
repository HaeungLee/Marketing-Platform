"""
소상공인시장진흥공단_상가(상권)정보_API 데이터 구조 분석
API 엔드포인트: https://apis.data.go.kr/B553077/api/open/sdsc2
실제 API 호출을 통한 데이터 형식 및 구조 확인
"""

import requests
import json
import xml.etree.ElementTree as ET
import pandas as pd
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BusinessStoreAPIStructureAnalyzer:
    """소상공인시장진흥공단 상가(상권)정보 API 구조 분석기"""
    
    def __init__(self):
        self.base_url = "https://apis.data.go.kr/B553077/api/open/sdsc2"
        self.api_key_encoded = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb%2FcuUI4dZSKEukcnq1me2b99jyFg%3D%3D"
        self.api_key_decoded = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg=="
        self.timeout = 30
        
    def make_api_request(self, params: Dict[str, Any], data_format: str = "json") -> Optional[requests.Response]:
        """API 요청 실행"""
        try:
            # 기본 파라미터 설정
            default_params = {
                "serviceKey": self.api_key_encoded,  # 먼저 인코딩된 키로 시도
                "type": data_format,
                "numOfRows": 10,  # 테스트용으로 작은 수
                "pageNo": 1
            }
            
            # 파라미터 병합
            final_params = {**default_params, **params}
            
            logger.info(f"API 요청 시작 - URL: {self.base_url}")
            logger.info(f"파라미터: {final_params}")
            
            response = requests.get(
                self.base_url,
                params=final_params,
                timeout=self.timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            logger.info(f"응답 상태 코드: {response.status_code}")
            logger.info(f"응답 URL: {response.url}")
            
            return response
            
        except requests.exceptions.Timeout:
            logger.error("API 요청 타임아웃")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API 요청 오류: {e}")
            return None
    
    def try_with_different_keys(self, params: Dict[str, Any], data_format: str = "json") -> Optional[requests.Response]:
        """인코딩된 키와 디코딩된 키 모두 시도"""
        # 먼저 인코딩된 키로 시도
        params_encoded = params.copy()
        params_encoded["serviceKey"] = self.api_key_encoded
        
        response = self.make_api_request(params_encoded, data_format)
        
        if response and response.status_code == 200:
            return response
            
        logger.info("인코딩된 키 실패, 디코딩된 키로 재시도")
        
        # 디코딩된 키로 시도
        params_decoded = params.copy()
        params_decoded["serviceKey"] = self.api_key_decoded
        
        return self.make_api_request(params_decoded, data_format)
    
    def analyze_json_response(self, response: requests.Response) -> Dict[str, Any]:
        """JSON 응답 분석"""
        try:
            data = response.json()
            
            analysis = {
                "format": "JSON",
                "status_code": response.status_code,
                "response_size": len(response.content),
                "content_type": response.headers.get('content-type', 'unknown'),
                "data_structure": self._analyze_json_structure(data),
                "sample_data": data,
                "field_analysis": self._analyze_fields(data)
            }
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 오류: {e}")
            return {
                "format": "JSON",
                "error": f"JSON 파싱 실패: {e}",
                "raw_content": response.text[:1000]  # 처음 1000자만
            }
    
    def analyze_xml_response(self, response: requests.Response) -> Dict[str, Any]:
        """XML 응답 분석"""
        try:
            root = ET.fromstring(response.content)
            
            analysis = {
                "format": "XML",
                "status_code": response.status_code,
                "response_size": len(response.content),
                "content_type": response.headers.get('content-type', 'unknown'),
                "root_tag": root.tag,
                "xml_structure": self._analyze_xml_structure(root),
                "sample_data": response.text,
                "field_analysis": self._analyze_xml_fields(root)
            }
            
            return analysis
            
        except ET.ParseError as e:
            logger.error(f"XML 파싱 오류: {e}")
            return {
                "format": "XML",
                "error": f"XML 파싱 실패: {e}",
                "raw_content": response.text[:1000]
            }
    
    def _analyze_json_structure(self, data: Any, depth: int = 0) -> Dict[str, Any]:
        """JSON 데이터 구조 재귀 분석"""
        if depth > 5:  # 무한 재귀 방지
            return {"type": "max_depth_reached"}
            
        if isinstance(data, dict):
            structure = {"type": "object", "keys": {}}
            for key, value in data.items():
                structure["keys"][key] = self._analyze_json_structure(value, depth + 1)
            return structure
        elif isinstance(data, list):
            if data:
                return {
                    "type": "array",
                    "length": len(data),
                    "item_structure": self._analyze_json_structure(data[0], depth + 1)
                }
            else:
                return {"type": "empty_array"}
        else:
            return {
                "type": type(data).__name__,
                "sample_value": str(data)[:100] if data is not None else None
            }
    
    def _analyze_xml_structure(self, element: ET.Element, depth: int = 0) -> Dict[str, Any]:
        """XML 구조 재귀 분석"""
        if depth > 5:
            return {"type": "max_depth_reached"}
            
        structure = {
            "tag": element.tag,
            "attributes": dict(element.attrib),
            "text": element.text.strip() if element.text else None,
            "children": {}
        }
        
        for child in element:
            child_tag = child.tag
            if child_tag not in structure["children"]:
                structure["children"][child_tag] = []
            structure["children"][child_tag].append(
                self._analyze_xml_structure(child, depth + 1)
            )
        
        return structure
    
    def _analyze_fields(self, data: Any, prefix: str = "") -> List[Dict[str, Any]]:
        """JSON 필드 분석"""
        fields = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                field_path = f"{prefix}.{key}" if prefix else key
                
                field_info = {
                    "field_path": field_path,
                    "data_type": type(value).__name__,
                    "sample_value": str(value)[:100] if value is not None else None,
                    "is_null": value is None
                }
                
                fields.append(field_info)
                
                # 중첩 구조 분석
                if isinstance(value, (dict, list)) and len(fields) < 100:  # 너무 많은 필드 방지
                    fields.extend(self._analyze_fields(value, field_path))
        
        elif isinstance(data, list) and data:
            # 배열의 첫 번째 항목 분석
            fields.extend(self._analyze_fields(data[0], f"{prefix}[0]"))
        
        return fields
    
    def _analyze_xml_fields(self, element: ET.Element, prefix: str = "") -> List[Dict[str, Any]]:
        """XML 필드 분석"""
        fields = []
        
        field_path = f"{prefix}.{element.tag}" if prefix else element.tag
        
        # 현재 요소 정보
        field_info = {
            "field_path": field_path,
            "data_type": "element",
            "text_content": element.text.strip() if element.text else None,
            "attributes": dict(element.attrib)
        }
        fields.append(field_info)
        
        # 자식 요소들 분석
        for child in element:
            if len(fields) < 100:  # 너무 많은 필드 방지
                fields.extend(self._analyze_xml_fields(child, field_path))
        
        return fields
    
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """종합적인 API 분석 실행"""
        logger.info("소상공인시장진흥공단 상가(상권)정보 API 분석 시작")
        
        results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "api_endpoint": self.base_url,
            "test_results": {}
        }
        
        # 다양한 파라미터 조합으로 테스트
        test_cases = [
            {
                "name": "기본_JSON_요청",
                "params": {"type": "json", "numOfRows": 5},
                "format": "json"
            },
            {
                "name": "기본_XML_요청", 
                "params": {"type": "xml", "numOfRows": 5},
                "format": "xml"
            },
            {
                "name": "지역_필터_JSON",
                "params": {"type": "json", "numOfRows": 5, "ctprvnCd": "11"},  # 서울
                "format": "json"
            },
            {
                "name": "업종_필터_JSON",
                "params": {"type": "json", "numOfRows": 5, "indtyLclsCd": "Q"},  # 보건업 및 사회복지서비스업
                "format": "json"
            }
        ]
        
        for test_case in test_cases:
            logger.info(f"테스트 케이스 실행: {test_case['name']}")
            
            # API 요청 (두 가지 키 모두 시도)
            response = self.try_with_different_keys(test_case["params"], test_case["format"])
            
            if response:
                if test_case["format"] == "json":
                    analysis = self.analyze_json_response(response)
                else:
                    analysis = self.analyze_xml_response(response)
                    
                results["test_results"][test_case["name"]] = analysis
            else:
                results["test_results"][test_case["name"]] = {
                    "error": "API 요청 실패",
                    "params": test_case["params"]
                }
            
            # API 호출 간격 (rate limiting 고려)
            time.sleep(1)
        
        return results
    
    def save_analysis_report(self, results: Dict[str, Any], filename: str = None):
        """분석 결과를 파일로 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_store_api_analysis_{timestamp}.json"
        
        filepath = f"d:/FinalProjects/Marketing-Platform/backend/tests/{filename}"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"분석 결과 저장 완료: {filepath}")
            
            # 요약 리포트도 생성
            self._generate_summary_report(results, filepath.replace('.json', '_summary.md'))
            
        except Exception as e:
            logger.error(f"분석 결과 저장 실패: {e}")
    
    def _generate_summary_report(self, results: Dict[str, Any], filepath: str):
        """요약 리포트 생성"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# 소상공인시장진흥공단 상가(상권)정보 API 분석 리포트\n\n")
                f.write(f"**분석 일시:** {results['analysis_timestamp']}\n")
                f.write(f"**API 엔드포인트:** {results['api_endpoint']}\n\n")
                
                f.write("## 테스트 결과 요약\n\n")
                
                for test_name, test_result in results["test_results"].items():
                    f.write(f"### {test_name}\n\n")
                    
                    if "error" in test_result:
                        f.write(f"❌ **오류:** {test_result['error']}\n\n")
                        continue
                    
                    f.write(f"✅ **상태:** 성공\n")
                    f.write(f"- **응답 형식:** {test_result.get('format', 'unknown')}\n")
                    f.write(f"- **상태 코드:** {test_result.get('status_code', 'unknown')}\n")
                    f.write(f"- **응답 크기:** {test_result.get('response_size', 'unknown')} bytes\n")
                    f.write(f"- **Content-Type:** {test_result.get('content_type', 'unknown')}\n\n")
                    
                    # 필드 분석 결과
                    if "field_analysis" in test_result:
                        f.write("**주요 필드:**\n")
                        for field in test_result["field_analysis"][:10]:  # 처음 10개만
                            f.write(f"- `{field['field_path']}`: {field['data_type']}\n")
                        f.write("\n")
                
                f.write("## 결론 및 권장사항\n\n")
                f.write("- API 연결 상태 및 데이터 구조 확인 완료\n")
                f.write("- 상세한 분석 결과는 JSON 파일 참조\n")
                f.write("- 실제 프로덕션 환경에서는 에러 처리 및 재시도 로직 구현 필요\n\n")
            
            logger.info(f"요약 리포트 생성 완료: {filepath}")
            
        except Exception as e:
            logger.error(f"요약 리포트 생성 실패: {e}")


def main():
    """메인 실행 함수"""
    try:
        analyzer = BusinessStoreAPIStructureAnalyzer()
        
        # 종합 분석 실행
        results = analyzer.run_comprehensive_analysis()
        
        # 결과 출력
        print("\n" + "="*80)
        print("소상공인시장진흥공단 상가(상권)정보 API 분석 결과")
        print("="*80)
        
        for test_name, test_result in results["test_results"].items():
            print(f"\n[{test_name}]")
            if "error" in test_result:
                print(f"❌ 오류: {test_result['error']}")
            else:
                print(f"✅ 성공 - 상태: {test_result.get('status_code')}, 형식: {test_result.get('format')}")
                print(f"   응답 크기: {test_result.get('response_size')} bytes")
                
                # 샘플 데이터 일부 출력
                if "sample_data" in test_result:
                    sample = test_result["sample_data"]
                    if isinstance(sample, dict):
                        print(f"   주요 키: {list(sample.keys())[:5]}")
                    elif isinstance(sample, str):
                        print(f"   XML 루트: {test_result.get('root_tag', 'unknown')}")
        
        # 파일로 저장
        analyzer.save_analysis_report(results)
        
        print(f"\n📄 상세 분석 결과가 파일로 저장되었습니다.")
        print("   - JSON 파일: 전체 분석 데이터")
        print("   - MD 파일: 요약 리포트")
        
    except Exception as e:
        logger.error(f"분석 실행 중 오류 발생: {e}")
        print(f"❌ 분석 실패: {e}")


if __name__ == "__main__":
    main()

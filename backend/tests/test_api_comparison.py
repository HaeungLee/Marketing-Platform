"""
공공데이터포털 행정동별 인구수 API와 현재 CSV 데이터 비교 테스트
"""
import requests
import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Any
import os
import sys
import urllib3
from urllib.parse import quote, unquote

# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 현재 디렉토리에서 backend 모듈을 import할 수 있도록 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class APIDataComparison:
    def __init__(self):
        # 공공데이터포털 API 설정
        self.api_endpoint = "https://apis.data.go.kr/1741000/admmSexdAgePpltn"
        self.api_key_encoding = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb%2FcuUI4dZSKEukcnq1me2b99jyFg%3D%3D"
        self.api_key_decoding = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg=="
        
        # CSV 파일 경로 (상대 경로로 수정)
        self.csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "totalpopulation", "population_with_total_columns.csv")
        
    def fetch_api_data(self, data_format="json", num_rows=10) -> Dict[str, Any]:
        """
        공공데이터포털 API에서 데이터를 가져옵니다
        """
        print(f"\n=== API 데이터 가져오기 ({data_format.upper()} 형식) ===")
        
        # SSL 인증서 검증 비활성화하여 다양한 방법으로 시도
        session = requests.Session()
        session.verify = False  # SSL 인증서 검증 비활성화
        
        # 1차 시도: Decoding 키
        params1 = {
            "serviceKey": self.api_key_decoding,
            "numOfRows": num_rows,
            "pageNo": 1,
            "type": data_format
        }
        
        # 2차 시도: Encoding 키
        params2 = {
            "serviceKey": self.api_key_encoding,
            "numOfRows": num_rows,
            "pageNo": 1,
            "type": data_format
        }
        
        attempts = [
            ("Decoding Key", params1),
            ("Encoding Key", params2)
        ]
        
        for attempt_name, params in attempts:
            try:
                print(f"\n🔄 {attempt_name}로 시도...")
                response = session.get(self.api_endpoint, params=params, timeout=30)
                print(f"API 호출 URL: {response.url}")
                print(f"응답 상태 코드: {response.status_code}")
                print(f"응답 헤더: {dict(response.headers)}")
                
                if response.status_code == 200:
                    print(f"✅ API 호출 성공!")
                    
                    # 응답 내용 확인
                    content = response.text
                    print(f"응답 내용 길이: {len(content)} 문자")
                    print(f"응답 내용 (처음 200자): {content[:200]}")
                    
                    if data_format == "json":
                        try:
                            result = response.json()
                            print("✅ JSON 파싱 성공")
                            return result
                        except json.JSONDecodeError as e:
                            print(f"❌ JSON 파싱 실패: {e}")
                            print(f"원본 응답: {content[:1000]}")
                            # XML로 파싱 시도
                            try:
                                root = ET.fromstring(content)
                                print("✅ XML로 파싱 성공")
                                return self.xml_to_dict(root)
                            except ET.ParseError:
                                return {"error": "JSON/XML 파싱 모두 실패", "raw_response": content}
                    else:  # xml
                        try:
                            root = ET.fromstring(content)
                            print("✅ XML 파싱 성공")
                            return self.xml_to_dict(root)
                        except ET.ParseError as e:
                            print(f"❌ XML 파싱 실패: {e}")
                            return {"error": "XML 파싱 실패", "raw_response": content}
                else:
                    print(f"❌ API 호출 실패: {response.status_code}")
                    print(f"응답 내용: {response.text[:1000]}")
                    
            except Exception as e:
                print(f"❌ {attempt_name} 시도 실패: {e}")
                continue
        
        # 모든 시도가 실패한 경우
        print("\n❌ 모든 API 호출 시도가 실패했습니다.")
        
        # 대안: 공공데이터포털 웹페이지에서 API 문서 확인 제안
        print("\n💡 문제 해결 제안:")
        print("1. 네트워크 연결 확인")
        print("2. API 키 유효성 확인")
        print("3. 공공데이터포털 사이트에서 API 상태 확인")
        print("4. 방화벽 설정 확인")
        
        return {"error": "모든 API 호출 시도 실패"}
    
    def xml_to_dict(self, element) -> Dict[str, Any]:
        """XML을 딕셔너리로 변환"""
        result = {}
        if element.text and element.text.strip():
            result['text'] = element.text.strip()
        
        for child in element:
            if len(list(child)) == 0:
                result[child.tag] = child.text
            else:
                if child.tag in result:
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(self.xml_to_dict(child))
                else:
                    result[child.tag] = self.xml_to_dict(child)
        return result
    
    def load_csv_data(self) -> pd.DataFrame:
        """현재 사용 중인 CSV 데이터를 로드합니다"""
        print("\n=== CSV 데이터 로드 ===")
        try:
            if os.path.exists(self.csv_path):
                df = pd.read_csv(self.csv_path, encoding='utf-8')
                print(f"CSV 파일 로드 성공: {len(df)}행, {len(df.columns)}열")
                return df
            else:
                print(f"CSV 파일을 찾을 수 없습니다: {self.csv_path}")
                return pd.DataFrame()
        except Exception as e:
            print(f"CSV 파일 로드 실패: {e}")
            try:
                # 다른 인코딩으로 시도
                df = pd.read_csv(self.csv_path, encoding='cp949')
                print(f"CSV 파일 로드 성공 (cp949 인코딩): {len(df)}행, {len(df.columns)}열")
                return df
            except Exception as e2:
                print(f"다른 인코딩으로도 실패: {e2}")
                return pd.DataFrame()
    
    def analyze_api_structure(self, api_data: Dict[str, Any]) -> None:
        """API 데이터 구조를 분석합니다"""
        print("\n=== API 데이터 구조 분석 ===")
        
        if "error" in api_data:
            print(f"❌ API 오류: {api_data['error']}")
            if "raw_response" in api_data:
                print(f"원본 응답 (처음 1000자):")
                print(api_data['raw_response'][:1000])
            return
        
        def print_structure(data, indent=0, max_depth=3):
            if indent > max_depth:
                return
            
            prefix = "  " * indent
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        print(f"{prefix}{key}: {type(value).__name__}")
                        if isinstance(value, list) and len(value) > 0:
                            print(f"{prefix}  └─ 배열 크기: {len(value)}")
                            if len(value) > 0:
                                print(f"{prefix}  └─ 첫 번째 요소 타입: {type(value[0]).__name__}")
                                if isinstance(value[0], dict):
                                    print_structure(value[0], indent + 2, max_depth)
                        elif isinstance(value, dict):
                            print_structure(value, indent + 1, max_depth)
                    else:
                        value_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                        print(f"{prefix}{key}: {value_str}")
            elif isinstance(data, list):
                print(f"{prefix}배열 크기: {len(data)}")
                if len(data) > 0:
                    print(f"{prefix}첫 번째 요소 타입: {type(data[0]).__name__}")
                    print_structure(data[0], indent + 1, max_depth)
        
        print_structure(api_data)
    
    def analyze_csv_structure(self, df: pd.DataFrame) -> None:
        """CSV 데이터 구조를 분석합니다"""
        print("\n=== CSV 데이터 구조 분석 ===")
        
        if df.empty:
            print("❌ CSV 데이터가 비어있습니다.")
            return
        
        print(f"📊 데이터 형태: {df.shape[0]}행 {df.shape[1]}열")
        print(f"\n📋 컬럼 목록 ({len(df.columns)}개):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print(f"\n📄 샘플 데이터 (처음 3행):")
        print(df.head(3).to_string(max_cols=10))
        
        print(f"\n🔍 결측값 확인:")
        null_counts = df.isnull().sum()
        has_nulls = False
        for col in df.columns:
            if null_counts[col] > 0:
                print(f"  {col}: {null_counts[col]}개")
                has_nulls = True
        
        if not has_nulls:
            print("  ✅ 결측값 없음")
    
    def extract_api_dataframe(self, api_data: Dict[str, Any]) -> pd.DataFrame:
        """API 데이터에서 실제 데이터 부분을 DataFrame으로 변환"""
        print("\n=== API 데이터를 DataFrame으로 변환 ===")
        
        if "error" in api_data:
            print("❌ API 오류로 인해 DataFrame 변환 불가")
            return pd.DataFrame()
        
        # 다양한 구조의 API 응답에서 실제 데이터 찾기
        data_items = []
        
        def find_data_items(obj, path=""):
            nonlocal data_items
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    # 일반적인 데이터 키들 확인
                    if key.lower() in ['items', 'item', 'data', 'list', 'result', 'body', 'response']:
                        if isinstance(value, list):
                            data_items.extend(value)
                            print(f"✅ 데이터 발견: {new_path} (배열 크기: {len(value)})")
                        elif isinstance(value, dict):
                            find_data_items(value, new_path)
                    else:
                        find_data_items(value, new_path)
            elif isinstance(obj, list) and obj:
                # 루트가 배열인 경우
                if isinstance(obj[0], dict):
                    data_items.extend(obj)
                    print(f"✅ 루트 배열 데이터 발견: {path} (배열 크기: {len(obj)})")
        
        find_data_items(api_data)
        
        if data_items:
            df = pd.DataFrame(data_items)
            print(f"✅ DataFrame 생성 성공: {df.shape}")
            if not df.empty:
                print(f"컬럼: {list(df.columns)}")
            return df
        else:
            print("❌ API 응답에서 데이터를 찾을 수 없습니다.")
            print("전체 응답 구조:")
            print(json.dumps(api_data, indent=2, ensure_ascii=False)[:500])
            return pd.DataFrame()
    
    def compare_datasets(self, api_df: pd.DataFrame, csv_df: pd.DataFrame) -> None:
        """두 데이터셋을 비교합니다"""
        print("\n" + "="*70)
        print("🔍 데이터셋 비교 결과")
        print("="*70)
        
        if api_df.empty and csv_df.empty:
            print("❌ 두 데이터셋 모두 비어있어 비교할 수 없습니다.")
            return
        elif api_df.empty:
            print("❌ API 데이터가 비어있어 비교할 수 없습니다.")
            print(f"📊 CSV 데이터만 있음: {csv_df.shape}")
            return
        elif csv_df.empty:
            print("❌ CSV 데이터가 비어있어 비교할 수 없습니다.")
            print(f"📊 API 데이터만 있음: {api_df.shape}")
            return
        
        print(f"\n📊 데이터 크기 비교:")
        print(f"  🔵 API 데이터: {api_df.shape[0]}행 {api_df.shape[1]}열")
        print(f"  🔴 CSV 데이터: {csv_df.shape[0]}행 {csv_df.shape[1]}열")
        
        print(f"\n📋 컬럼 비교:")
        api_cols = set(api_df.columns)
        csv_cols = set(csv_df.columns)
        
        print(f"  🔵 API 컬럼 수: {len(api_cols)}")
        print(f"  🔴 CSV 컬럼 수: {len(csv_cols)}")
        
        common_cols = api_cols & csv_cols
        api_only_cols = api_cols - csv_cols
        csv_only_cols = csv_cols - api_cols
        
        if common_cols:
            print(f"\n✅ 공통 컬럼 ({len(common_cols)}개):")
            for col in sorted(common_cols):
                print(f"    - {col}")
        
        if api_only_cols:
            print(f"\n🔵 API에만 있는 컬럼 ({len(api_only_cols)}개):")
            for col in sorted(api_only_cols):
                print(f"    - {col}")
        
        if csv_only_cols:
            print(f"\n🔴 CSV에만 있는 컬럼 ({len(csv_only_cols)}개):")
            for col in sorted(csv_only_cols):
                print(f"    - {col}")
        
        # 유사한 컬럼명 찾기
        print(f"\n🔍 유사한 컬럼명 분석:")
        self.find_similar_columns(api_cols, csv_cols)
        
        # 샘플 데이터 비교
        if not api_df.empty:
            print(f"\n📋 API 샘플 데이터 (상위 2행):")
            print(api_df.head(2).to_string(max_cols=10))
        
        if not csv_df.empty:
            print(f"\n📋 CSV 샘플 데이터 (상위 2행):")
            print(csv_df.head(2).to_string(max_cols=10))
    
    def find_similar_columns(self, api_cols: set, csv_cols: set) -> None:
        """유사한 컬럼명을 찾습니다"""
        similarities = []
        
        for api_col in api_cols:
            for csv_col in csv_cols:
                api_lower = api_col.lower().replace(' ', '').replace('_', '')
                csv_lower = csv_col.lower().replace(' ', '').replace('_', '')
                
                # 정확히 일치
                if api_lower == csv_lower:
                    similarities.append((api_col, csv_col, "정확일치"))
                # 부분 문자열 포함
                elif api_lower in csv_lower or csv_lower in api_lower:
                    similarities.append((api_col, csv_col, "부분일치"))
                # 키워드 일치 확인
                else:
                    api_words = set(api_lower.split())
                    csv_words = set(csv_lower.split())
                    if api_words & csv_words:  # 교집합이 있으면
                        similarities.append((api_col, csv_col, "키워드일치"))
        
        if similarities:
            print("  ✅ 유사한 컬럼 쌍 발견:")
            for api_col, csv_col, match_type in similarities:
                print(f"    🔗 {api_col} ↔ {csv_col} ({match_type})")
        else:
            print("  ❌ 유사한 컬럼명을 찾지 못했습니다.")
    
    def assess_compatibility(self, api_df: pd.DataFrame, csv_df: pd.DataFrame) -> None:
        """API 데이터와 CSV 데이터의 호환성을 평가합니다"""
        print("\n" + "="*70)
        print("🎯 호환성 평가 및 변환 가능성")
        print("="*70)
        
        if api_df.empty or csv_df.empty:
            print("❌ 데이터가 부족해 호환성 평가를 할 수 없습니다.")
            return
        
        # 컬럼 유사도 계산
        api_cols = set(api_df.columns)
        csv_cols = set(csv_df.columns)
        common_cols = api_cols & csv_cols
        
        column_similarity = len(common_cols) / max(len(csv_cols), 1) * 100
        
        print(f"📊 컬럼 유사도: {column_similarity:.1f}%")
        print(f"   - 공통 컬럼: {len(common_cols)}개")
        print(f"   - CSV 총 컬럼: {len(csv_cols)}개")
        
        # 데이터 규모 비교
        size_ratio = min(len(api_df), len(csv_df)) / max(len(api_df), len(csv_df)) * 100
        print(f"📏 데이터 규모 유사도: {size_ratio:.1f}%")
        
        # 종합 호환성 점수
        compatibility_score = (column_similarity * 0.7 + size_ratio * 0.3)
        
        print(f"\n🏆 종합 호환성 점수: {compatibility_score:.1f}%")
        
        if compatibility_score > 70:
            print("✅ 높은 호환성: API 데이터를 CSV 형태로 쉽게 변환할 수 있습니다!")
            print("   🎉 발표에서 API 사용을 주장할 수 있는 좋은 상황입니다.")
        elif compatibility_score > 40:
            print("⚠️ 중간 호환성: 일부 전처리 후 변환 가능합니다.")
            print("   💡 적절한 매핑 로직으로 API 데이터 활용이 가능합니다.")
        else:
            print("❌ 낮은 호환성: 상당한 구조 변경이 필요합니다.")
            print("   🔄 프론트엔드 인구통계 부분을 API 데이터에 맞게 수정해야 합니다.")
        
        # 구체적인 변환 제안
        print(f"\n💡 변환 제안:")
        if common_cols:
            print(f"1. ✅ 공통 컬럼 활용: {', '.join(sorted(common_cols))}")
        
        print("2. 🔄 필요한 변환 작업:")
        print("   - 행정구역 코드/명 매핑")
        print("   - 연령대별 데이터 구조 정리")
        print("   - 성별 데이터 통합")
        print("   - 결측값 처리")

def main():
    """메인 실행 함수"""
    print("="*80)
    print("🔍 공공데이터포털 API vs 현재 CSV 데이터 비교 분석")
    print("="*80)
    
    comparator = APIDataComparison()
    
    # 1. CSV 데이터 먼저 로드
    csv_data = comparator.load_csv_data()
    comparator.analyze_csv_structure(csv_data)
    
    # 2. API 데이터 가져오기 (JSON 우선)
    api_data_json = comparator.fetch_api_data("json", 20)
    comparator.analyze_api_structure(api_data_json)
    
    # 3. API 데이터를 DataFrame으로 변환
    api_df = comparator.extract_api_dataframe(api_data_json)
    
    # JSON이 실패하면 XML도 시도
    if api_df.empty:
        print("\n⚠️ JSON 형식이 실패하여 XML 형식으로 재시도...")
        api_data_xml = comparator.fetch_api_data("xml", 20)
        comparator.analyze_api_structure(api_data_xml)
        api_df = comparator.extract_api_dataframe(api_data_xml)
    
    # 4. 데이터셋 비교
    comparator.compare_datasets(api_df, csv_data)
    
    # 5. 호환성 평가 및 제안
    comparator.assess_compatibility(api_df, csv_data)
    
    print("\n" + "="*80)
    print("✅ 분석 완료! 위 결과를 바탕으로 API 활용 전략을 수립하세요.")
    print("="*80)

if __name__ == "__main__":
    main() 
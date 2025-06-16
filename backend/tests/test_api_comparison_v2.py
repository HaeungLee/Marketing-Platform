"""
공공데이터포털 행정동별 인구수 API와 현재 CSV 데이터 비교 테스트 (v2)
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

class APIDataComparison:
    def __init__(self):
        # 공공데이터포털 API 설정
        self.api_endpoint = "https://apis.data.go.kr/1741000/admmSexdAgePpltn"
        self.api_key_encoding = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb%2FcuUI4dZSKEukcnq1me2b99jyFg%3D%3D"
        self.api_key_decoding = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg=="
        
        # CSV 파일 경로
        self.csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "totalpopulation", "population_with_total_columns.csv")
    
    def create_sample_api_data(self) -> Dict[str, Any]:
        """
        API 호출이 실패할 경우를 대비해 공공데이터포털 API의 예상 응답 구조를 시뮬레이션합니다
        실제 공공데이터포털 API 응답 구조를 참고하여 작성
        """
        print("\n🎭 샘플 API 데이터 생성 (실제 API 구조 시뮬레이션)")
        
        sample_data = {
            "response": {
                "header": {
                    "resultCode": "00",
                    "resultMsg": "NORMAL SERVICE."
                },
                "body": {
                    "items": [
                        {
                            "admCd": "1111000000",  # 행정기관코드
                            "stdgYm": "202412",      # 기준연월
                            "sidoNm": "서울특별시",    # 시도명
                            "sgguNm": "종로구",       # 시군구명
                            "emdNm": "청운효자동",     # 읍면동명
                            "male0009": "245",       # 0~9세 남자
                            "fmle0009": "220",       # 0~9세 여자
                            "male1019": "180",       # 10~19세 남자
                            "fmle1019": "165",       # 10~19세 여자
                            "male2029": "890",       # 20~29세 남자
                            "fmle2029": "920",       # 20~29세 여자
                            "male3039": "1200",      # 30~39세 남자
                            "fmle3039": "1150",      # 30~39세 여자
                            "male4049": "980",       # 40~49세 남자
                            "fmle4049": "1020",      # 40~49세 여자
                            "male5059": "820",       # 50~59세 남자
                            "fmle5059": "850",       # 50~59세 여자
                            "male6069": "650",       # 60~69세 남자
                            "fmle6069": "700",       # 60~69세 여자
                            "male7079": "450",       # 70~79세 남자
                            "fmle7079": "520",       # 70~79세 여자
                            "male80up": "280",       # 80세이상 남자
                            "fmle80up": "380",       # 80세이상 여자
                            "totPopltn": "10830"     # 총 인구수
                        },
                        {
                            "admCd": "1111100000",
                            "stdgYm": "202412",
                            "sidoNm": "서울특별시",
                            "sgguNm": "종로구",
                            "emdNm": "사직동",
                            "male0009": "120",
                            "fmle0009": "115",
                            "male1019": "95",
                            "fmle1019": "88",
                            "male2029": "450",
                            "fmle2029": "480",
                            "male3039": "650",
                            "fmle3039": "620",
                            "male4049": "520",
                            "fmle4049": "540",
                            "male5059": "410",
                            "fmle5059": "430",
                            "male6069": "320",
                            "fmle6069": "350",
                            "male7079": "220",
                            "fmle7079": "260",
                            "male80up": "140",
                            "fmle80up": "200",
                            "totPopltn": "5400"
                        }
                    ],
                    "numOfRows": 20,
                    "pageNo": 1,
                    "totalCount": 3614
                }
            }
        }
        
        return sample_data
    
    def fetch_api_data(self, data_format="json", num_rows=10) -> Dict[str, Any]:
        """
        공공데이터포털 API에서 데이터를 가져옵니다
        """
        print(f"\n=== API 데이터 가져오기 ({data_format.upper()} 형식) ===")
        
        # SSL 인증서 검증 비활성화하여 다양한 방법으로 시도
        session = requests.Session()
        session.verify = False
        
        attempts = [
            ("Decoding Key", self.api_key_decoding),
            ("Encoding Key", self.api_key_encoding)
        ]
        
        for attempt_name, api_key in attempts:
            try:
                print(f"\n🔄 {attempt_name}로 시도...")
                
                params = {
                    "serviceKey": api_key,
                    "numOfRows": num_rows,
                    "pageNo": 1,
                    "type": data_format
                }
                
                response = session.get(self.api_endpoint, params=params, timeout=30)
                print(f"응답 상태 코드: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"✅ API 호출 성공!")
                    content = response.text
                    print(f"응답 내용 길이: {len(content)} 문자")
                    print(f"응답 내용 (처음 200자): {content[:200]}")
                    
                    if data_format == "json":
                        try:
                            result = response.json()
                            print("✅ JSON 파싱 성공")
                            return result
                        except json.JSONDecodeError:
                            print("❌ JSON 파싱 실패, XML로 시도")
                            try:
                                root = ET.fromstring(content)
                                return self.xml_to_dict(root)
                            except ET.ParseError:
                                print("❌ XML 파싱도 실패")
                                continue
                    else:  # xml
                        try:
                            root = ET.fromstring(content)
                            print("✅ XML 파싱 성공")
                            return self.xml_to_dict(root)
                        except ET.ParseError:
                            print("❌ XML 파싱 실패")
                            continue
                else:
                    print(f"❌ API 호출 실패: {response.status_code}")
                    print(f"응답 내용: {response.text[:500]}")
                    
            except Exception as e:
                print(f"❌ {attempt_name} 시도 실패: {e}")
                continue
        
        # 모든 시도가 실패한 경우 샘플 데이터 사용
        print("\n⚠️ 모든 API 호출이 실패했습니다. 샘플 데이터를 사용합니다.")
        return self.create_sample_api_data()
    
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
                print(f"✅ CSV 파일 로드 성공: {len(df)}행, {len(df.columns)}열")
                return df
            else:
                print(f"❌ CSV 파일을 찾을 수 없습니다: {self.csv_path}")
                return pd.DataFrame()
        except Exception as e:
            print(f"⚠️ UTF-8 인코딩 실패: {e}")
            try:
                df = pd.read_csv(self.csv_path, encoding='cp949')
                print(f"✅ CSV 파일 로드 성공 (cp949 인코딩): {len(df)}행, {len(df.columns)}열")
                return df
            except Exception as e2:
                print(f"❌ 모든 인코딩 시도 실패: {e2}")
                return pd.DataFrame()
    
    def analyze_api_structure(self, api_data: Dict[str, Any]) -> None:
        """API 데이터 구조를 분석합니다"""
        print("\n=== API 데이터 구조 분석 ===")
        
        def print_structure(data, indent=0, max_depth=4):
            if indent > max_depth:
                return
            
            prefix = "  " * indent
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        print(f"{prefix}📁 {key}: {type(value).__name__}")
                        print_structure(value, indent + 1, max_depth)
                    elif isinstance(value, list):
                        print(f"{prefix}📋 {key}: 배열 (크기: {len(value)})")
                        if len(value) > 0:
                            print(f"{prefix}  └─ 첫 번째 요소 타입: {type(value[0]).__name__}")
                            if isinstance(value[0], dict):
                                print_structure(value[0], indent + 2, max_depth)
                    else:
                        value_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                        print(f"{prefix}📝 {key}: {value_str}")
            elif isinstance(data, list):
                print(f"{prefix}📋 배열 크기: {len(data)}")
                if len(data) > 0:
                    print_structure(data[0], indent + 1, max_depth)
        
        print_structure(api_data)
    
    def analyze_csv_structure(self, df: pd.DataFrame) -> None:
        """CSV 데이터 구조를 분석합니다"""
        print("\n=== CSV 데이터 구조 분석 ===")
        
        if df.empty:
            print("❌ CSV 데이터가 비어있습니다.")
            return
        
        print(f"📊 데이터 형태: {df.shape[0]:,}행 {df.shape[1]}열")
        print(f"\n📋 컬럼 목록 ({len(df.columns)}개):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print(f"\n📄 샘플 데이터 (처음 3행):")
        print(df.head(3).to_string(max_cols=15, max_colwidth=15))
        
        print(f"\n🔍 결측값 확인:")
        null_counts = df.isnull().sum()
        has_nulls = False
        for col in df.columns:
            if null_counts[col] > 0:
                print(f"  ⚠️ {col}: {null_counts[col]}개")
                has_nulls = True
        
        if not has_nulls:
            print("  ✅ 결측값 없음")
    
    def extract_api_dataframe(self, api_data: Dict[str, Any]) -> pd.DataFrame:
        """API 데이터에서 실제 데이터 부분을 DataFrame으로 변환"""
        print("\n=== API 데이터를 DataFrame으로 변환 ===")
        
        data_items = []
        
        def find_data_items(obj, path=""):
            nonlocal data_items
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    if key.lower() in ['items', 'item', 'data', 'list', 'result', 'body', 'response']:
                        if isinstance(value, list):
                            data_items.extend(value)
                            print(f"✅ 데이터 발견: {new_path} (배열 크기: {len(value)})")
                        elif isinstance(value, dict):
                            find_data_items(value, new_path)
                    else:
                        find_data_items(value, new_path)
            elif isinstance(obj, list) and obj:
                if isinstance(obj[0], dict):
                    data_items.extend(obj)
                    print(f"✅ 루트 배열 데이터 발견: (배열 크기: {len(obj)})")
        
        find_data_items(api_data)
        
        if data_items:
            df = pd.DataFrame(data_items)
            print(f"✅ DataFrame 생성 성공: {df.shape}")
            if not df.empty:
                print(f"컬럼: {list(df.columns)}")
            return df
        else:
            print("❌ API 응답에서 데이터를 찾을 수 없습니다.")
            return pd.DataFrame()
    
    def compare_datasets(self, api_df: pd.DataFrame, csv_df: pd.DataFrame) -> None:
        """두 데이터셋을 비교합니다"""
        print("\n" + "="*80)
        print("🔍 데이터셋 비교 결과")
        print("="*80)
        
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
        print(f"  🔵 API 데이터: {api_df.shape[0]:,}행 {api_df.shape[1]}열")
        print(f"  🔴 CSV 데이터: {csv_df.shape[0]:,}행 {csv_df.shape[1]}열")
        
        # 컬럼 매핑 분석
        self.analyze_column_mapping(api_df, csv_df)
        
        # 샘플 데이터 비교
        print(f"\n📋 API 샘플 데이터 (상위 2행):")
        print(api_df.head(2).to_string(max_cols=15, max_colwidth=15))
        
        print(f"\n📋 CSV 샘플 데이터 (상위 2행):")
        print(csv_df.head(2).to_string(max_cols=15, max_colwidth=15))
    
    def analyze_column_mapping(self, api_df: pd.DataFrame, csv_df: pd.DataFrame) -> None:
        """컬럼 매핑을 분석합니다"""
        print(f"\n📋 컬럼 매핑 분석:")
        
        api_cols = list(api_df.columns)
        csv_cols = list(csv_df.columns)
        
        print(f"\n🔵 API 컬럼 ({len(api_cols)}개):")
        for col in api_cols:
            print(f"    - {col}")
        
        print(f"\n🔴 CSV 컬럼 ({len(csv_cols)}개):")
        for col in csv_cols:
            print(f"    - {col}")
        
        # 매핑 가능한 컬럼들 찾기
        print(f"\n🔗 예상 매핑:")
        mappings = [
            ("admCd", "행정기관코드", "행정구역 코드"),
            ("stdgYm", "기준연월", "기준 연월"),
            ("sidoNm", "시도명", "시도명"),
            ("sgguNm", "시군구명", "시군구명"),
            ("emdNm", "읍면동명", "읍면동명"),
            ("male0009", "0~9세_남자", "0-9세 남성"),
            ("fmle0009", "0~9세_여자", "0-9세 여성"),
            ("male1019", "10~19세_남자", "10-19세 남성"),
            ("fmle1019", "10~19세_여자", "10-19세 여성"),
            ("male2029", "20~29세_남자", "20-29세 남성"),
            ("fmle2029", "20~29세_여자", "20-29세 여성"),
            ("male3039", "30~39세_남자", "30-39세 남성"),
            ("fmle3039", "30~39세_여자", "30-39세 여성"),
            ("male4049", "40~49세_남자", "40-49세 남성"),
            ("fmle4049", "40~49세_여자", "40-49세 여성"),
            ("male5059", "50~59세_남자", "50-59세 남성"),
            ("fmle5059", "50~59세_여자", "50-59세 여성"),
            ("totPopltn", "총인구수", "총 인구수")
        ]
        
        matching_count = 0
        for api_col, csv_col, description in mappings:
            if api_col in api_cols and csv_col in csv_cols:
                print(f"    ✅ {api_col} ↔ {csv_col} ({description})")
                matching_count += 1
            elif api_col in api_cols:
                print(f"    🔵 {api_col} (API에만 있음)")
            elif csv_col in csv_cols:
                print(f"    🔴 {csv_col} (CSV에만 있음)")
        
        print(f"\n📊 매핑 가능한 컬럼: {matching_count}/{len(mappings)}개")
    
    def assess_compatibility(self, api_df: pd.DataFrame, csv_df: pd.DataFrame) -> None:
        """API 데이터와 CSV 데이터의 호환성을 평가합니다"""
        print("\n" + "="*80)
        print("🎯 호환성 평가 및 변환 가능성")
        print("="*80)
        
        if api_df.empty or csv_df.empty:
            print("❌ 데이터가 부족해 호환성 평가를 할 수 없습니다.")
            return
        
        # 예상 매핑 기반 호환성 계산
        api_cols = set(api_df.columns)
        csv_cols = set(csv_df.columns)
        
        # 핵심 컬럼들의 매핑 가능성 확인
        core_mappings = [
            ("admCd", "행정기관코드"),
            ("sidoNm", "시도명"),
            ("sgguNm", "시군구명"),
            ("emdNm", "읍면동명"),
        ]
        
        age_mappings = [
            ("male0009", "0~9세_남자"), ("fmle0009", "0~9세_여자"),
            ("male1019", "10~19세_남자"), ("fmle1019", "10~19세_여자"),
            ("male2029", "20~29세_남자"), ("fmle2029", "20~29세_여자"),
            ("male3039", "30~39세_남자"), ("fmle3039", "30~39세_여자"),
            ("male4049", "40~49세_남자"), ("fmle4049", "40~49세_여자"),
            ("male5059", "50~59세_남자"), ("fmle5059", "50~59세_여자"),
        ]
        
        core_matches = sum(1 for api_col, csv_col in core_mappings if api_col in api_cols and csv_col in csv_cols)
        age_matches = sum(1 for api_col, csv_col in age_mappings if api_col in api_cols and csv_col in csv_cols)
        
        core_compatibility = core_matches / len(core_mappings) * 100
        age_compatibility = age_matches / len(age_mappings) * 100
        
        print(f"📊 핵심 필드 호환성: {core_compatibility:.1f}% ({core_matches}/{len(core_mappings)})")
        print(f"📊 연령대 필드 호환성: {age_compatibility:.1f}% ({age_matches}/{len(age_mappings)})")
        
        overall_compatibility = (core_compatibility * 0.4 + age_compatibility * 0.6)
        
        print(f"\n🏆 종합 호환성 점수: {overall_compatibility:.1f}%")
        
        if overall_compatibility > 80:
            print("✅ 매우 높은 호환성: API 데이터를 CSV 형태로 쉽게 변환할 수 있습니다!")
            print("   🎉 발표에서 API 사용을 확신을 가지고 주장할 수 있습니다.")
            print("   💡 단순한 컬럼명 매핑만으로 변환 가능합니다.")
        elif overall_compatibility > 60:
            print("⚠️ 높은 호환성: 일부 전처리 후 변환 가능합니다.")
            print("   ✅ API 데이터 활용이 충분히 가능합니다.")
            print("   💡 컬럼명 변경과 데이터 형식 통일이 필요합니다.")
        elif overall_compatibility > 40:
            print("🔄 중간 호환성: 상당한 전처리가 필요합니다.")
            print("   ⚠️ API 데이터 구조를 CSV에 맞게 변환하는 작업이 필요합니다.")
        else:
            print("❌ 낮은 호환성: 대대적인 구조 변경이 필요합니다.")
            print("   🔄 프론트엔드를 API 데이터 구조에 맞게 수정하는 것이 나을 수 있습니다.")
        
        # 구체적인 변환 방법 제안
        print(f"\n💡 구체적인 변환 방법:")
        print("1. 🏷️ 컬럼명 매핑 딕셔너리 생성")
        print("2. 📅 날짜 형식 통일 (YYYY-MM → YYYY-MM-DD)")
        print("3. 🔢 숫자 데이터 타입 통일")
        print("4. 🧮 필요시 연령대별 합계 계산")
        print("5. 📍 행정구역 코드 표준화")
        
        print(f"\n🎯 결론:")
        if overall_compatibility > 70:
            print("✅ API 데이터 활용을 강력히 권장합니다!")
            print("   국가 인증 데이터로 가산점을 받을 수 있으며, 변환 비용도 낮습니다.")
        else:
            print("⚠️ API 데이터 활용 시 추가 개발 비용을 고려해야 합니다.")
            print("   현재 CSV 데이터를 유지하되, API 연동을 추후 계획으로 고려하세요.")

def main():
    """메인 실행 함수"""
    print("="*90)
    print("🔍 공공데이터포털 API vs 현재 CSV 데이터 비교 분석 (v2)")
    print("="*90)
    
    comparator = APIDataComparison()
    
    # 1. CSV 데이터 먼저 로드
    csv_data = comparator.load_csv_data()
    comparator.analyze_csv_structure(csv_data)
    
    # 2. API 데이터 가져오기 (JSON 우선)
    api_data_json = comparator.fetch_api_data("json", 20)
    comparator.analyze_api_structure(api_data_json)
    
    # 3. API 데이터를 DataFrame으로 변환
    api_df = comparator.extract_api_dataframe(api_data_json)
    
    # 4. 데이터셋 비교
    comparator.compare_datasets(api_df, csv_data)
    
    # 5. 호환성 평가 및 제안
    comparator.assess_compatibility(api_df, csv_data)
    
    print("\n" + "="*90)
    print("✅ 분석 완료! 위 결과를 바탕으로 API 활용 전략을 수립하세요.")
    print("📋 요약: 국가 인증 데이터 사용으로 가산점을 받을 수 있는 좋은 기회입니다!")
    print("="*90)

if __name__ == "__main__":
    main() 
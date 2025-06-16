"""
소상공인시장진흥공단_상가(상권)정보_API 데이터 구조 분석
API 엔드포인트: https://apis.data.go.kr/B553077/api/open/sdsc2
"""

import requests
import pandas as pd
import json
from typing import Dict, Any, List
import urllib.parse

class BusinessAPIAnalyzer:
    def __init__(self):
        # API 설정
        self.base_url = "https://apis.data.go.kr/B553077/api/open/sdsc2"
        self.encoding_key = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb%2FcuUI4dZSKEukcnq1me2b99jyFg%3D%3D"
        self.decoding_key = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg=="
        
    def test_api_call(self, use_encoding_key=True):
        """API 호출 테스트"""
        try:
            # 기본 파라미터 설정
            params = {
                'serviceKey': self.encoding_key if use_encoding_key else self.decoding_key,
                'pageNo': '1',
                'numOfRows': '10',  # 일단 10개만 가져와서 구조 파악
                'type': 'json'  # JSON 형태로 요청
            }
            
            print(f"API 호출 시도 - Encoding Key 사용: {use_encoding_key}")
            print(f"URL: {self.base_url}")
            print(f"Parameters: {params}")
            
            response = requests.get(self.base_url, params=params, timeout=30)
            print(f"응답 상태 코드: {response.status_code}")
            print(f"응답 헤더: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ JSON 파싱 성공!")
                    return data
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 파싱 실패: {e}")
                    print(f"응답 내용 (처음 500자): {response.text[:500]}")
                    return None
            else:
                print(f"❌ API 호출 실패: {response.status_code}")
                print(f"응답 내용: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 요청 오류: {e}")
            return None
    
    def analyze_data_structure(self, data: Dict[str, Any]):
        """데이터 구조 분석"""
        print("\n" + "="*50)
        print("📊 데이터 구조 분석")
        print("="*50)
        
        def print_structure(obj, indent=0):
            """재귀적으로 데이터 구조 출력"""
            prefix = "  " * indent
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, (dict, list)):
                        print(f"{prefix}{key}: {type(value).__name__}")
                        if isinstance(value, list) and len(value) > 0:
                            print(f"{prefix}  └─ 배열 길이: {len(value)}")
                            if isinstance(value[0], dict):
                                print(f"{prefix}  └─ 첫 번째 요소 구조:")
                                print_structure(value[0], indent + 2)
                        elif isinstance(value, dict):
                            print_structure(value, indent + 1)
                    else:
                        print(f"{prefix}{key}: {type(value).__name__} = {value}")
            elif isinstance(obj, list):
                print(f"{prefix}배열 길이: {len(obj)}")
                if len(obj) > 0:
                    print(f"{prefix}첫 번째 요소:")
                    print_structure(obj[0], indent + 1)
        
        print_structure(data)
    
    def create_sample_dataframe(self, data: Dict[str, Any]):
        """샘플 데이터로 DataFrame 생성"""
        print("\n" + "="*50)
        print("📋 DataFrame 생성 시도")
        print("="*50)
        
        # 일반적인 공공데이터 API 응답 구조 탐색
        possible_data_keys = ['response', 'body', 'items', 'item', 'data', 'result']
        
        items_data = None
        for key in possible_data_keys:
            if key in data:
                current = data[key]
                print(f"'{key}' 키 발견: {type(current)}")
                
                # 중첩 구조 탐색
                if isinstance(current, dict):
                    for sub_key in possible_data_keys:
                        if sub_key in current:
                            print(f"  └─ '{sub_key}' 하위 키 발견: {type(current[sub_key])}")
                            if isinstance(current[sub_key], list):
                                items_data = current[sub_key]
                                break
                elif isinstance(current, list):
                    items_data = current
                    break
        
        if items_data and len(items_data) > 0:
            try:
                df = pd.DataFrame(items_data)
                print(f"✅ DataFrame 생성 성공!")
                print(f"   - 행 수: {len(df)}")
                print(f"   - 열 수: {len(df.columns)}")
                print(f"   - 컬럼명: {list(df.columns)}")
                
                return df
            except Exception as e:
                print(f"❌ DataFrame 생성 실패: {e}")
                return None
        else:
            print("❌ 적절한 데이터 배열을 찾을 수 없습니다.")
            return None
    
    def analyze_dataframe(self, df: pd.DataFrame):
        """DataFrame 상세 분석"""
        print("\n" + "="*50)
        print("🔍 DataFrame 상세 분석")
        print("="*50)
        
        print("📊 기본 정보:")
        print(f"   - 데이터 형태: {df.shape}")
        print(f"   - 메모리 사용량: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        print("\n📋 컬럼 정보:")
        for i, col in enumerate(df.columns):
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            print(f"   {i+1:2d}. {col:20s} | {str(dtype):10s} | Null: {null_count:2d} | Unique: {unique_count:4d}")
        
        print("\n📝 샘플 데이터 (처음 3행):")
        print(df.head(3).to_string())
        
        print("\n🎯 위치/상권 관련 컬럼 추출:")
        location_keywords = ['주소', '위치', '좌표', '경도', '위도', 'addr', 'address', 'lat', 'lng', 'lon', 'x', 'y', '구', '동', '시', '도']
        business_keywords = ['업종', '상호', '업체', '상가', '점포', '매장', 'business', 'store', 'shop', 'category', 'type']
        
        location_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in location_keywords)]
        business_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in business_keywords)]
        
        print(f"   위치 관련: {location_cols}")
        print(f"   업종 관련: {business_cols}")
        
        return {
            'location_columns': location_cols,
            'business_columns': business_cols,
            'total_columns': list(df.columns),
            'sample_data': df.head(3).to_dict('records')
        }
    
    def create_sample_data_for_testing(self):
        """API 호출 실패 시 샘플 데이터 생성"""
        print("\n" + "="*50)
        print("🔧 샘플 데이터 생성 (API 호출 실패 시)")
        print("="*50)
        
        # 일반적인 상가 정보 API 구조 예상
        sample_data = [
            {
                "상호명": "카페 드림",
                "업종명": "커피전문점",
                "도로명주소": "서울특별시 강남구 테헤란로 123",
                "지번주소": "서울특별시 강남구 역삼동 123-45",
                "경도": "127.0276",
                "위도": "37.4979",
                "시도명": "서울특별시",
                "시군구명": "강남구",
                "행정동명": "역삼동",
                "개업일자": "20230315",
                "폐업일자": "",
                "상태구분": "영업"
            },
            {
                "상호명": "맛있는 식당",
                "업종명": "한식음식점",
                "도로명주소": "서울특별시 강남구 테헤란로 125",
                "지번주소": "서울특별시 강남구 역삼동 123-47",
                "경도": "127.0278",
                "위도": "37.4981",
                "시도명": "서울특별시",
                "시군구명": "강남구",
                "행정동명": "역삼동",
                "개업일자": "20220801",
                "폐업일자": "",
                "상태구분": "영업"
            },
            {
                "상호명": "편의점24",
                "업종명": "편의점",
                "도로명주소": "서울특별시 강남구 테헤란로 127",
                "지번주소": "서울특별시 강남구 역삼동 123-49",
                "경도": "127.0280",
                "위도": "37.4983",
                "시도명": "서울특별시",
                "시군구명": "강남구",
                "행정동명": "역삼동",
                "개업일자": "20210601",
                "폐업일자": "",
                "상태구분": "영업"
            }
        ]
        
        df = pd.DataFrame(sample_data)
        print("✅ 샘플 DataFrame 생성 완료")
        return df

def main():
    """메인 실행 함수"""
    print("🏪 소상공인시장진흥공단 상가정보 API 분석 시작")
    print("="*60)
    
    analyzer = BusinessAPIAnalyzer()
    
    # 1. Encoding Key로 API 호출 시도
    data = analyzer.test_api_call(use_encoding_key=True)
    
    # 2. 실패 시 Decoding Key로 재시도
    if data is None:
        print("\n🔄 Decoding Key로 재시도...")
        data = analyzer.test_api_call(use_encoding_key=False)
    
    # 3. API 호출 성공 시 데이터 분석
    if data is not None:
        analyzer.analyze_data_structure(data)
        df = analyzer.create_sample_dataframe(data)
        
        if df is not None:
            analysis_result = analyzer.analyze_dataframe(df)
            
            # 분석 결과 저장
            with open('business_api_analysis_result.json', 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            print(f"\n💾 분석 결과가 'business_api_analysis_result.json'에 저장되었습니다.")
            
            return df
    
    # 4. API 호출 실패 시 샘플 데이터로 분석
    print("\n🔄 샘플 데이터로 분석 진행...")
    df = analyzer.create_sample_data_for_testing()
    analysis_result = analyzer.analyze_dataframe(df)
    
    print("\n" + "="*60)
    print("📋 분석 완료 - 다음 단계 제안:")
    print("1. 실제 API 데이터 구조 확인")
    print("2. Leaflet 지도 연동 방안 설계")
    print("3. 비즈니스 위치 설정 페이지 개선 방향 논의")
    print("="*60)
    
    return df

if __name__ == "__main__":
    df = main() 
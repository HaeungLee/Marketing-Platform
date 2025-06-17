import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from datetime import datetime
import logging
from ...config.settings import Settings

logger = logging.getLogger(__name__)

class BusinessStoreAPIClient:
    """소상공인시장진흥공단 상가(상권) 정보 API 클라이언트"""
    
    def __init__(self):
        self.settings = Settings()
        self.base_url = "https://apis.data.go.kr/B553077/api/open/sdsc2"
        # 제공받은 인증키 사용
        self.service_key = "gQc0yFNcfSJFxqpfs1cTqhCll64HdzEQjHYSKeOYUpUMcrS2rqjroogqUOb/cuUI4dZSKEukcnq1me2b99jyFg=="
        
    async def get_stores_by_region(
        self, 
        sido_cd: str, 
        sigungu_cd: str = None,
        dong_cd: str = None,
        page_no: int = 1,
        num_of_rows: int = 1000
    ) -> List[Dict]:
        """지역별 상가 정보 조회"""
        
        params = {
            'serviceKey': self.service_key,
            'pageNo': page_no,
            'numOfRows': num_of_rows,
            'type': 'xml',  # JSON도 가능하지만 XML이 더 안정적
            'divId': 'ctprvnCd',  # 시도코드 기준 조회
            'key': sido_cd
        }
        
        # 시군구 코드가 있으면 추가
        if sigungu_cd:
            params['divId'] = 'signguCd'
            params['key'] = sigungu_cd
            
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                # XML 응답 파싱
                return self._parse_xml_response(response.text)
                
        except httpx.HTTPStatusError as e:
            logger.error(f"API 호출 실패: {e.response.status_code}")
            raise
        except Exception as e:
            logger.error(f"상가 정보 조회 오류: {str(e)}")
            raise
    
    def _parse_xml_response(self, xml_text: str) -> List[Dict]:
        """XML 응답을 딕셔너리 리스트로 변환"""
        stores = []
        
        try:
            root = ET.fromstring(xml_text)
            
            # 응답 구조: response > body > items > item
            items = root.findall('.//item')
            
            for item in items:
                store_data = {}
                
                # 각 필드 매핑
                field_mapping = {
                    'bizesId': 'store_number',           # 상가업소번호
                    'bizesNm': 'store_name',             # 상호명
                    'indsLclsCd': 'business_code',       # 업종코드
                    'indsLclsNm': 'business_name',       # 업종명
                    'lon': 'longitude',                  # 경도
                    'lat': 'latitude',                   # 위도
                    'lnmadr': 'jibun_address',          # 지번주소
                    'rdnmadr': 'road_address',          # 도로명주소
                    'ctprvnNm': 'sido_name',            # 시도명
                    'signguNm': 'sigungu_name',         # 시군구명
                    'adongNm': 'dong_name',             # 행정동명
                    'bldNm': 'building_name',           # 건물명
                    'flrInfo': 'floor_info',            # 층정보
                    'hoInfo': 'room_info',              # 호정보
                    'opnDt': 'open_date',              # 개업일자
                    'clsDt': 'close_date',             # 폐업일자
                    'trdStateNm': 'business_status',    # 영업상태
                    'ksicCd': 'standard_industry_code', # 표준산업분류코드
                    'ctgryThreeNm': 'commercial_category_code'  # 상권업종분류
                }
                
                for xml_field, db_field in field_mapping.items():
                    element = item.find(xml_field)
                    if element is not None and element.text:
                        value = element.text.strip()
                        
                        # 데이터 타입 변환
                        if db_field in ['longitude', 'latitude']:
                            try:
                                store_data[db_field] = float(value)
                            except ValueError:
                                store_data[db_field] = None
                        elif db_field in ['open_date', 'close_date']:
                            try:
                                # YYYYMMDD 형식을 datetime으로 변환
                                if len(value) == 8:
                                    store_data[db_field] = datetime.strptime(value, '%Y%m%d').date()
                                else:
                                    store_data[db_field] = None
                            except ValueError:
                                store_data[db_field] = None
                        else:
                            store_data[db_field] = value
                    else:
                        store_data[db_field] = None
                
                # 필수 필드가 있는 경우만 추가
                if (store_data.get('store_number') and 
                    store_data.get('store_name') and 
                    store_data.get('longitude') and 
                    store_data.get('latitude')):
                    stores.append(store_data)
                    
        except ET.ParseError as e:
            logger.error(f"XML 파싱 오류: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"응답 처리 오류: {str(e)}")
            raise
            
        return stores
    
    async def get_available_regions(self) -> Dict[str, List]:
        """사용 가능한 지역 코드 조회 (하드코딩 또는 별도 API)"""
        # 실제로는 별도 API나 코드표를 통해 조회해야 함
        # 여기서는 주요 지역만 예시로 제공
        return {
            "sido_codes": [
                {"code": "11", "name": "서울특별시"},
                {"code": "26", "name": "부산광역시"}, 
                {"code": "27", "name": "대구광역시"},
                {"code": "28", "name": "인천광역시"},
                {"code": "29", "name": "광주광역시"},
                {"code": "30", "name": "대전광역시"},
                {"code": "31", "name": "울산광역시"},
                {"code": "41", "name": "경기도"},
                {"code": "42", "name": "강원도"},
                {"code": "43", "name": "충청북도"},
                {"code": "44", "name": "충청남도"},
                {"code": "45", "name": "전라북도"},
                {"code": "46", "name": "전라남도"},
                {"code": "47", "name": "경상북도"},
                {"code": "48", "name": "경상남도"},
                {"code": "50", "name": "제주특별자치도"}
            ]
        } 
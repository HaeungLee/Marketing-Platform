"""
AI 서비스 인터페이스
SOLID 원칙: 인터페이스 분리 원칙 적용
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class AIService(ABC):
    """AI 서비스 추상 인터페이스"""
    
    @abstractmethod
    async def generate_content(self, 
                             business_info: Dict[str, Any], 
                             content_type: str = "blog",
                             target_audience: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        콘텐츠 생성
        
        Args:
            business_info: 비즈니스 정보
            content_type: 콘텐츠 타입 ('blog', 'instagram', 'youtube', 'flyer')
            target_audience: 타겟 고객 정보
            
        Returns:
            생성된 콘텐츠 딕셔너리
        """
        pass
    
    @abstractmethod
    async def generate_hashtags(self, content: str, business_info: Dict[str, Any]) -> List[str]:
        """
        해시태그 생성
        
        Args:
            content: 콘텐츠 텍스트
            business_info: 비즈니스 정보
            
        Returns:
            해시태그 리스트
        """
        pass
    
    @abstractmethod
    async def analyze_keywords(self, text: str) -> List[str]:
        """
        키워드 분석 (형태소 분석 대체)
        
        Args:
            text: 분석할 텍스트
            
        Returns:
            키워드 리스트
        """
        pass
    
    @abstractmethod
    async def measure_performance(self, model_name: str, prompt: str) -> Dict[str, Any]:
        """
        모델 성능 측정
        
        Args:
            model_name: 모델명
            prompt: 테스트 프롬프트
            
        Returns:
            성능 메트릭 딕셔너리 (추론 시간, 메모리 사용량 등)
        """
        pass
    
    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """
        사용 가능한 모델 목록 조회
        
        Returns:
            모델명 리스트
        """
        pass

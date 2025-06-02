"""
Google Gemini AI 서비스 구현 (간단한 버전)
"""
import os
from typing import Dict, Any, List
import time

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-generativeai package not available. Please install it.")

from src.application.interfaces.ai_service import AIService
from src.config.settings import settings

class GeminiService(AIService):
    def __init__(self, api_key: str = None):
        """
        Gemini 서비스 초기화
        """
        if not GENAI_AVAILABLE:
            raise ImportError("google-generativeai package is required")
        
        # API 키 설정
        self.api_key = api_key or settings.google_api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required")
        
        # Gemini 초기화
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemma-3-27b-it")
    
    async def generate_content(self, prompt: str) -> Dict[str, Any]:
        """콘텐츠 생성"""
        try:
            start_time = time.time()
            
            # Gemini API 호출
            response = self.model.generate_content(prompt)
            
            # 응답 처리
            if response and response.text:
                result = {
                    "content": response.text,
                    "performance_metrics": {
                        "response_time": time.time() - start_time,
                        "tokens_used": len(response.text.split())
                    }
                }
                return result
            else:
                raise Exception("Empty response from Gemini API")
                
        except Exception as e:
            print(f"Content generation error: {str(e)}")
            raise

    async def generate_hashtags(self, content: str, business_info: Dict[str, Any]) -> List[str]:
        """해시태그 생성"""
        try:
            prompt = f"다음 콘텐츠에 적합한 한국어 해시태그 5개를 생성해주세요 (# 기호 포함):\n{content[:500]}"
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # 해시태그 추출 (# 기호로 시작하는 단어들)
                hashtags = []
                for word in response.text.split():
                    if word.startswith('#'):
                        hashtags.append(word)
                
                # 기본 해시태그 추가 (결과가 없거나 부족한 경우)
                if len(hashtags) < 5:
                    default_tags = ['#마케팅', '#비즈니스', '#홍보', '#브랜드', '#성장']
                    hashtags.extend(default_tags[:(5 - len(hashtags))])
                
                return hashtags[:5]  # 최대 5개 반환
            
            return ['#마케팅', '#비즈니스', '#홍보', '#브랜드', '#성장']
            
        except Exception as e:
            print(f"Hashtag generation error: {str(e)}")
            return ['#마케팅', '#비즈니스', '#홍보', '#브랜드', '#성장']
    
    async def analyze_keywords(self, text: str) -> List[str]:
        """키워드 분석"""
        try:
            prompt = f"다음 텍스트에서 주요 키워드 5개를 추출해주세요:\n{text}"
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # 응답에서 키워드 추출
                keywords = [word.strip() for word in response.text.split(',')]
                return keywords[:5]  # 최대 5개 반환
            return []
            
        except Exception as e:
            print(f"Keyword analysis error: {str(e)}")
            return []
    
    async def get_available_models(self) -> List[str]:
        """사용 가능한 모델 목록 반환"""
        return ["gemma-3-27b-it"]  # 현재는 하나의 모델만 사용
    
    async def measure_performance(self, model_name: str, prompt: str) -> Dict[str, Any]:
        """성능 측정"""
        try:
            start_time = time.time()
            response = self.model.generate_content(prompt)
            end_time = time.time()
            
            return {
                "model": model_name,
                "response_time": end_time - start_time,
                "tokens_generated": len(response.text.split()) if response else 0,
                "status": "success"
            }
        except Exception as e:
            return {
                "model": model_name,
                "status": "error",
                "error": str(e)
            }
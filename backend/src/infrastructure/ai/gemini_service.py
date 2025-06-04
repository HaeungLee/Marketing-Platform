"""
Google Gemini AI 서비스 구현 (google-genai 패키지 사용)
"""
import asyncio
import base64
import os
import time
from typing import Dict, Any, List, Optional
from google import genai
from google.genai.types import GenerateContentConfig, Modality
from application.interfaces.ai_service import AIService


class GeminiService(AIService):
    """Google Gemini를 사용한 AI 서비스 구현체"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        
    async def generate_content(self, 
                             business_info: Dict[str, Any], 
                             content_type: str = "blog",
                             target_audience: Dict[str, Any] = None) -> Dict[str, Any]:
        """텍스트 콘텐츠 생성"""
        try:
            # 프롬프트 생성
            prompt = self._create_text_prompt(business_info, content_type, target_audience)
              # Gemini 모델 사용 (텍스트 생성)
            response = self.client.models.generate_content(
                model="gemma-3-27b-it",  # 현재 사용 가능한 최신 모델 사용
                contents=prompt
            )
            
            # 응답 파싱
            content_text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    content_text += part.text
            
            # 콘텐츠 포맷팅
            result = self._format_content(content_text, content_type, business_info)
            
            return result
            
        except Exception as e:
            print(f"Gemini 텍스트 생성 오류: {e}")
            return self._get_fallback_content(business_info, content_type)
  
    
    def _create_text_prompt(self, business_info: Dict[str, Any], content_type: str, target_audience: Dict[str, Any] = None) -> str:
        """텍스트 생성용 프롬프트 생성"""
        business_name = business_info.get("name", "비즈니스")
        category = business_info.get("category", "")
        product_name = business_info.get("product", {}).get("name", "상품")
        product_description = business_info.get("product", {}).get("description", "")
        tone = business_info.get("tone", "친근한")
        keywords = business_info.get("keywords", [])
        
        if content_type == "blog":
            prompt = f"""
{business_name}의 {product_name}에 대한 네이버 블로그 포스트를 작성해주세요.

비즈니스 정보:
- 업체명: {business_name}
- 업종: {category}
- 상품/서비스: {product_name}
- 상품 설명: {product_description}
- 톤앤매너: {tone}

요구사항:
1. SEO에 최적화된 제목 (30-40자)
2. 자연스러운 키워드 배치
3. 고객의 관심을 끄는 구성
4. 1000-1500자 분량
5. 단락별로 구성

키워드: {', '.join(keywords) if keywords else '없음'}
"""
        elif content_type == "instagram":
            prompt = f"""
{business_name}의 {product_name}에 대한 인스타그램 게시물을 작성해주세요.

비즈니스 정보:
- 업체명: {business_name}
- 업종: {category}
- 상품/서비스: {product_name}
- 상품 설명: {product_description}
- 톤앤매너: {tone}

요구사항:
1. 시선을 끄는 첫 문장
2. 150-300자 내외
3. 이모지 적절히 사용
4. 행동 유도 문구 포함
5. 해시태그는 별도로 생성하지 말고 본문만 작성

키워드: {', '.join(keywords) if keywords else '없음'}
"""
        elif content_type == "youtube":
            prompt = f"""
{business_name}의 {product_name}에 대한 유튜브 숏폼 스크립트를 작성해주세요.

비즈니스 정보:
- 업체명: {business_name}
- 업종: {category}
- 상품/서비스: {product_name}
- 상품 설명: {product_description}
- 톤앤매너: {tone}

요구사항:
1. 15-60초 분량의 스크립트
2. 후킹이 강한 첫 3초
3. 핵심 메시지 전달
4. 행동 유도 문구
5. 대화체 형식

키워드: {', '.join(keywords) if keywords else '없음'}
"""
        elif content_type == "flyer":
            prompt = f"""
{business_name}의 {product_name}에 대한 전단지 텍스트를 작성해주세요.

비즈니스 정보:
- 업체명: {business_name}
- 업종: {category}
- 상품/서비스: {product_name}
- 상품 설명: {product_description}
- 톤앤매너: {tone}

요구사항:
1. 강력한 헤드라인
2. 핵심 혜택 3-5개
3. 가격/할인 정보 영역
4. 연락처 정보 영역
5. 간결하고 임팩트 있는 문구

키워드: {', '.join(keywords) if keywords else '없음'}
"""
        else:
            prompt = f"{business_name}의 {product_name}에 대한 {tone} 톤의 마케팅 콘텐츠를 작성해주세요."
        
        return prompt
    
    def _format_content(self, content_text: str, content_type: str, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """생성된 콘텐츠 포맷팅"""
        lines = content_text.strip().split('\n')
        title = lines[0] if lines else f"{business_info.get('product', {}).get('name', '상품')} 소개"
        
        # 제목에서 특수문자 제거
        title = title.replace('#', '').replace('*', '').strip()
        
        return {
            "title": title,
            "content": content_text,
            "performance_metrics": {
                "generation_time": 0.5,  # 예시값
                "word_count": len(content_text.split()),
                "estimated_read_time": len(content_text.split()) / 200  # 분당 200단어
            }
        }
    
    async def generate_hashtags(self, content: str, business_info: Dict[str, Any]) -> List[str]:
        """해시태그 생성"""
        try:
            prompt = f"""
다음 콘텐츠와 비즈니스 정보를 바탕으로 인스타그램 해시태그 10-15개를 생성해주세요.

비즈니스: {business_info.get('name', '')} ({business_info.get('category', '')})
콘텐츠: {content[:200]}...

요구사항:
1. 관련성 높은 해시태그
2. 인기 해시태그와 니치 해시태그 조합
3. 지역 태그 포함 (가능한 경우)
4. 한글 해시태그도 포함
5. # 없이 단어만 반환

해시태그만 콤마로 구분해서 반환해주세요.
"""
            
            response = self.client.models.generate_content(
                model="gemma-3-27b-it",
                contents=prompt
            )
            
            hashtag_text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    hashtag_text += part.text
            
            # 해시태그 파싱
            hashtags = []
            for tag in hashtag_text.split(','):
                clean_tag = tag.strip().replace('#', '').strip()
                if clean_tag and len(clean_tag) > 1:
                    hashtags.append(clean_tag)
            
            return hashtags[:15]  # 최대 15개
            
        except Exception as e:
            print(f"해시태그 생성 오류: {e}")
            # 기본 해시태그 반환
            category = business_info.get('category', '').split('>')[-1] if business_info.get('category') else ''
            return [
                business_info.get('name', '비즈니스'),
                category,
                "맛집",
                "추천",
                "일상",
                "소상공인",
                "로컬",
                "이벤트"
            ]
    
    async def analyze_keywords(self, text: str) -> List[str]:
        """키워드 분석"""
        try:
            prompt = f"""
다음 텍스트에서 핵심 키워드를 5-10개 추출해주세요.

텍스트: {text[:500]}...

요구사항:
1. 마케팅에 중요한 키워드 우선
2. 브랜드/상품명 포함
3. 업종 관련 키워드
4. 감정/특성 키워드

키워드만 콤마로 구분해서 반환해주세요.
"""
            
            response = self.client.models.generate_content(
                model="gemma-3-27b-it",
                contents=prompt
            )
            
            keyword_text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    keyword_text += part.text
            
            # 키워드 파싱
            keywords = []
            for keyword in keyword_text.split(','):
                clean_keyword = keyword.strip()
                if clean_keyword and len(clean_keyword) > 1:
                    keywords.append(clean_keyword)
            
            return keywords[:10]  # 최대 10개
            
        except Exception as e:
            print(f"키워드 분석 오류: {e}")
            return ["마케팅", "추천", "고품질", "서비스", "고객만족"]
    
    async def get_available_models(self) -> List[str]:
        """사용 가능한 모델 목록 조회"""
        return [
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash-preview-image-generation"
        ]
        
    async def measure_performance(self, model_name: str, prompt: str) -> Dict[str, Any]:
        """
        모델 성능 측정
        
        Args:
            model_name: 모델명
            prompt: 테스트 프롬프트
            
        Returns:
            성능 메트릭 딕셔너리 (추론 시간, 메모리 사용량 등)
        """
        try:
            import psutil
            
            # 현재 프로세스 정보 가져오기
            process = psutil.Process(os.getpid())
            
            # 측정 시작
            start_memory = process.memory_info().rss / 1024 / 1024  # MB
            start_time = time.time()
              # 모델 실행
            try:
                response = self.client.models.generate_content(
                    model=model_name if model_name else "gemma-3-27b-it",
                    contents=prompt
                )
                
                # 결과 추출
                generated_text = ""
                if hasattr(response, 'candidates') and response.candidates:
                    if hasattr(response.candidates[0], 'content'):
                        for part in response.candidates[0].content.parts:
                            if hasattr(part, 'text'):
                                generated_text += part.text
                
                success = True
                token_count = len(generated_text.split())
                
            except Exception as e:
                print(f"모델 호출 오류: {e}")
                success = False
                token_count = 0
                generated_text = f"오류 발생: {str(e)}"
            
            # 측정 종료
            end_time = time.time()
            end_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # 결과 계산
            inference_time = (end_time - start_time) * 1000  # ms
            memory_used = end_memory - start_memory
            
            return {
                "model": model_name,
                "success": success,
                "inference_time_ms": round(inference_time, 2),
                "memory_usage_mb": round(memory_used, 2),
                "token_count": token_count,
                "sample_output": generated_text[:100] + "..." if len(generated_text) > 100 else generated_text
            }
            
        except Exception as e:
            print(f"성능 측정 오류: {e}")
            return {
                "model": model_name,
                "success": False,
                "inference_time_ms": 0,
                "memory_usage_mb": 0,
                "token_count": 0,
                "error": str(e)
            }
    
    def _get_fallback_content(self, business_info: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """폴백 콘텐츠 생성"""
        business_name = business_info.get("name", "우리 비즈니스")
        product_name = business_info.get("product", {}).get("name", "상품")
        
        if content_type == "blog":
            return {
                "title": f"{business_name}의 {product_name} 소개",
                "content": f"{business_name}에서 선보이는 {product_name}을 소개합니다.\n\n고품질의 서비스로 고객 만족을 위해 최선을 다하고 있습니다.\n\n지금 바로 문의해보세요!",
                "performance_metrics": {"generation_time": 0.1, "word_count": 30}
            }
        elif content_type == "instagram":
            return {
                "title": f"{product_name} 신상 출시! 🎉",
                "content": f"{business_name}의 {product_name}을 만나보세요! ✨\n\n특별한 혜택도 함께 준비했어요 💝\n\n지금 바로 DM 주세요! 📱",
                "performance_metrics": {"generation_time": 0.1, "word_count": 25}
            }
        elif content_type == "youtube":
            return {
                "title": f"{product_name} 리뷰 - {business_name}",
                "content": f"안녕하세요! 오늘은 {business_name}의 {product_name}에 대해 소개해 드릴게요.\n\n이 제품의 특별한 점은 무엇일까요?\n\n영상 끝까지 시청하시고 좋아요, 구독 부탁드립니다!",
                "performance_metrics": {"generation_time": 0.1, "word_count": 35}
            }
        elif content_type == "flyer":
            return {
                "title": f"{business_name} 스페셜 프로모션",
                "content": f"[특별 할인]\n{product_name} 프로모션\n\n지금 구매하시면 20% 할인!\n\n기간: 이번주 한정\n연락처: 000-0000-0000\n주소: 서울시 강남구",
                "performance_metrics": {"generation_time": 0.1, "word_count": 25}
            }
        else:
            return {
                "title": f"{business_name} - {product_name}",
                "content": f"{business_name}의 {product_name}을 소개합니다.",
                "performance_metrics": {"generation_time": 0.1, "word_count": 10}
            }
    
    async def close(self):
        """리소스 정리"""
        # Google Genai 클라이언트는 별도 종료 작업이 필요하지 않음
        pass
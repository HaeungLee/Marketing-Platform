"""
Ollama AI 서비스 구현
"""
import time
import psutil
import asyncio
from typing import Dict, Any, List
import httpx
from backend.src.application.interfaces.ai_service import AIService


class OllamaService(AIService):
    """Ollama를 사용한 AI 서비스 구현체"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def generate_content(self, 
                             business_info: Dict[str, Any], 
                             content_type: str = "blog",
                             target_audience: Dict[str, Any] = None) -> Dict[str, Any]:
        """콘텐츠 생성"""
        try:
            # 프롬프트 템플릿 선택
            prompt = self._create_prompt(business_info, content_type, target_audience)
            
            # 모델 선택 (기본: gemma3:1b)
            model = "gemma3:1b"
            
            # Ollama API 호출
            response = await self._call_ollama(model, prompt)
            
            # 응답 파싱
            content = self._parse_response(response, content_type)
            
            # 해시태그 생성
            if content_type in ["instagram", "blog"]:
                hashtags = await self.generate_hashtags(content.get("content", ""), business_info)
                content["hashtags"] = hashtags
            
            return content
            
        except Exception as e:
            # 에러 시 기본 응답 반환
            return self._get_fallback_content(business_info, content_type)
    
    async def generate_hashtags(self, content: str, business_info: Dict[str, Any]) -> List[str]:
        """해시태그 생성"""
        try:
            prompt = f"""
다음 비즈니스 정보와 콘텐츠를 바탕으로 인스타그램용 해시태그 10개를 생성해주세요.

비즈니스: {business_info.get('name', '')}
업종: {business_info.get('category', '')}
위치: {business_info.get('address', '서울')}

콘텐츠: {content[:200]}...

해시태그는 '#' 없이 단어만 나열해주세요. 한 줄에 하나씩 출력해주세요.
한국어와 영어를 혼합하여 사용하세요.
"""
            
            response = await self._call_ollama("gemma3:1b", prompt)
            hashtags = self._parse_hashtags(response)
            
            return hashtags
            
        except Exception:
            # 기본 해시태그 반환
            category = business_info.get('category', '').split('>')[-1]
            return [
                f"{business_info.get('name', '비즈니스')}",
                f"{category}",
                "서울맛집",
                "추천",
                "일상",
                "소상공인",
                "로컬",
                "맛집추천"
            ]
    
    async def analyze_keywords(self, text: str) -> List[str]:
        """키워드 분석"""
        try:
            prompt = f"""
다음 텍스트에서 중요한 키워드 10개를 추출해주세요.
한 줄에 하나씩 출력해주세요.

텍스트: {text}
"""
            
            response = await self._call_ollama("gemma3:1b", prompt)
            keywords = [line.strip() for line in response.split('\n') if line.strip()]
            
            return keywords[:10]
            
        except Exception:
            # 기본 키워드 반환
            words = text.split()
            return words[:10] if len(words) >= 10 else words
    
    async def measure_performance(self, model_name: str, prompt: str) -> Dict[str, Any]:
        """모델 성능 측정"""
        try:
            # 메모리 사용량 측정 시작
            process = psutil.Process()
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # 추론 시간 측정
            start_time = time.time()
            
            response = await self._call_ollama(model_name, prompt)
            
            end_time = time.time()
            inference_time_ms = (end_time - start_time) * 1000
            
            # 메모리 사용량 측정 종료
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_usage = memory_after - memory_before
            
            # 토큰 추정 (단어 수 기반)
            tokens = len(response.split())
            tokens_per_second = tokens / (inference_time_ms / 1000) if inference_time_ms > 0 else 0
            
            return {
                "model_name": model_name,
                "inference_time_ms": round(inference_time_ms, 2),
                "memory_usage_mb": round(memory_usage, 2),
                "tokens_per_second": round(tokens_per_second, 2),
                "response_length": len(response),
                "estimated_tokens": tokens
            }
            
        except Exception as e:
            return {
                "model_name": model_name,
                "error": str(e),
                "inference_time_ms": 0,
                "memory_usage_mb": 0,
                "tokens_per_second": 0
            }
    
    async def get_available_models(self) -> List[str]:
        """사용 가능한 모델 목록 조회"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            data = response.json()
            
            models = []
            for model in data.get("models", []):
                models.append(model.get("name", ""))
            
            return models
            
        except Exception:
            # 기본 모델 목록 반환
            return ["gemma3:1b", "qwen2.5:1.5b"]
    
    async def _call_ollama(self, model: str, prompt: str) -> str:
        """Ollama API 호출"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        response = await self.client.post(
            f"{self.base_url}/api/generate",
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code}")
        
        data = response.json()
        return data.get("response", "")
    
    def _create_prompt(self, business_info: Dict[str, Any], content_type: str, target_audience: Dict[str, Any] = None) -> str:
        """프롬프트 생성"""
        base_info = f"""
비즈니스 정보:
- 이름: {business_info.get('name', '')}
- 업종: {business_info.get('category', '')}
- 설명: {business_info.get('description', '')}
- 위치: {business_info.get('address', '서울')}
"""
        
        if target_audience:
            base_info += f"""
타겟 고객:
- 연령대: {target_audience.get('age_group', '20-40대')}
- 성별: {target_audience.get('gender', '전체')}
- 관심사: {target_audience.get('interests', [])}
"""
        
        prompts = {
            "blog": f"""{base_info}

위 정보를 바탕으로 네이버 블로그용 포스트를 작성해주세요.
- 제목과 본문으로 구성
- SEO를 고려한 키워드 포함
- 친근하고 매력적인 톤
- 300-500자 분량
""",
            "instagram": f"""{base_info}

위 정보를 바탕으로 인스타그램용 포스트를 작성해주세요.
- 짧고 임팩트 있는 문장
- 이모지 활용
- 100-150자 분량
""",
            "youtube": f"""{base_info}

위 정보를 바탕으로 30-60초 유튜브 숏폼 스크립트를 작성해주세요.
- 인트로, 메인, 아웃트로 구성
- 시청자의 관심을 끄는 내용
- 자막 형태로 구성
""",
            "flyer": f"""{base_info}

위 정보를 바탕으로 전단지용 카피를 작성해주세요.
- 제목, 부제목, 메인 내용으로 구성
- 간결하고 임팩트 있는 문구
- 연락처나 위치 정보 포함 유도
"""
        }
        
        return prompts.get(content_type, prompts["blog"])
    
    def _parse_response(self, response: str, content_type: str) -> Dict[str, Any]:
        """응답 파싱"""
        if content_type == "blog":
            # 제목과 본문 분리 시도
            lines = response.split('\n')
            title = lines[0] if lines else "제목"
            content = '\n'.join(lines[1:]) if len(lines) > 1 else response
            
            return {
                "title": title.strip(),
                "content": content.strip(),
                "type": "blog"
            }
        
        elif content_type == "youtube":
            return {
                "script": response.strip(),
                "estimated_duration": "30-60초",
                "type": "youtube"
            }
        
        else:
            return {
                "content": response.strip(),
                "type": content_type
            }
    
    def _parse_hashtags(self, response: str) -> List[str]:
        """해시태그 파싱"""
        lines = response.split('\n')
        hashtags = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                hashtags.append(line)
        
        return hashtags[:10]  # 최대 10개
    
    def _get_fallback_content(self, business_info: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """폴백 콘텐츠"""
        name = business_info.get('name', '우리 비즈니스')
        category = business_info.get('category', '').split('>')[-1] if business_info.get('category') else '서비스'
        
        fallback = {
            "blog": {
                "title": f"{name} - 특별한 {category} 경험을 만나보세요!",
                "content": f"{name}에서 제공하는 특별한 {category} 서비스를 소개합니다. 고객 만족을 위해 최선을 다하고 있습니다.",
                "type": "blog"
            },
            "instagram": {
                "content": f"✨ {name} ✨\n{category}의 새로운 경험 🎉\n#추천 #맛집 #서울",
                "type": "instagram"
            },
            "youtube": {
                "script": f"안녕하세요! {name}를 소개합니다. 특별한 {category} 서비스로 고객님을 기다리고 있어요!",
                "type": "youtube"
            }
        }
        
        return fallback.get(content_type, fallback["blog"])
    
    async def close(self):
        """리소스 정리"""
        await self.client.aclose()

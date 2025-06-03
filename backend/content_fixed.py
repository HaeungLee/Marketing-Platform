"""
수정된 콘텐츠 생성 API - gemma-3-27b-it 모델 사용
"""
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

app = FastAPI(title="Content Generation API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ContentGenerationRequest(BaseModel):
    business_id: str
    business_name: str
    business_category: str
    business_description: str
    product_name: str = Field(..., description="홍보할 상품/서비스명")
    product_description: str = Field(..., description="상품/서비스 설명")
    content_type: str = Field(..., description="콘텐츠 타입", pattern="^(blog|instagram|youtube|flyer)$")
    target_audience: Optional[Dict[str, Any]] = Field(None, description="타겟 고객층 정보")
    tone: Optional[str] = Field("친근한", description="콘텐츠 톤앤매너")
    keywords: Optional[List[str]] = Field(None, description="포함할 키워드")

# Response Models
class ContentGenerationResponse(BaseModel):
    content_id: str
    content_type: str
    title: Optional[str] = None
    content: str
    hashtags: List[str] = []
    keywords: List[str] = []
    estimated_engagement: Optional[str] = None
    performance_metrics: Dict[str, Any] = {}
    created_at: datetime

class GeminiContentService:
    """Gemini를 사용한 콘텐츠 생성 서비스"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            from google import genai
            self.client = genai.Client(api_key=api_key)
        except ImportError:
            raise Exception("google-genai 패키지가 설치되지 않았습니다.")
    
    async def generate_content(self, 
                             business_info: Dict[str, Any], 
                             content_type: str = "blog",
                             target_audience: Dict[str, Any] = None) -> Dict[str, Any]:
        """콘텐츠 생성"""
        try:
            # 프롬프트 생성
            prompt = self._create_prompt(business_info, content_type, target_audience)
            
            # gemma-3-27b-it 모델 사용
            response = self.client.models.generate_content(
                model="gemma-3-27b-it",
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
            print(f"Gemini 콘텐츠 생성 오류: {e}")
            return self._get_fallback_content(business_info, content_type)
    
    def _create_prompt(self, business_info: Dict[str, Any], content_type: str, target_audience: Dict[str, Any] = None) -> str:
        """프롬프트 생성"""
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

다음 형식으로 응답해주세요:
제목: [제목]
내용: [내용]
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

다음 형식으로 응답해주세요:
제목: [제목]
내용: [내용]
"""
        else:
            prompt = f"""
{business_name}의 {product_name}에 대한 {content_type} 콘텐츠를 작성해주세요.

비즈니스 정보:
- 업체명: {business_name}
- 업종: {category}
- 상품/서비스: {product_name}
- 상품 설명: {product_description}
- 톤앤매너: {tone}

키워드: {', '.join(keywords) if keywords else '없음'}

다음 형식으로 응답해주세요:
제목: [제목]
내용: [내용]
"""
        
        return prompt
    
    def _format_content(self, content_text: str, content_type: str, business_info: Dict[str, Any]) -> Dict[str, Any]:
        """콘텐츠 포맷팅"""
        lines = content_text.split('\n')
        title = ""
        content = ""
        
        for line in lines:
            if line.strip().startswith("제목:"):
                title = line.replace("제목:", "").strip()
            elif line.strip().startswith("내용:"):
                content = line.replace("내용:", "").strip()
            elif content and line.strip():
                content += "\n" + line
        
        if not title:
            title = f"{business_info.get('name', '')} {business_info.get('product', {}).get('name', '')} 소개"
        
        if not content:
            content = content_text
        
        return {
            "title": title,
            "content": content,
            "performance_metrics": {
                "estimated_read_time": len(content) // 200,  # 대략적인 읽기 시간 (분)
                "character_count": len(content),
                "word_count": len(content.split())
            }
        }
    
    def _get_fallback_content(self, business_info: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """fallback 콘텐츠"""
        business_name = business_info.get("name", "비즈니스")
        product_name = business_info.get("product", {}).get("name", "상품")
        
        if content_type == "blog":
            title = f"{business_name}의 {product_name} 소개"
            content = f"""
{business_name}에서 새롭게 선보이는 {product_name}을 소개합니다.

고객 여러분께 최고의 품질과 서비스를 제공하기 위해 끊임없이 노력하고 있습니다.

{product_name}의 특별한 장점:
- 뛰어난 품질
- 합리적인 가격
- 친절한 서비스

더 자세한 정보는 문의해 주세요!
"""
        elif content_type == "instagram":
            title = f"{product_name} 소개"
            content = f"""
✨ {business_name}의 특별한 {product_name}을 만나보세요! ✨

고객 만족을 위해 최선을 다하고 있습니다 💪

#문의환영 #최고품질 #합리적가격
"""
        else:
            title = f"{product_name} 소개"
            content = f"{business_name}의 {product_name}을 소개합니다. 최고의 품질로 고객 만족을 추구합니다."
        
        return {
            "title": title,
            "content": content,
            "performance_metrics": {
                "estimated_read_time": 1,
                "character_count": len(content),
                "word_count": len(content.split())
            }
        }
    
    async def generate_hashtags(self, content: str, business_info: Dict[str, Any]) -> List[str]:
        """해시태그 생성"""
        try:
            business_name = business_info.get("name", "")
            category = business_info.get("category", "")
            
            prompt = f"""
다음 콘텐츠에 적합한 해시태그 10개를 생성해주세요:

콘텐츠: {content[:200]}...
비즈니스: {business_name}
카테고리: {category}

요구사항:
- 한국어 해시태그 우선
- 트렌디하고 검색에 유리한 태그
- 비즈니스와 관련된 태그 포함
- # 기호 없이 태그명만 제공

응답 형식: 태그1, 태그2, 태그3, ...
"""
            
            response = self.client.models.generate_content(
                model="gemma-3-27b-it",
                contents=prompt
            )
            
            hashtags_text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    hashtags_text += part.text
            
            hashtags = [tag.strip() for tag in hashtags_text.split(',') if tag.strip()]
            return hashtags[:10]  # 최대 10개
            
        except Exception as e:
            print(f"해시태그 생성 오류: {e}")
            return ["마케팅", "비즈니스", "추천", "좋아요", "팔로우"]
    
    async def analyze_keywords(self, text: str) -> List[str]:
        """키워드 분석"""
        try:
            prompt = f"""
다음 텍스트에서 중요한 키워드 5개를 추출해주세요:

텍스트: {text[:500]}...

요구사항:
- 마케팅에 중요한 키워드 우선
- 브랜드명, 상품명 포함
- SEO에 유리한 키워드

응답 형식: 키워드1, 키워드2, 키워드3, ...
"""
            
            response = self.client.models.generate_content(
                model="gemma-3-27b-it",
                contents=prompt
            )
            
            keywords_text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    keywords_text += part.text
            
            keywords = [keyword.strip() for keyword in keywords_text.split(',') if keyword.strip()]
            return keywords[:5]  # 최대 5개
            
        except Exception as e:
            print(f"키워드 분석 오류: {e}")
            return ["마케팅", "비즈니스", "상품", "서비스", "고객"]

# 서비스 인스턴스 생성
def get_content_service():
    api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyDrPzr9VvEUGVU6a87DxyTQNs17_wldqBE")
    return GeminiContentService(api_key)

@app.post("/api/v1/content/generate", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    """
    마케팅 콘텐츠 생성
    
    비즈니스 정보와 상품 정보를 바탕으로 다양한 플랫폼용 마케팅 콘텐츠를 생성합니다.
    """
    try:
        # 서비스 인스턴스 생성
        content_service = get_content_service()
        
        # 비즈니스 정보 구성
        business_info = {
            "id": request.business_id,
            "name": request.business_name,
            "category": request.business_category,
            "description": request.business_description,
            "product": {
                "name": request.product_name,
                "description": request.product_description
            },
            "tone": request.tone,
            "keywords": request.keywords or []
        }
        
        # 콘텐츠 생성
        content_result = await content_service.generate_content(
            business_info=business_info,
            content_type=request.content_type,
            target_audience=request.target_audience
        )
        
        # 해시태그 생성
        hashtags = await content_service.generate_hashtags(
            content=content_result.get("content", ""),
            business_info=business_info
        )
        
        # 키워드 분석
        keywords = await content_service.analyze_keywords(
            text=content_result.get("content", "")
        )
        
        # 성능 메트릭 측정
        performance_metrics = content_result.get("performance_metrics", {})
        
        return ContentGenerationResponse(
            content_id=f"content-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            content_type=request.content_type,
            title=content_result.get("title"),
            content=content_result.get("content", ""),
            hashtags=hashtags,
            keywords=keywords,
            estimated_engagement=content_result.get("estimated_engagement"),
            performance_metrics=performance_metrics,
            created_at=datetime.now()
        )
        
    except Exception as e:
        print(f"콘텐츠 생성 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"콘텐츠 생성 중 오류가 발생했습니다: {str(e)}"
        )

@app.get("/")
async def root():
    return {"message": "Content Generation API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "content-generation"}

if __name__ == "__main__":
    import uvicorn
    print("Content Generation API 서버를 시작합니다...")
    print("API URL: http://localhost:8001/api/v1/content/generate")
    print("Health Check: http://localhost:8001/health")
    uvicorn.run(app, host="0.0.0.0", port=8001)

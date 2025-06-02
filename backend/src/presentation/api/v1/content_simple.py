"""
콘텐츠 생성 API 엔드포인트 (단순화된 버전)
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from application.interfaces.ai_service import AIService
from infrastructure.ai.gemini_service import GeminiService

router = APIRouter()


# Request Models
class ContentGenerationRequest(BaseModel):
    business_name: str = Field("우리 회사", description="회사/사업체명")
    business_description: str = Field("", description="사업 설명")
    product_name: str = Field("우리 제품", description="홍보할 상품/서비스명")
    product_description: str = Field("", description="상품/서비스 설명")
    content_type: str = Field("blog", description="콘텐츠 타입", pattern="^(blog|instagram|youtube|flyer)$")
    target_audience: Optional[Dict[str, Any]] = Field({}, description="타겟 고객층 정보")
    tone: Optional[str] = Field("친근한", description="콘텐츠 톤앤매너")
    keywords: Optional[List[str]] = Field([], description="포함할 키워드")


# Response Models
class ContentGenerationResponse(BaseModel):
    content_type: str
    title: Optional[str] = None
    content: str
    hashtags: List[str] = []
    keywords: List[str] = []
    performance_metrics: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.now)


# Dependency injection
def get_ai_service() -> AIService:
    """AI 서비스 의존성 주입"""
    return GeminiService()


@router.post("/generate", response_model=ContentGenerationResponse)
async def generate_content(
    request: ContentGenerationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    마케팅 콘텐츠 생성 (단순화된 버전)
    
    비즈니스 정보와 상품 정보를 바탕으로 다양한 플랫폼용 마케팅 콘텐츠를 생성합니다.
    """
    try:
        print(f"Received request: {request}")
        
        # 비즈니스 정보 구성 (단순화)
        business_info = {
            "name": request.business_name,
            "description": request.business_description,
            "product_name": request.product_name,
            "product_description": request.product_description,
            "tone": request.tone,
            "keywords": request.keywords or []
        }
        
        print(f"Business info: {business_info}")
        
        # 콘텐츠 생성
        content_result = await ai_service.generate_content(
            business_info=business_info,
            content_type=request.content_type,
            target_audience=request.target_audience
        )
        
        print(f"Content result: {content_result}")
        
        # 해시태그 생성 (선택적)
        hashtags = []
        try:
            hashtags = await ai_service.generate_hashtags(
                content=content_result.get("content", ""),
                business_info=business_info
            )
        except Exception as e:
            print(f"Hashtag generation failed: {e}")
            hashtags = ["#마케팅", "#비즈니스"]
        
        print(f"Generated hashtags: {hashtags}")
        
        # 응답 구성
        response = ContentGenerationResponse(
            content_type=request.content_type,
            title=content_result.get("title", f"{request.business_name} {request.content_type} 콘텐츠"),
            content=content_result.get("content", ""),
            hashtags=hashtags,
            keywords=request.keywords or [],
            performance_metrics=content_result.get("performance_metrics", {}),
            created_at=datetime.now()
        )
        
        print(f"Final response: {response}")
        return response
        
    except Exception as e:
        print(f"Error in generate_content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"콘텐츠 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/test")
async def test_ai_service(ai_service: AIService = Depends(get_ai_service)):
    """AI 서비스 테스트 엔드포인트"""
    try:
        test_business = {
            "name": "테스트 카페",
            "description": "맛있는 커피를 제공하는 카페"
        }
        
        result = await ai_service.generate_content(
            business_info=test_business,
            content_type="blog"
        )
        
        return {"status": "success", "result": result}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

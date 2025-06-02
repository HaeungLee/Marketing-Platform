"""
콘텐츠 생성 및 분석 API 엔드포인트
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


class HashtagGenerationRequest(BaseModel):
    content: str = Field(..., description="해시태그를 생성할 콘텐츠")
    business_name: str = Field("우리 회사", description="회사/사업체명")
    max_count: int = Field(10, ge=1, le=30, description="생성할 해시태그 최대 개수")


class KeywordAnalysisRequest(BaseModel):
    text: str = Field(..., description="분석할 텍스트")


class PerformanceTestRequest(BaseModel):
    model_name: str = Field(..., description="테스트할 모델명")
    prompt: str = Field(..., description="테스트용 프롬프트")


# Response Models
class ContentGenerationResponse(BaseModel):
    content_type: str
    title: Optional[str] = None
    content: str
    hashtags: List[str] = []
    keywords: List[str] = []
    performance_metrics: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.now)


class HashtagResponse(BaseModel):
    hashtags: List[str]
    generated_at: datetime


class KeywordAnalysisResponse(BaseModel):
    keywords: List[str]
    analyzed_at: datetime


class PerformanceMetricsResponse(BaseModel):
    model_name: str
    inference_time_ms: float
    memory_usage_mb: float
    token_count: Optional[int] = None
    quality_score: Optional[float] = None
    measured_at: datetime


class AvailableModelsResponse(BaseModel):
    models: List[str]
    default_model: str


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


@router.post("/hashtags", response_model=HashtagResponse)
async def generate_hashtags(
    request: HashtagGenerationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    해시태그 생성 (단순화된 버전)
    
    주어진 콘텐츠와 비즈니스 정보를 바탕으로 관련 해시태그를 생성합니다.
    """
    try:
        business_info = {
            "name": request.business_name
        }
        
        hashtags = await ai_service.generate_hashtags(
            content=request.content,
            business_info=business_info
        )
        
        # 최대 개수 제한
        hashtags = hashtags[:request.max_count]
        
        return HashtagResponse(
            hashtags=hashtags,
            generated_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"해시태그 생성 중 오류가 발생했습니다: {str(e)}"
        )


# 간단한 테스트 엔드포인트
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


@router.get("/models", response_model=AvailableModelsResponse)
async def get_available_models(ai_service: AIService = Depends(get_ai_service)):
    """
    사용 가능한 AI 모델 목록 조회
    
    AI 서비스에서 지원하는 모델들의 목록을 반환합니다.
    """
    try:
        models = await ai_service.get_available_models()
        
        return AvailableModelsResponse(
            models=models,
            default_model=models[0] if models else "gemma3:1b"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"모델 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/templates/{content_type}")
async def get_content_templates(content_type: str):
    """
    콘텐츠 템플릿 조회
    
    플랫폼별 콘텐츠 템플릿을 반환합니다.
    """
    templates = {
        "blog": {
            "title_format": "[업종] [상품명] - [특징/혜택]",
            "structure": [
                "인사말 및 도입",
                "상품/서비스 소개",
                "특징 및 장점",
                "고객 혜택",
                "문의 방법 및 위치"
            ],
            "recommended_length": "800-1200자",
            "seo_tips": ["키워드 자연스럽게 배치", "제목에 핵심 키워드 포함", "지역명 포함"]
        },
        "instagram": {
            "title_format": "[이모지] [간단한 후킹 멘트]",
            "structure": [
                "시선을 끄는 첫 문장",
                "상품/서비스 핵심 포인트",
                "고객 혜택 강조",
                "행동 유도 (CTA)"
            ],
            "recommended_length": "150-300자",
            "hashtag_count": "10-20개",
            "visual_tips": ["고화질 이미지", "일관된 필터", "브랜드 컬러 활용"]
        },
        "youtube": {
            "title_format": "[숫자/질문] [상품명] [결과/혜택]",
            "structure": [
                "강력한 오프닝 (3초 내)",
                "문제 제기",
                "솔루션 제시",
                "증명/사례",
                "행동 유도"
            ],
            "recommended_length": "15-60초 스크립트",
            "engagement_tips": ["질문으로 시작", "빠른 편집", "자막 활용"]
        },
        "flyer": {
            "title_format": "[이벤트/할인] [상품명]",
            "structure": [
                "눈에 띄는 헤드라인",
                "핵심 혜택/할인율",
                "상품 특징 (3-5개)",
                "연락처 및 위치",
                "기간 한정 표시"
            ],
            "design_tips": ["대비 강한 색상", "큰 폰트 사이즈", "여백 활용", "QR코드 포함"]
        }
    }
    
    if content_type not in templates:
        raise HTTPException(
            status_code=404,
            detail=f"'{content_type}' 타입의 템플릿을 찾을 수 없습니다."
        )
    
    return {
        "content_type": content_type,
        "template": templates[content_type],
        "examples": f"{content_type} 콘텐츠 예시들..."
    }

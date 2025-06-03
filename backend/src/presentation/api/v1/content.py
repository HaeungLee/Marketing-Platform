"""
콘텐츠 생성 및 분석 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import base64
import os

from application.interfaces.ai_service import AIService

router = APIRouter()


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


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="이미지 생성 프롬프트")
    business_name: Optional[str] = Field(None, description="비즈니스명")
    business_category: Optional[str] = Field(None, description="비즈니스 카테고리")
    style: Optional[str] = Field("professional", description="이미지 스타일")


class HashtagGenerationRequest(BaseModel):
    content: str = Field(..., description="해시태그를 생성할 콘텐츠")
    business_name: str
    business_category: str
    max_count: int = Field(10, ge=1, le=30, description="생성할 해시태그 최대 개수")


class KeywordAnalysisRequest(BaseModel):
    text: str = Field(..., description="분석할 텍스트")


class PerformanceTestRequest(BaseModel):
    model_name: str = Field(..., description="테스트할 모델명")
    prompt: str = Field(..., description="테스트용 프롬프트")


# Response Models
class ContentGenerationResponse(BaseModel):
    content_id: str
    content_type: str
    title: Optional[str] = None
    content: str
    hashtags: List[str]
    keywords: List[str]
    estimated_engagement: Optional[Dict[str, float]] = None
    performance_metrics: Dict[str, Any]
    created_at: datetime


class ImageGenerationResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    filename: Optional[str] = None
    prompt: str
    error: Optional[str] = None
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
    # 환경변수에서 API 키 가져오기
    api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyDrPzr9VvEUGVU6a87DxyTQNs17_wldqBE")
    try:
        from infrastructure.ai.gemini_service import GeminiService
        return GeminiService(api_key)
    except ImportError as e:
        # Gemini 서비스를 사용할 수 없는 경우
        raise HTTPException(status_code=500, detail=f"AI 서비스를 사용할 수 없습니다: {str(e)}")


def get_gemini_service():
    """Gemini 서비스 의존성 주입"""
    # 환경변수에서 API 키 가져오기
    api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyDrPzr9VvEUGVU6a87DxyTQNs17_wldqBE")
    
    try:
        from google import genai
        from google.genai.types import GenerateContentConfig, Modality
        
        class SimpleGeminiService:
            def __init__(self, api_key: str):
                self.client = genai.Client(api_key=api_key)
            
            async def generate_image(self, prompt: str, business_info: Dict[str, Any] = None) -> Dict[str, Any]:
                """이미지 생성"""
                try:
                    # 이미지 생성용 프롬프트 개선
                    enhanced_prompt = prompt
                    if business_info:
                        business_name = business_info.get("name", "")
                        category = business_info.get("category", "")
                        enhanced_prompt += f"\n\n비즈니스 컨텍스트: {business_name} ({category})"
                        enhanced_prompt += "\n고품질, 전문적인, 마케팅에 적합한 이미지"
                    
                    enhanced_prompt += "\n\nStyle: Professional, high-quality, marketing-ready"
                    enhanced_prompt += "\nResolution: High resolution, crisp details"
                    enhanced_prompt += "\nComposition: Well-balanced, visually appealing"
                    
                    # Gemini 2.0 Flash Image Generation 모델 사용
                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash-preview-image-generation",
                        contents=enhanced_prompt,
                        config=GenerateContentConfig(
                            response_modalities=[Modality.TEXT, Modality.IMAGE]
                        )
                    )
                    
                    # 응답에서 이미지 데이터 추출
                    for part in response.candidates[0].content.parts:
                        if part.inline_data:
                            image_data = self._process_image_data(part.inline_data)
                            return {
                                "success": True,
                                "image_data": image_data["data"],
                                "image_type": image_data["type"],
                                "filename": image_data["filename"],
                                "prompt": enhanced_prompt
                            }
                    
                    return {
                        "success": False,
                        "error": "이미지가 생성되지 않았습니다."
                    }
                    
                except Exception as e:
                    print(f"Gemini 이미지 생성 오류: {e}")
                    return {
                        "success": False,
                        "error": f"이미지 생성 중 오류가 발생했습니다: {str(e)}"
                    }
            
            def _process_image_data(self, inline_data) -> Dict[str, Any]:
                """이미지 데이터 처리"""
                try:
                    import time
                    
                    # 원본 데이터 타입 확인
                    raw_data = inline_data.data
                    mime_type = inline_data.mime_type
                    
                    # bytes 타입이면 그대로 사용, str 타입이면 base64 디코딩
                    if isinstance(raw_data, bytes):
                        image_data = raw_data
                    else:
                        image_data = base64.b64decode(raw_data)
                    
                    # 파일 확장자 결정
                    if mime_type == "image/png" or image_data.startswith(b'\x89PNG'):
                        file_extension = "png"
                    elif mime_type == "image/jpeg" or image_data.startswith(b'\xFF\xD8\xFF'):
                        file_extension = "jpg"
                    else:
                        file_extension = "png"  # 기본값
                    
                    # 파일명 생성
                    timestamp = int(time.time())
                    filename = f"generated_image_{timestamp}.{file_extension}"
                    
                    return {
                        "data": image_data,
                        "type": mime_type,
                        "filename": filename
                    }
                    
                except Exception as e:
                    raise Exception(f"이미지 데이터 처리 오류: {str(e)}")
        
        return SimpleGeminiService(api_key)
    except ImportError:
        raise HTTPException(status_code=500, detail="google-genai package not installed")


@router.post("/generate", response_model=ContentGenerationResponse)
async def generate_content(
    request: ContentGenerationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    마케팅 콘텐츠 생성
    
    비즈니스 정보와 상품 정보를 바탕으로 다양한 플랫폼용 마케팅 콘텐츠를 생성합니다.
    """
    try:
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
        content_result = await ai_service.generate_content(
            business_info=business_info,
            content_type=request.content_type,
            target_audience=request.target_audience
        )
        
        # 해시태그 생성
        hashtags = await ai_service.generate_hashtags(
            content=content_result.get("content", ""),
            business_info=business_info
        )
        
        # 키워드 분석
        keywords = await ai_service.analyze_keywords(
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
        raise HTTPException(
            status_code=500,
            detail=f"콘텐츠 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    gemini_service = Depends(get_gemini_service)
):
    """
    AI 이미지 생성
    
    주어진 프롬프트를 바탕으로 마케팅에 적합한 이미지를 생성합니다.
    """
    try:
        business_info = {
            "name": request.business_name,
            "category": request.business_category
        }
        
        # 이미지 생성
        result = await gemini_service.generate_image(
            prompt=request.prompt,
            business_info=business_info
        )
        
        if result["success"]:
            # 이미지 파일을 static 폴더에 저장
            static_dir = "static/images"
            os.makedirs(static_dir, exist_ok=True)
            
            filepath = os.path.join(static_dir, result["filename"])
            with open(filepath, "wb") as f:
                f.write(result["image_data"])
            
            # URL 생성
            image_url = f"/static/images/{result['filename']}"
            
            return ImageGenerationResponse(
                success=True,
                image_url=image_url,
                filename=result["filename"],
                prompt=result["prompt"]
            )
        else:
            return ImageGenerationResponse(
                success=False,
                prompt=request.prompt,
                error=result["error"]
            )
            
    except Exception as e:
        return ImageGenerationResponse(
            success=False,
            prompt=request.prompt,
            error=f"이미지 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/image/{filename}")
async def get_image(filename: str):
    """생성된 이미지 파일 제공"""
    try:
        filepath = f"static/images/{filename}"
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Image not found")
        
        with open(filepath, "rb") as f:
            image_data = f.read()
        
        # 파일 확장자에 따른 content type 결정
        if filename.endswith('.png'):
            media_type = "image/png"
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            media_type = "image/jpeg"
        else:
            media_type = "application/octet-stream"
        
        return Response(content=image_data, media_type=media_type)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hashtags", response_model=HashtagResponse)
async def generate_hashtags(
    request: HashtagGenerationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    해시태그 생성
    
    주어진 콘텐츠와 비즈니스 정보를 바탕으로 관련 해시태그를 생성합니다.
    """
    try:
        business_info = {
            "name": request.business_name,
            "category": request.business_category
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


@router.post("/keywords", response_model=KeywordAnalysisResponse)
async def analyze_keywords(
    request: KeywordAnalysisRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    키워드 분석
    
    주어진 텍스트에서 핵심 키워드를 추출합니다.
    """
    try:
        keywords = await ai_service.analyze_keywords(request.text)
        
        return KeywordAnalysisResponse(
            keywords=keywords,
            analyzed_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"키워드 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/performance", response_model=PerformanceMetricsResponse)
async def measure_performance(
    request: PerformanceTestRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    AI 모델 성능 측정
    
    지정된 모델의 성능을 측정합니다.
    """
    try:
        import time
        import psutil
        import os
        
        # 성능 측정 시작
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # AI 모델 호출 (단순한 콘텐츠 생성으로 테스트)
        business_info = {
            "name": "테스트 비즈니스",
            "product": {"name": "테스트 상품", "description": "테스트 설명"}
        }
        
        result = await ai_service.generate_content(
            business_info=business_info,
            content_type="blog"
        )
        
        # 성능 측정 종료
        end_time = time.time()
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        inference_time = (end_time - start_time) * 1000  # ms
        memory_usage = end_memory - start_memory
        
        # 토큰 수 계산 (대략적)
        token_count = len(result.get("content", "").split()) if result else 0
        
        return PerformanceMetricsResponse(
            model_name=request.model_name,
            inference_time_ms=inference_time,
            memory_usage_mb=memory_usage,
            token_count=token_count,
            quality_score=0.85,  # 임시 점수
            measured_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"성능 측정 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/models", response_model=AvailableModelsResponse)
async def get_available_models(
    ai_service: AIService = Depends(get_ai_service)
):
    """
    사용 가능한 AI 모델 목록 조회
    
    현재 사용 가능한 모든 AI 모델의 목록을 반환합니다.
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
    콘텐츠 타입별 템플릿 및 가이드라인 조회
    
    각 플랫폼에 최적화된 콘텐츠 작성 가이드라인을 제공합니다.
    """
    templates = {
        "blog": {
            "title_format": "[키워드] + [감정어] + [업종/지역]",
            "structure": [
                "후킹 제목과 인트로",
                "문제 제기 및 공감대 형성",
                "해결책 제시 (상품/서비스 소개)",
                "구체적인 혜택 및 특징",
                "고객 후기 또는 사례",
                "행동 유도 (CTA)"
            ],
            "recommended_length": "1000-1500자",
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
            "title_format": "[후킹] + [키워드] + [감정어]",
            "structure": [
                "강력한 후킹 (첫 3초)",
                "문제 상황 제시",
                "해결책 소개",
                "실제 시연 또는 설명",
                "마무리 및 구독 유도"
            ],
            "recommended_length": "30-60초 스크립트",
            "engagement_tips": ["질문으로 시작", "스토리텔링 활용", "명확한 CTA"]
        },
        "flyer": {
            "title_format": "[큰 할인율] + [상품명] + [긴급성]",
            "structure": [
                "강력한 헤드라인",
                "주요 혜택 (3-5개)",
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

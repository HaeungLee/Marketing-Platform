"""
간단한 콘텐츠 생성 서버 - 테스트용
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uvicorn

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

@app.post("/api/v1/content/generate", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    """
    마케팅 콘텐츠 생성 - 기본 응답 (API 연결 테스트용)
    """
    try:
        # 기본 응답 생성
        if request.content_type == "blog":
            title = f"{request.business_name}의 {request.product_name} 완벽 가이드"
            content = f"""
{request.business_name}에서 자신 있게 추천하는 {request.product_name}을 소개합니다.

## {request.product_name}의 특별한 장점

{request.product_description}

저희 {request.business_name}은 {request.business_category} 분야에서 오랜 경험을 바탕으로 고객 여러분께 최고의 서비스를 제공하고 있습니다.

## 왜 {request.product_name}을 선택해야 할까요?

1. **뛰어난 품질**: 엄선된 재료와 기술로 제작
2. **합리적인 가격**: 최고의 가성비 제공
3. **신뢰할 수 있는 서비스**: 고객 만족을 최우선으로

{request.tone} 톤으로 고객과 소통하며, 언제나 최선을 다하겠습니다.

더 자세한 정보는 언제든 문의해 주세요!
"""
        elif request.content_type == "instagram":
            title = f"{request.product_name} 소개"
            content = f"""
✨ {request.business_name}의 특별한 {request.product_name}을 만나보세요! ✨

{request.product_description}

💫 {request.business_category} 전문가가 추천하는 특별한 경험
🌟 고객 만족도 1위의 {request.business_name}
💝 지금 바로 경험해보세요!

더 많은 정보가 궁금하시다면 DM 또는 댓글로 문의해 주세요 💌

#문의환영 #최고품질 #고객만족 #{request.business_name.replace(' ', '')}
"""
        elif request.content_type == "youtube":
            title = f"{request.product_name} 리뷰 및 추천"
            content = f"""
안녕하세요! {request.business_name}입니다.

오늘은 저희가 자신 있게 추천하는 {request.product_name}에 대해 소개해드리려고 합니다.

{request.product_description}

이 영상에서는:
- {request.product_name}의 주요 특징
- 실제 고객 후기
- 사용법 및 팁
- Q&A 시간

{request.business_category} 분야에서 오랜 경험을 가진 저희 {request.business_name}이 직접 테스트하고 검증한 내용들을 공유해드립니다.

영상 끝까지 시청해주시고, 궁금한 점이 있으시면 댓글로 남겨주세요!

좋아요와 구독 잊지 마세요! 🔔
"""
        else:
            title = f"{request.product_name} 소개"
            content = f"{request.business_name}의 {request.product_name}을 소개합니다. {request.product_description}"

        # 기본 해시태그
        hashtags = [
            request.business_name.replace(" ", ""),
            request.product_name.replace(" ", ""),
            request.business_category.replace(" ", ""),
            "마케팅", "추천", "좋아요", "팔로우", "문의환영"
        ]

        # 기본 키워드
        keywords = [
            request.business_name,
            request.product_name,
            request.business_category,
            "품질", "서비스"
        ]

        return ContentGenerationResponse(
            content_id=f"content-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            content_type=request.content_type,
            title=title,
            content=content,
            hashtags=hashtags[:8],  # 최대 8개
            keywords=keywords[:5],  # 최대 5개
            estimated_engagement="높음",
            performance_metrics={
                "estimated_read_time": len(content) // 200,
                "character_count": len(content),
                "word_count": len(content.split())
            },
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
    return {"message": "Content Generation API is running", "status": "OK"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "content-generation", "model": "basic-template"}

if __name__ == "__main__":
    print("Content Generation API 서버를 시작합니다...")
    print("API URL: http://localhost:8001/api/v1/content/generate")
    print("Health Check: http://localhost:8001/health")
    uvicorn.run(app, host="0.0.0.0", port=8001)

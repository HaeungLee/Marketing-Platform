"""
AI 상담 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from src.application.services.ai_consultant_service import AIConsultantService

router = APIRouter(prefix="/consultation", tags=["AI 상담"])

# AI 상담 서비스 인스턴스
consultant_service = None

def get_consultant_service() -> AIConsultantService:
    """AI 상담 서비스 인스턴스 반환"""
    global consultant_service
    if consultant_service is None:
        # GOOGLE_API_KEY 또는 GOOGLE_AI_API_KEY 환경 변수 확인
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_AI_API_KEY")
        if not api_key:
            # settings에서 기본값 가져오기
            from src.config.settings import settings
            api_key = settings.google_api_key
            
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="Google AI API 키가 설정되지 않았습니다."
            )
        consultant_service = AIConsultantService(api_key)
    return consultant_service


class ConsultationRequest(BaseModel):
    """상담 요청 모델"""
    question: str
    business_type: Optional[str] = None
    region: Optional[str] = None  
    budget: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ConsultationResponse(BaseModel):
    """상담 응답 모델"""
    answer: str
    context: str
    question: str
    timestamp: str
    fallback: Optional[bool] = False


@router.post("/ask", response_model=ConsultationResponse)
async def ask_consultation(
    request: ConsultationRequest,
    service: AIConsultantService = Depends(get_consultant_service)
):
    """AI 상담 질문"""
    try:
        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="질문을 입력해주세요."
            )
        
        # AI 상담 서비스 호출
        result = await service.get_consultation(
            question=request.question,
            business_type=request.business_type,
            region=request.region,
            budget=request.budget,
            context=request.context
        )
        
        return ConsultationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"상담 API 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="상담 서비스에 일시적인 문제가 발생했습니다."
        )


@router.get("/health")
async def health_check():
    """상담 서비스 상태 확인"""
    try:
        service = get_consultant_service()
        return {
            "status": "healthy",
            "service": "AI 상담 서비스",
            "timestamp": service._get_current_timestamp()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"상담 서비스 오류: {str(e)}"
        )


@router.get("/topics")
async def get_consultation_topics():
    """상담 가능한 주제 목록"""
    return {
        "topics": [
            {
                "category": "상권 분석",
                "keywords": ["상권", "입지", "유동인구", "임대료", "접근성"],
                "description": "상권 분석 및 최적 입지 선정 도움"
            },
            {
                "category": "창업 전략", 
                "keywords": ["창업", "사업계획", "자금조달", "시장조사"],
                "description": "창업 준비부터 실행까지 단계별 가이드"
            },
            {
                "category": "마케팅",
                "keywords": ["마케팅", "홍보", "고객", "온라인", "SNS"],
                "description": "효과적인 마케팅 전략 및 실행 방안"
            },
            {
                "category": "정부 지원",
                "keywords": ["지원사업", "정책자금", "보조금", "융자"],
                "description": "정부 및 지자체 지원사업 정보"
            },
            {
                "category": "경영 개선",
                "keywords": ["경영", "수익", "비용", "효율", "개선"],
                "description": "경영 진단 및 수익성 향상 방안"
            }
        ]
    }

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
class SimpleContentGenerationRequest(BaseModel):
    prompt: str = Field(..., description="콘텐츠 생성을 위한 프롬프트")
    content_type: Optional[str] = Field("blog", description="콘텐츠 타입 (blog, instagram, youtube, flyer)", pattern="^(blog|instagram|youtube|flyer)$")
    tone: Optional[str] = Field("친근한", description="톤 앤 매너 (친근한, 전문적인, 캐주얼한, 공식적인)")
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
    try:
        return GeminiService()
    except Exception as e:
        print(f"GeminiService initialization error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI 서비스 초기화 실패: {str(e)}"
        )


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


@router.post("/test-ai")
async def test_ai_service(ai_service: AIService = Depends(get_ai_service)):
    """
    AI 서비스 테스트 엔드포인트
    """
    try:
        test_prompt = "안녕하세요. 간단한 응답을 해주세요."
        response = await ai_service.generate_text(test_prompt)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI 서비스 테스트 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/generate/simple", response_model=ContentGenerationResponse)
async def generate_simple_content(
    request: SimpleContentGenerationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    간단한 프롬프트로 콘텐츠 생성
    하나의 프롬프트로 마케팅 콘텐츠를 빠르게 생성합니다.
    """
    try:
        # API 키 가져오기
        from src.config.settings import settings
        api_key = os.getenv("GOOGLE_API_KEY", settings.google_api_key)
        if not api_key:
            raise ValueError("Google API key is not configured")

        # content_type과 tone에 기본값 설정
        content_type = request.content_type or "blog"
        tone = request.tone or "친근한"

        # 톤에 따른 스타일 가이드라인
        style_guidance = {
            "친근한": "Use casual, friendly language with emojis and personal pronouns like '우리', '이거 어때요?'",
            "전문적인": "Use formal, professional language with industry-specific terms and structured paragraphs",
            "캐주얼한": "Use slang and informal expressions, similar to social media posts",
            "공식적인": "Use highly formal language suitable for corporate reports or official announcements"
        }

        # 콘텐츠 타입에 따른 형식 가이드라인
        format_guidance = {
            "blog": "Include a title, introduction, body with bullet points or examples, and a conclusion. Around 500-700 words.",
            "instagram": "Short, catchy text with emojis and hashtags. Include CTA like 'DM me' or 'Click the link'.",
            "youtube": "Script-style structure: Hook in first sentence, explanation, call-to-action at the end.",
            "flyer": "Concise, eye-catching text with clear benefits, prices, and contact information."
        }

        # 시스템 메시지 구성
        system_message = f"""
You are a marketing content expert specialized in creating high-engagement content.
Please follow these instructions carefully:

- Content Type: {content_type}
- Tone & Manner: {tone}

Guidelines:
1. Use the '{tone}' tone: {style_guidance.get(tone, "Standard tone")}
2. Follow the '{content_type}' format: {format_guidance.get(content_type, "Standard format")}
3. Keep it engaging and persuasive
4. Include appropriate calls-to-action when needed
5. Make sure the length is suitable for the platform

Output should be well-structured and ready for immediate use.
"""

        user_prompt = f"""
User Request:
{request.prompt}
"""

        full_prompt = system_message + "\n\n" + user_prompt

        # 실행 시간 측정 시작
        start_time = time.time()
        try:
            # Google Generative AI 라이브러리 불러오기
            import google.generativeai as genai
            # Google Generative AI 설정
            genai.configure(api_key=api_key)
            # 모델 설정 (gemma-3-27b-it 사용)
            model = genai.GenerativeModel('gemma-3-27b-it')
            # 모델 호출
            response = model.generate_content(full_prompt)
            # 응답 텍스트 추출
            content_text = response.text if hasattr(response, 'text') else ""
            if not content_text:
                raise ValueError("AI 모델에서 콘텐츠를 생성하지 못했습니다.")
        except ImportError:
            # 대체 방법으로 시도
            try:
                from google import genai
                # 클라이언트 초기화
                client = genai.Client(api_key=api_key)
                # Gemini 모델 호출
                response = client.models.generate_content(
                    model="gemma-3-27b-it",
                    contents=full_prompt
                )
                # 응답 처리
                content_text = ""
                if hasattr(response, 'candidates') and response.candidates:
                    if hasattr(response.candidates[0], 'content') and hasattr(response.candidates[0].content, 'parts'):
                        for part in response.candidates[0].content.parts:
                            if hasattr(part, 'text') and part.text:
                                content_text += part.text
                if not content_text:
                    raise ValueError("AI 모델에서 콘텐츠를 생성하지 못했습니다.")
            except ImportError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Google Generative AI 라이브러리를 불러올 수 없습니다. 'pip install google-generativeai'를 설치해야 합니다. 오류: {str(e)}"
                )

        # 실행 시간 측정 종료
        end_time = time.time()
        generation_time = end_time - start_time

        # 제목과 내용 분리
        lines = content_text.strip().split('\n')
        title = lines[0] if lines else "생성된 콘텐츠"
        content = "\n".join(lines[1:]) if len(lines) > 1 else content_text

        # AI를 활용한 해시태그 생성
        try:
            hashtag_prompt = f"""
            다음 콘텐츠에 어울리는 해시태그 5개를 생성해주세요.
            콘텐츠 타입: {content_type}
            톤: {tone}
            콘텐츠: {content_text[:500]}  # 내용이 길 경우 앞부분만 사용
            
            - 해시태그는 '#'으로 시작하는 단어로 만들어주세요.
            - 인기 있는 해시태그 위주로 생성해주세요.
            - 콤마로 구분된 문자열로 반환해주세요.
            예시: #마케팅 #콘텐츠 #SNS #홍보 #인스타그램
            """
            
            # 해시태그 생성 요청
            hashtag_response = model.generate_content(hashtag_prompt)
            hashtags_text = hashtag_response.text.strip()
            
            # 생성된 해시태그 파싱
            if hashtags_text:
                # 쉼표나 공백으로 구분하여 리스트로 변환
                generated_hashtags = [tag.strip() for tag in hashtags_text.replace('#', ' #').split() if tag.startswith('#')]
                # 중복 제거
                generated_hashtags = list(dict.fromkeys(generated_hashtags))
                # 최대 5개로 제한
                default_hashtags = generated_hashtags[:5]
            else:
                default_hashtags = ["#마케팅", "#콘텐츠", f"#{content_type}", f"#{tone}"]
                
        except Exception as e:
            print(f"해시태그 생성 중 오류: {str(e)}")
            default_hashtags = ["#마케팅", "#콘텐츠", f"#{content_type}", f"#{tone}"]
            
        keywords = ["마케팅", "콘텐츠", content_type, tone]

        # 결과 반환
        return ContentGenerationResponse(
            content_id=f"simple-content-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            content_type=content_type,
            title=title,
            content=content,
            hashtags=default_hashtags,
            keywords=keywords,
            performance_metrics={
                "generation_time": round(generation_time, 2),
                "word_count": len(content_text.split())
            },
            created_at=datetime.now()
        )
    except Exception as e:
        # 상세한 오류 로깅
        print(f"콘텐츠 생성 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        # 클라이언트에게 오류 정보 반환
        raise HTTPException(
            status_code=500,
            detail=f"콘텐츠 생성 중 오류가 발생했습니다: {str(e)}"
        )

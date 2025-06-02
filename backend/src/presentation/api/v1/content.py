from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from infrastructure.ai.gemini_service import GeminiService

router = APIRouter()
gemini_service = GeminiService()

class ContentRequest(BaseModel):
    prompt: str

class ContentResponse(BaseModel):
    content: str

@router.post("/generate")
async def generate_content(request: ContentRequest):
    """콘텐츠 생성 엔드포인트"""
    try:
        result = await gemini_service.generate_content(request.prompt)
        return {"content": result["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

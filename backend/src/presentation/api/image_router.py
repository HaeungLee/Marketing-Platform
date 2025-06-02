from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.domain.services.image_service import image_service

router = APIRouter(prefix="/api/images", tags=["images"])

class ImageGenerationRequest(BaseModel):
    prompt: str

class ImageGenerationResponse(BaseModel):
    image_data: str | None

@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    프롬프트를 기반으로 이미지를 생성합니다.
    """
    try:
        image_data = await image_service.generate_image(request.prompt)
        if not image_data:
            raise HTTPException(status_code=500, detail="이미지 생성에 실패했습니다.")
        
        return ImageGenerationResponse(image_data=image_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 생성 중 오류 발생: {str(e)}") 
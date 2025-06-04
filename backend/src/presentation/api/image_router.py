from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.infrastructure.ai.gemini_image_service import GeminiImageService
import os

router = APIRouter(prefix="/api/images", tags=["images"])

# GeminiImageService 인스턴스 생성
image_service = GeminiImageService(api_key="AIzaSyDrPzr9VvEUGVU6a87DxyTQNs17_wldqBE")

class ImageGenerationRequest(BaseModel):
    prompt: str
    business_name: Optional[str] = ""
    business_category: Optional[str] = ""

class ImageGenerationResponse(BaseModel):
    success: bool
    filename: Optional[str] = ""
    url: Optional[str] = ""
    file_size: Optional[int] = 0
    message: Optional[str] = ""
    image_data: Optional[str] = ""  # Base64 인코딩된 이미지 데이터

@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    프롬프트를 기반으로 이미지를 생성합니다.
    """
    try:
        business_info = {
            "name": request.business_name,
            "category": request.business_category
        }
        result = await image_service.generate_image(request.prompt, business_info)
        
        if result["success"]:
            return ImageGenerationResponse(
                success=True,
                filename=result["filename"],
                url=result["url"],
                file_size=result["file_size"],
                message=f"이미지가 성공적으로 생성되었습니다. (크기: {result['file_size']:,} bytes)",
                image_data=result.get("image_data", "")  # Base64 이미지 데이터 추가
            )
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 생성 중 오류 발생: {str(e)}")

@router.get("/file/{filename}")
async def get_image_file(filename: str):
    """생성된 이미지 파일 제공"""
    file_path = os.path.join("static", "images", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")
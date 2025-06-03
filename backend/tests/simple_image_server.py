#!/usr/bin/env python3
"""
Simple Image Generation Server
gemini_test.py 형식을 기반으로 한 간단한 이미지 생성 API
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai.types import GenerateContentConfig, Modality
import base64
import os
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple Image Generation API")

# CORS 설정 (프론트엔드 연결용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# static 폴더 마운트
if not os.path.exists("static/images"):
    os.makedirs("static/images")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Gemini 클라이언트 초기화
client = genai.Client(api_key="AIzaSyDrPzr9VvEUGVU6a87DxyTQNs17_wldqBE")

class ImageRequest(BaseModel):
    prompt: str
    business_name: str = ""
    business_category: str = ""

class ImageResponse(BaseModel):
    success: bool
    filename: str = ""
    url: str = ""
    message: str = ""

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Simple Image Generation API is running"}

@app.post("/generate-image", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    """gemini_test.py 형식으로 이미지 생성"""
    
    try:
        logger.info(f"이미지 생성 요청: {request.prompt}")
        
        # 비즈니스 정보가 있으면 프롬프트에 추가
        enhanced_prompt = request.prompt
        if request.business_name or request.business_category:
            enhanced_prompt = f"Create a professional flyer image for {request.business_name} ({request.business_category}): {request.prompt}"
        
        logger.info(f"강화된 프롬프트: {enhanced_prompt}")
        
        # Gemini API 호출 (gemini_test.py와 동일한 방식)
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=enhanced_prompt,
            config=GenerateContentConfig(
                response_modalities=[Modality.TEXT, Modality.IMAGE]
            )
        )
        
        # 응답에서 이미지 데이터 추출
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                logger.info(f"이미지 데이터 타입: {part.inline_data.mime_type}")
                
                # gemini_test.py와 동일한 로직
                raw_data = part.inline_data.data
                logger.info(f"원본 데이터 타입: {type(raw_data)}, 길이: {len(raw_data)}")
                
                # bytes 타입이면 그대로, str 타입이면 base64 디코딩
                if isinstance(raw_data, bytes):
                    image_data = raw_data
                else:
                    image_data = base64.b64decode(raw_data)
                
                logger.info(f"디코딩된 이미지 크기: {len(image_data)} bytes")
                
                # 파일 헤더 확인하여 확장자 결정
                filename = f"generated_image_{int(time.time())}"
                if len(image_data) >= 8:
                    header = image_data[:8]
                    if header.startswith(b'\x89PNG'):
                        filename += ".png"
                    elif header.startswith(b'\xFF\xD8\xFF'):
                        filename += ".jpg"
                    else:
                        filename += ".png"  # 기본값
                else:
                    filename += ".png"
                
                # 파일 저장
                file_path = os.path.join("static", "images", filename)
                with open(file_path, "wb") as f:
                    f.write(image_data)
                
                file_size = os.path.getsize(file_path)
                logger.info(f"이미지가 {file_path}로 저장되었습니다. (크기: {file_size} bytes)")
                
                return ImageResponse(
                    success=True,
                    filename=filename,
                    url=f"/static/images/{filename}",
                    message=f"이미지가 성공적으로 생성되었습니다. (크기: {file_size:,} bytes)"
                )
        
        # 이미지가 없는 경우
        raise HTTPException(status_code=500, detail="생성된 응답에 이미지가 없습니다.")
        
    except Exception as e:
        logger.error(f"이미지 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"이미지 생성 실패: {str(e)}")

@app.get("/image/{filename}")
async def get_image(filename: str):
    """생성된 이미지 파일 제공"""
    file_path = os.path.join("static", "images", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")

if __name__ == "__main__":
    import uvicorn
    logger.info("Simple Image Generation Server 시작...")
    uvicorn.run(app, host="0.0.0.0", port=8001)

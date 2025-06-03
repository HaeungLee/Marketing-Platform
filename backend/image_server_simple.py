#!/usr/bin/env python3
"""
gemini_test.py 기반 간단한 이미지 생성 서버
"""
from fastapi import FastAPI, HTTPException
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

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini 클라이언트 초기화
client = genai.Client(api_key="AIzaSyDrPzr9VvEUGVU6a87DxyTQNs17_wldqBE")

class ImageRequest(BaseModel):
    prompt: str

class ImageResponse(BaseModel):
    success: bool
    filename: str = ""
    url: str = ""
    file_size: int = 0
    message: str = ""
    image_data: str = ""  # Base64 인코딩된 이미지 데이터

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Simple Image Generation API is running"}

@app.post("/api/images/generate", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    """gemini_test.py 형식으로 이미지 생성"""
    
    try:
        logger.info(f"이미지 생성 요청: {request.prompt}")
        
        # gemini_test.py와 동일한 방식으로 Gemini API 호출
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=request.prompt,
            config=GenerateContentConfig(
                response_modalities=[Modality.TEXT, Modality.IMAGE]
            )
        )
        
        # 응답에서 이미지 데이터 추출 (gemini_test.py와 동일한 로직)
        for part in response.candidates[0].content.parts:
            if part.text:
                logger.info(f"텍스트 응답: {part.text}")
            elif part.inline_data:
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
                        logger.info("PNG 헤더 감지")
                    elif header.startswith(b'\xFF\xD8\xFF'):
                        filename += ".jpg"
                        logger.info("JPEG 헤더 감지")
                    else:
                        filename += ".png"  # 기본값
                        logger.info("알 수 없는 형식, PNG로 저장")
                else:
                    filename += ".png"
                
                # Base64 인코딩하여 프론트엔드에 전달
                image_data_b64 = base64.b64encode(image_data).decode('utf-8')
                
                logger.info(f"이미지 생성 완료: {filename}")
                
                return ImageResponse(
                    success=True,
                    filename=filename,
                    url=f"/static/images/{filename}",
                    file_size=len(image_data),
                    message=f"이미지가 성공적으로 생성되었습니다. (크기: {len(image_data):,} bytes)",
                    image_data=image_data_b64
                )
        
        # 이미지가 없는 경우
        raise HTTPException(status_code=500, detail="생성된 응답에 이미지가 없습니다.")
        
    except Exception as e:
        logger.error(f"이미지 생성 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"이미지 생성 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Simple Image Generation Server 시작...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

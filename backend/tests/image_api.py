"""
단순한 이미지 생성 API 서버
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import base64
import os
import time

app = FastAPI(title="Marketing Platform - Image Generation API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (이미지)
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Request Models
class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="이미지 생성 프롬프트")
    business_name: Optional[str] = Field(None, description="비즈니스명")
    business_category: Optional[str] = Field(None, description="비즈니스 카테고리")
    style: Optional[str] = Field("professional", description="이미지 스타일")

# Response Models
class ImageGenerationResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    filename: Optional[str] = None
    prompt: str
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class SimpleGeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._setup_client()
    
    def _setup_client(self):
        """Gemini 클라이언트 설정"""
        try:
            from google import genai
            from google.genai.types import GenerateContentConfig, Modality
            self.genai = genai
            self.GenerateContentConfig = GenerateContentConfig
            self.Modality = Modality
            self.client = genai.Client(api_key=self.api_key)
            print("✅ Gemini 클라이언트 초기화 성공")
        except ImportError as e:
            print(f"❌ google-genai 패키지 import 실패: {e}")
            raise
        except Exception as e:
            print(f"❌ Gemini 클라이언트 초기화 실패: {e}")
            raise
    
    def generate_image(self, prompt: str, business_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """이미지 생성 (동기 버전)"""
        try:
            print(f"🎨 이미지 생성 시작: {prompt[:50]}...")
            
            # 이미지 생성용 프롬프트 개선
            enhanced_prompt = prompt
            if business_info:
                business_name = business_info.get("name", "")
                category = business_info.get("category", "")
                if business_name:
                    enhanced_prompt += f"\n\n비즈니스 컨텍스트: {business_name}"
                if category:
                    enhanced_prompt += f" ({category})"
                enhanced_prompt += "\n고품질, 전문적인, 마케팅에 적합한 이미지"
            
            enhanced_prompt += "\n\nStyle: Professional, high-quality, marketing-ready"
            enhanced_prompt += "\nResolution: High resolution, crisp details"
            enhanced_prompt += "\nComposition: Well-balanced, visually appealing"
            
            print(f"📝 향상된 프롬프트: {enhanced_prompt}")
              # Gemini 2.0 Flash Image Generation 모델 사용
            print("🚀 Gemini API 호출 중...")
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",  # 이미지 생성 전용 모델
                contents=enhanced_prompt,
                config=self.GenerateContentConfig(
                    response_modalities=[self.Modality.TEXT, self.Modality.IMAGE]
                )
            )
            
            print("📦 응답 처리 중...")
            
            # 응답에서 이미지 데이터 추출
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    print("🖼️ 이미지 데이터 발견, 처리 중...")
                    image_data = self._process_image_data(part.inline_data)
                    return {
                        "success": True,
                        "image_data": image_data["data"],
                        "image_type": image_data["type"],
                        "filename": image_data["filename"],
                        "prompt": enhanced_prompt
                    }
            
            # 텍스트 응답만 있는 경우
            print("📝 텍스트 응답만 수신됨")
            text_content = ""
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text'):
                    text_content += part.text
            
            return {
                "success": False,
                "error": f"이미지가 생성되지 않았습니다. 응답: {text_content[:200]}..."
            }
            
        except Exception as e:
            print(f"❌ Gemini 이미지 생성 오류: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"이미지 생성 중 오류가 발생했습니다: {str(e)}"
            }
    
    def _process_image_data(self, inline_data) -> Dict[str, Any]:
        """이미지 데이터 처리"""
        try:
            # 원본 데이터 타입 확인
            raw_data = inline_data.data
            mime_type = inline_data.mime_type
            
            print(f"📊 이미지 데이터 타입: {type(raw_data)}, MIME: {mime_type}")
            
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
            
            print(f"✅ 이미지 데이터 처리 완료: {len(image_data)} bytes, {filename}")
            
            return {
                "data": image_data,
                "type": mime_type,
                "filename": filename
            }
            
        except Exception as e:
            print(f"❌ 이미지 데이터 처리 오류: {e}")
            raise Exception(f"이미지 데이터 처리 오류: {str(e)}")

# 글로벌 Gemini 서비스 인스턴스
gemini_service = None

def get_gemini_service():
    """Gemini 서비스 의존성 주입"""
    global gemini_service
    if gemini_service is None:
        api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyDrPzr9VvEUGVU6a87DxyTQNs17_wldqBE")
        try:
            gemini_service = SimpleGeminiService(api_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini 서비스 초기화 실패: {str(e)}")
    return gemini_service

@app.get("/")
async def root():
    return {"message": "Marketing Platform Image Generation API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/v1/content/generate-image", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    AI 이미지 생성
    
    주어진 프롬프트를 바탕으로 마케팅에 적합한 이미지를 생성합니다.
    """
    try:
        print(f"🎯 이미지 생성 요청: {request.prompt}")
        
        # Gemini 서비스 가져오기
        service = get_gemini_service()
        
        business_info = {
            "name": request.business_name,
            "category": request.business_category
        }
        
        # 이미지 생성 (동기 호출)
        result = service.generate_image(
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
            
            print(f"💾 이미지 파일 저장: {filepath}")
            
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
        print(f"❌ 이미지 생성 API 오류: {e}")
        import traceback
        traceback.print_exc()
        return ImageGenerationResponse(
            success=False,
            prompt=request.prompt,
            error=f"이미지 생성 중 오류가 발생했습니다: {str(e)}"
        )

@app.get("/api/v1/content/image/{filename}")
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

@app.get("/api/v1/content/test")
async def test_endpoint():
    """테스트 엔드포인트"""
    return {"message": "Content API is working!", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

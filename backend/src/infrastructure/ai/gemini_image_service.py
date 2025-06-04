"""
Google Gemini AI 이미지 생성 서비스 (google-genai 패키지 사용)
"""
import base64
import os
import time
from typing import Dict, Any
from google import genai
from google.genai.types import GenerateContentConfig, Modality


class GeminiImageService:
    """Google Gemini를 사용한 이미지 생성 서비스"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        
        # 이미지 저장 디렉토리 생성
        self.images_dir = os.path.join("static", "images")
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
    
    async def generate_image(self, prompt: str, business_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """이미지 생성"""
        try:
            # 이미지 생성용 프롬프트 개선
            enhanced_prompt = self._enhance_image_prompt(prompt, business_info)
            
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
                    
                    # 파일 저장
                    file_path = os.path.join(self.images_dir, image_data["filename"])
                    with open(file_path, "wb") as f:
                        f.write(image_data["data"])
                    
                    file_size = os.path.getsize(file_path)
                    return {
                        "success": True,
                        "filename": image_data["filename"],
                        "url": f"/static/images/{image_data['filename']}",
                        "file_size": file_size,
                        "image_type": image_data["type"],
                        "prompt": enhanced_prompt,
                        "image_data": base64.b64encode(image_data["data"]).decode('utf-8')  # Base64 인코딩된 이미지 데이터 추가
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
    
    def _enhance_image_prompt(self, prompt: str, business_info: Dict[str, Any] = None) -> str:
        """이미지 생성용 프롬프트 개선"""
        enhanced_prompt = prompt
        
        if business_info:
            business_name = business_info.get("name", "")
            category = business_info.get("category", "")
            
            # 비즈니스 정보를 바탕으로 프롬프트 개선
            if business_name or category:
                enhanced_prompt = f"Create a professional flyer image for {business_name} ({category}): {prompt}"
        
        # 기본 품질 지시사항 추가
        enhanced_prompt += "\n\nStyle: Professional, high-quality, marketing-ready"
        enhanced_prompt += "\nResolution: High resolution, crisp details"
        enhanced_prompt += "\nComposition: Well-balanced, visually appealing"
        
        return enhanced_prompt
    
    async def close(self):
        """리소스 정리"""
        # Google Genai 클라이언트는 별도 종료 작업이 필요하지 않음
        pass

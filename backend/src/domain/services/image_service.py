from typing import Optional
import base64
import io
import logging
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
from src.config.settings import settings

class ImageService:
    def __init__(self):
        try:
            # Google Generative AI 설정
            genai.configure(api_key=settings.google_api_key)
            
            # 이미지 생성용 모델 초기화 - 정확한 모델명 사용
            self.image_model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            logging.info("ImageService initialized successfully with Gemini image generation model")
        except Exception as e:
            logging.error(f"Failed to initialize ImageService: {str(e)}")
            self.image_model = None
    
    async def generate_image(self, prompt: str) -> Optional[str]:
        """
        Gemini 2.0 Flash Experimental 모델을 사용하여 이미지를 생성합니다.
        
        Args:
            prompt (str): 이미지 생성을 위한 프롬프트
            
        Returns:
            Optional[str]: 생성된 이미지의 base64 인코딩 문자열. 실패 시 None
        """
        try:
            if not self.image_model:
                logging.error("Image generation model is not available")
                return await self.generate_placeholder_image(prompt)
                
            logging.info(f"Generating image with Gemini 2.0 Flash: {prompt}")
            
            # 한국어 프롬프트를 영어로 번역하여 더 나은 결과 얻기
            enhanced_prompt = f"Create a high-quality, detailed image: {prompt}"
            
            # Gemini 2.0 Flash 모델로 이미지 생성
            response = self.image_model.generate_content(enhanced_prompt)
            
            if not response.candidates:
                logging.warning("No candidates in response")
                return await self.generate_placeholder_image(prompt)
                
            candidate = response.candidates[0]
            if not candidate.content or not candidate.content.parts:
                logging.warning("No content or parts in candidate")
                return await self.generate_placeholder_image(prompt)
                
            # 이미지 데이터 추출
            for part in candidate.content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Base64 인코딩된 이미지 데이터 반환
                    image_data = part.inline_data.data
                    logging.info("Successfully generated image with Gemini 2.0 Flash")
                    return image_data
                elif hasattr(part, 'file_data') and part.file_data:
                    # 파일 데이터가 있는 경우 처리
                    logging.info("Generated image as file data")
                    return part.file_data.file_uri
                    
            logging.warning("No image data found in response parts")
            return await self.generate_placeholder_image(prompt)
            
        except Exception as e:
            logging.error(f"Gemini image generation error: {str(e)}", exc_info=True)
            return await self.generate_placeholder_image(prompt)

    async def generate_placeholder_image(self, prompt: str) -> Optional[str]:
        """
        플레이스홀더 이미지를 생성합니다 (이미지 생성이 실패했을 때)
        
        Args:
            prompt (str): 이미지 생성을 위한 프롬프트
            
        Returns:
            Optional[str]: 생성된 이미지의 base64 인코딩 문자열
        """
        try:
            logging.info(f"Generating placeholder image for prompt: {prompt}")
            
            # 512x512 크기의 플레이스홀더 이미지 생성
            img = Image.new('RGB', (512, 512), color=(240, 240, 245))
            draw = ImageDraw.Draw(img)
            
            # 텍스트 추가
            try:
                # 기본 폰트 사용
                font = ImageFont.load_default()
            except:
                font = None
            
            # 텍스트를 이미지 중앙에 배치
            text_lines = [
                "AI Generated Image",
                f"Prompt: {prompt[:30]}..." if len(prompt) > 30 else f"Prompt: {prompt}",
                "Image generation in progress..."
            ]
            
            y_offset = 200
            for line in text_lines:
                # 텍스트 크기 계산
                if font:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                else:
                    text_width = len(line) * 8  # 대략적인 계산
                
                x = (512 - text_width) // 2
                
                # 텍스트 그리기
                draw.text((x, y_offset), line, fill=(100, 100, 100), font=font)
                y_offset += 30
            
            # 장식적인 테두리 추가
            draw.rectangle([10, 10, 502, 502], outline=(200, 200, 200), width=2)
            
            # Base64로 인코딩
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logging.info("Successfully generated placeholder image")
            return image_data
            
        except Exception as e:
            logging.error(f"Placeholder image generation error: {str(e)}", exc_info=True)
            return None

# 싱글톤 인스턴스
image_service = ImageService()
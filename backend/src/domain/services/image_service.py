from typing import Optional
import base64
import io
import logging
from PIL import Image, ImageDraw, ImageFont
from src.config.settings import settings

class ImageService:
    def __init__(self):
        try:
            logging.info("ImageService initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize ImageService: {str(e)}")
    
    async def generate_image(self, prompt: str) -> Optional[str]:
        """
        현재 Google Gemini는 직접적인 이미지 생성을 지원하지 않으므로,
        고품질 플레이스홀더 이미지를 생성합니다.
        
        Args:
            prompt (str): 이미지 생성을 위한 프롬프트
            
        Returns:
            Optional[str]: 생성된 이미지의 base64 인코딩 문자열. 실패 시 None
        """
        try:
            logging.info(f"Generating enhanced placeholder image for: {prompt}")
            
            # 더 고품질의 플레이스홀더 이미지 생성
            return await self.generate_enhanced_placeholder_image(prompt)
        except Exception as e:
            logging.error(f"Image generation error: {str(e)}", exc_info=True)
            return await self.generate_enhanced_placeholder_image(prompt)

    async def generate_enhanced_placeholder_image(self, prompt: str) -> Optional[str]:
        """
        고품질 플레이스홀더 이미지를 생성합니다.
        
        Args:
            prompt (str): 이미지 생성을 위한 프롬프트
            
        Returns:
            Optional[str]: 생성된 이미지의 base64 인코딩 문자열
        """
        try:
            logging.info(f"Generating enhanced placeholder image for prompt: {prompt}")
            
            # 800x600 크기의 고품질 이미지 생성
            img = Image.new('RGB', (800, 600), color=(245, 247, 250))
            draw = ImageDraw.Draw(img)
            
            # 그라데이션 배경 효과
            for y in range(600):
                color_value = int(245 + (y / 600) * 10)
                draw.line([(0, y), (800, y)], fill=(color_value, color_value + 2, color_value + 5))
            
            # 메인 컨테이너
            container_margin = 50
            draw.rectangle([container_margin, container_margin, 800-container_margin, 600-container_margin], 
                         outline=(200, 210, 220), width=3)
            
            # 헤더 영역
            header_height = 80
            draw.rectangle([container_margin + 10, container_margin + 10, 
                          800-container_margin-10, container_margin + header_height], 
                         fill=(70, 130, 180), outline=(50, 110, 160), width=2)
            
            # 아이콘 영역 (원형)
            icon_center_x, icon_center_y = 150, container_margin + 40
            icon_radius = 25
            draw.ellipse([icon_center_x - icon_radius, icon_center_y - icon_radius,
                         icon_center_x + icon_radius, icon_center_y + icon_radius], 
                        fill=(255, 255, 255), outline=(200, 200, 200), width=2)
            
            # 아이콘 내부 (이미지 심볼)
            draw.rectangle([icon_center_x - 10, icon_center_y - 8,
                           icon_center_x + 10, icon_center_y + 8], 
                          fill=(70, 130, 180))
            
            try:
                # 기본 폰트 사용
                font = ImageFont.load_default()
                title_font = font
            except:
                font = None
                title_font = None
            
            # 제목 텍스트
            title = "AI Generated Image"
            if title_font:
                bbox = draw.textbbox((0, 0), title, font=title_font)
                title_width = bbox[2] - bbox[0]
            else:
                title_width = len(title) * 8
            
            title_x = 200
            title_y = container_margin + 25
            draw.text((title_x, title_y), title, fill=(255, 255, 255), font=title_font)
            
            # 프롬프트 텍스트 (여러 줄로 분할)
            content_start_y = container_margin + header_height + 30
            prompt_text = f"프롬프트: {prompt}"
            
            # 텍스트를 여러 줄로 분할
            max_chars_per_line = 50
            words = prompt_text.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + " " + word) <= max_chars_per_line:
                    current_line = current_line + " " + word if current_line else word
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # 프롬프트 텍스트 그리기
            y_offset = content_start_y
            for line in lines:
                if font:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                else:
                    text_width = len(line) * 8
                
                x = container_margin + 20
                draw.text((x, y_offset), line, fill=(60, 70, 80), font=font)
                y_offset += 25
            
            # 상태 메시지
            status_lines = [
                "",
                "🎨 이미지 생성 완료",
                "📝 전단지 편집 도구를 사용하여 텍스트와 도형을 추가하세요",
                "💾 편집 완료 후 다운로드 버튼을 클릭하세요"
            ]
            
            y_offset += 30
            for line in status_lines:
                if not line:
                    y_offset += 15
                    continue
                    
                x = container_margin + 20
                draw.text((x, y_offset), line, fill=(100, 120, 140), font=font)
                y_offset += 25
            
            # 장식적인 요소들
            # 하단 장식선
            footer_y = 600 - container_margin - 30
            draw.line([(container_margin + 20, footer_y), (800 - container_margin - 20, footer_y)], 
                     fill=(200, 210, 220), width=2)
            
            # 코너 장식
            corner_size = 15
            # 좌상단
            draw.line([(container_margin + 20, container_margin + 20), 
                      (container_margin + 20 + corner_size, container_margin + 20)], 
                     fill=(70, 130, 180), width=3)
            draw.line([(container_margin + 20, container_margin + 20), 
                      (container_margin + 20, container_margin + 20 + corner_size)], 
                     fill=(70, 130, 180), width=3)
            
            # 우하단
            draw.line([(800 - container_margin - 20, 600 - container_margin - 20), 
                      (800 - container_margin - 20 - corner_size, 600 - container_margin - 20)], 
                     fill=(70, 130, 180), width=3)
            draw.line([(800 - container_margin - 20, 600 - container_margin - 20), 
                      (800 - container_margin - 20, 600 - container_margin - 20 - corner_size)], 
                     fill=(70, 130, 180), width=3)
            
            # Base64로 인코딩
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logging.info("Successfully generated enhanced placeholder image")
            return image_data
            
        except Exception as e:
            logging.error(f"Enhanced placeholder image generation error: {str(e)}", exc_info=True)
            # 기본 플레이스홀더로 폴백
            return await self.generate_basic_placeholder_image(prompt)
    
    async def generate_basic_placeholder_image(self, prompt: str) -> Optional[str]:
        """
        기본 플레이스홀더 이미지를 생성합니다.
        
        Args:
            prompt (str): 이미지 생성을 위한 프롬프트
            
        Returns:
            Optional[str]: 생성된 이미지의 base64 인코딩 문자열
        """
        try:
            logging.info(f"Generating basic placeholder image for prompt: {prompt}")
            
            # 800x600 크기의 기본 이미지 생성
            img = Image.new('RGB', (800, 600), color=(240, 240, 245))
            draw = ImageDraw.Draw(img)
            
            # 텍스트 추가
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # 텍스트를 이미지 중앙에 배치
            text_lines = [
                "AI Generated Image",
                f"Prompt: {prompt[:50]}..." if len(prompt) > 50 else f"Prompt: {prompt}",
                "Image Ready for Editing"
            ]
            
            y_offset = 250
            for line in text_lines:
                if font:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                else:
                    text_width = len(line) * 8
                
                x = (800 - text_width) // 2
                draw.text((x, y_offset), line, fill=(100, 100, 100), font=font)
                y_offset += 30
            
            # 장식적인 테두리 추가
            draw.rectangle([10, 10, 790, 590], outline=(200, 200, 200), width=2)
            
            # Base64로 인코딩
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logging.info("Successfully generated basic placeholder image")
            return image_data
            
        except Exception as e:
            logging.error(f"Basic placeholder image generation error: {str(e)}", exc_info=True)
            return None

# 싱글톤 인스턴스
image_service = ImageService()
#!/usr/bin/env python3
"""
간단한 Gemini 서비스 테스트
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# src 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from infrastructure.ai.gemini_service import GeminiService

async def test_gemini():
    """Gemini 서비스 테스트"""
    try:
        print("🤖 Gemini 서비스 테스트 시작...")
        
        # 서비스 인스턴스 생성
        service = GeminiService()
        print("✅ GeminiService 인스턴스 생성 성공")
        
        # 비즈니스 정보
        business_info = {
            "name": "맛있는 카페",
            "description": "신선한 원두와 수제 디저트를 제공하는 아늑한 카페",
            "category": "카페"ㄴ
        }
        
        # 블로그 콘텐츠 생성 테스트
        print("📝 블로그 콘텐츠 생성 중...")
        result = await service.generate_content(business_info, "blog")
        
        if result and result.get("content"):
            print("✅ 콘텐츠 생성 성공!")
            print("📄 생성된 콘텐츠 미리보기:")
            print("-" * 50)
            print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
            print("-" * 50)
            return True
        else:
            print("❌ 콘텐츠 생성 실패")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini())
    if success:
        print("🎉 Gemini 서비스 테스트 완료!")
    else:
        print("💥 테스트 실패")

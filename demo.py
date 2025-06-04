#!/usr/bin/env python3
"""
Demo script for the AI Marketing Platform
This script demonstrates the key features of the platform
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from infrastructure.ai.gemini_service import GeminiService
from config.settings import settings

async def demo_ai_content_generation():
    """Demonstrate AI content generation capabilities"""
    print("🚀 AI 마케팅 플랫폼 데모 시작")
    print("=" * 50)
    
    # Initialize AI service
    ai_service = GeminiService()
    
    try:
        # Check available models
        print("📋 사용 가능한 AI 모델 확인 중...")
        models = await ai_service.get_available_models()
        if models:
            print(f"✅ 모델 발견: {', '.join(models)}")
        else:
            print("⚠️  사용 가능한 모델이 없습니다. Gemini API 키를 확인하세요.")
            return
        
        print("\n📝 AI 콘텐츠 생성 데모")
        print("-" * 30)
        
        # Demo content generation
        demo_prompts = [
            {
                "type": "블로그 포스트",
                "prompt": "수제 케이크 맛집에 대한 블로그 포스트를 작성해주세요. 특별한 할인 이벤트가 있습니다.",
                "max_tokens": 200
            },
            {
                "type": "인스타그램 캡션",
                "prompt": "카페 신메뉴 출시에 대한 인스타그램 캡션을 작성해주세요. 친근하고 매력적인 톤으로.",
                "max_tokens": 100
            }
        ]
        
        for i, demo in enumerate(demo_prompts, 1):
            print(f"\n{i}. {demo['type']} 생성 중...")
            try:
                result = await ai_service.generate_content(
                    prompt=demo['prompt'],
                    max_tokens=demo['max_tokens']
                )
                print(f"✅ 생성 완료:")
                print(f"   {result[:100]}..." if len(result) > 100 else f"   {result}")
            except Exception as e:
                print(f"❌ 생성 실패: {str(e)}")
        
        print("\n🎯 키워드 분석 데모")
        print("-" * 30)
        
        try:
            keywords = await ai_service.analyze_keywords("수제 케이크 카페 맛집 할인")
            print(f"✅ 추출된 키워드: {', '.join(keywords)}")
        except Exception as e:
            print(f"❌ 키워드 분석 실패: {str(e)}")
        
    except Exception as e:
        print(f"❌ AI 서비스 연결 실패: {str(e)}")
        print("💡 Gemini API 키가 올바른지 확인해보세요.")
    
    finally:
        await ai_service.close()
    
    print("\n🏁 데모 완료!")
    print("\n📖 다음 단계:")
    print("1. 백엔드 서버 시작: cd backend && python run.py")
    print("2. 프론트엔드 서버 시작: cd frontend && npm run dev")
    print("3. 브라우저에서 http://localhost:5173 접속")

def show_project_structure():
    """Show the project structure and features"""
    print("\n📁 프로젝트 구조")
    print("=" * 50)
    
    structure = """
📦 AI 마케팅 플랫폼
├── 🎯 타겟 고객 분석
│   ├── 업종별 고객 세그먼트 분석
│   ├── 연령대/성별/지역별 분포
│   └── AI 기반 행동 패턴 분석
│
├── 📝 AI 콘텐츠 생성
│   ├── 📰 네이버 블로그 (SEO 최적화)
│   ├── 📱 인스타그램 (해시태그 포함)
│   ├── 🎬 유튜브 숏폼 (스크립트)
│   └── 📄 전단지 (인쇄용 텍스트)
│
├── 📊 성과 분석 & 인사이트
│   ├── 실시간 성과 지표 추적
│   ├── 경쟁사 대비 성과 비교
│   ├── 트렌드 키워드 분석
│   └── AI 개선 제안
│
└── ⚙️ 비즈니스 설정
    ├── 업종별 맞춤 설정
    ├── 소셜 미디어 연동
    └── 브랜드 톤앤매너 설정
    """
    
    print(structure)
    
    print("\n✨ 주요 특징")
    print("-" * 30)
    features = [
        "🔥 원클릭 다채널 콘텐츠 생성",
        "🎯 업종별 맞춤 타겟 분석", 
        "📈 실시간 성과 모니터링",
        "🤖 로컬 AI로 비용 최소화",
        "🏗️ Clean Architecture 적용",
        "🧪 TDD 방식 개발",
        "💻 React + TypeScript",
        "🚀 FastAPI + Python"
    ]
    
    for feature in features:
        print(f"  {feature}")

if __name__ == "__main__":
    print("🌟 AI 마케팅 플랫폼에 오신 것을 환영합니다!")
    
    show_project_structure()
    
    print("\n" + "=" * 50)
    response = input("\nAI 콘텐츠 생성 데모를 실행하시겠습니까? (y/n): ")
    
    if response.lower() in ['y', 'yes', '네', 'ㅇ']:
        asyncio.run(demo_ai_content_generation())
    else:
        print("\n💡 서버를 시작하려면:")
        print("   백엔드: cd backend && python run.py")
        print("   프론트엔드: cd frontend && npm run dev")
        print("\n📖 자세한 정보는 README.md를 참고하세요.")

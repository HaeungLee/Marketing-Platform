#!/usr/bin/env python3
"""
Google Gemini API 통합 테스트 스크립트
실제 API 키를 사용하여 Gemini 서비스를 테스트합니다.
"""

import asyncio
import os
from dotenv import load_dotenv
from src.infrastructure.ai.gemini_service import GeminiService

# 환경 변수 로드
load_dotenv()

async def test_gemini_integration():
    """Gemini API 통합 테스트"""
    
    # API 키 확인
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_gemini_api_key_here":
        print("❌ GOOGLE_API_KEY가 설정되지 않았습니다.")
        print("📝 .env 파일에 실제 Google API 키를 설정해주세요.")
        return False
    
    try:
        # GeminiService 인스턴스 생성
        gemini_service = GeminiService(api_key=api_key)
        print("✅ GeminiService 인스턴스 생성 성공")
        
        # 테스트용 비즈니스 정보
        business_info = {
            "name": "맛있는 카페",
            "industry": "카페",
            "description": "신선한 원두와 수제 디저트를 제공하는 아늑한 카페",
            "target_audience": "20-30대 직장인",
            "unique_value": "직접 로스팅한 원두와 매일 만드는 수제 케이크"
        }
        
        print("\n🔍 테스트 1: 블로그 콘텐츠 생성")
        try:
            blog_content = await gemini_service.generate_content(
                business_info=business_info,
                content_type="blog"
            )
            # blog_content는 딕셔너리이므로 전체 문자열 길이를 계산
            content_text = str(blog_content.get("content", ""))
            print(f"✅ 블로그 콘텐츠 생성 성공 ({len(content_text)} 글자)")
            print(f"📝 제목: {blog_content.get('title', 'N/A')}")
            print(f"📝 미리보기: {content_text[:100]}...")
        except Exception as e:
            print(f"❌ 블로그 콘텐츠 생성 실패: {e}")
            return False
        
        print("\n🔍 테스트 2: 해시태그 생성")
        try:
            hashtags = await gemini_service.generate_hashtags(
                business_info=business_info,
                content="맛있는 커피와 수제 케이크를 즐길 수 있는 카페입니다."
            )
            print(f"✅ 해시태그 생성 성공: {hashtags}")
        except Exception as e:
            print(f"❌ 해시태그 생성 실패: {e}")
            return False
        
        print("\n🔍 테스트 3: 키워드 분석")
        try:
            keywords = await gemini_service.analyze_keywords(
                "신선한 원두로 만든 아메리카노와 라떼, 그리고 매일 새로 만드는 수제 케이크"
            )
            print(f"✅ 키워드 분석 성공: {keywords}")
        except Exception as e:
            print(f"❌ 키워드 분석 실패: {e}")
            return False
        
        print("\n🔍 테스트 4: 사용 가능한 모델 조회")
        try:
            models = await gemini_service.get_available_models()
            print(f"✅ 모델 조회 성공: {len(models)}개 모델 발견")
            for model in models[:3]:  # 처음 3개만 표시
                print(f"   - {model}")
            if len(models) > 3:
                print(f"   ... 외 {len(models) - 3}개")
        except Exception as e:
            print(f"❌ 모델 조회 실패: {e}")
            return False
        
        print("\n🔍 테스트 5: 성능 측정")
        try:
            performance = await gemini_service.measure_performance(
                model_name="gemini-1.5-flash",
                prompt="간단한 카페 소개글을 작성해주세요."
            )
            print(f"✅ 성능 측정 성공:")
            for key, value in performance.items():
                print(f"   - {key}: {value}")
        except Exception as e:
            print(f"❌ 성능 측정 실패: {e}")
            return False
        
        print("\n🎉 모든 통합 테스트 성공!")
        return True
        
    except Exception as e:
        print(f"❌ 통합 테스트 실패: {e}")
        return False

async def test_content_generation_quality():
    """콘텐츠 생성 품질 테스트"""
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_gemini_api_key_here":
        print("❌ API 키가 설정되지 않아 품질 테스트를 건너뜁니다.")
        return
    
    gemini_service = GeminiService(api_key=api_key)
    
    # 다양한 업종 테스트
    business_types = [
        {
            "name": "헬스케어 클리닉",
            "industry": "의료",
            "description": "개인 맞춤 건강 관리 서비스를 제공하는 클리닉",
            "target_audience": "30-50대 건강 관심층",
            "unique_value": "개인별 건강 데이터 분석과 맞춤 솔루션"
        },
        {
            "name": "펫샵 & 호텔",
            "industry": "펫케어",
            "description": "반려동물을 위한 종합 케어 서비스",
            "target_audience": "반려동물을 키우는 가족",
            "unique_value": "24시간 전문 케어와 개별 맞춤 서비스"
        }
    ]
    
    print("\n🎨 콘텐츠 생성 품질 테스트")
    
    for i, business_info in enumerate(business_types, 1):
        print(f"\n--- 테스트 {i}: {business_info['name']} ---")
        
        # 각 콘텐츠 타입별 생성 테스트
        content_types = ["blog", "instagram", "youtube", "flyer"]
        
        for content_type in content_types:
            try:
                content_result = await gemini_service.generate_content(
                    business_info=business_info,
                    content_type=content_type
                )
                # 콘텐츠 타입별로 적절한 필드에서 텍스트 추출
                if content_type == "blog":
                    main_content = content_result.get("content", "")
                    title = content_result.get("title", "")
                    preview = f"제목: {title}, 내용: {main_content[:50]}..."
                elif content_type == "instagram":
                    main_content = content_result.get("caption", "")
                    hashtags = content_result.get("hashtags", [])
                    preview = f"캡션: {main_content[:50]}..., 해시태그: {len(hashtags)}개"
                elif content_type == "youtube":
                    main_content = content_result.get("script", "")
                    title = content_result.get("title", "")
                    preview = f"제목: {title}, 스크립트: {main_content[:50]}..."
                elif content_type == "flyer":
                    main_content = content_result.get("body", "")
                    headline = content_result.get("headline", "")
                    preview = f"헤드라인: {headline}, 본문: {main_content[:50]}..."
                else:
                    main_content = str(content_result)
                    preview = main_content[:80]
                
                print(f"✅ {content_type.upper()} 콘텐츠 ({len(main_content)} 글자)")
                print(f"   📝 {preview}")
            except Exception as e:
                print(f"❌ {content_type.upper()} 콘텐츠 생성 실패: {e}")

if __name__ == "__main__":
    print("🚀 Google Gemini API 통합 테스트 시작")
    print("=" * 50)
    
    # 기본 통합 테스트
    success = asyncio.run(test_gemini_integration())
    
    if success:
        print("\n" + "=" * 50)
        # 품질 테스트
        asyncio.run(test_content_generation_quality())
    
    print("\n" + "=" * 50)
    print("✨ 테스트 완료")

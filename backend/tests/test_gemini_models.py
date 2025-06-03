#!/usr/bin/env python3
"""
Gemini 모델 테스트 스크립트
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키 설정
api_key = os.getenv('GOOGLE_API_KEY')
print(f"API 키 설정 상태: {'✅ 설정됨' if api_key else '❌ 설정되지 않음'}")

if not api_key:
    print("GOOGLE_API_KEY가 .env 파일에 설정되지 않았습니다.")
    exit(1)

# Gemini 설정
genai.configure(api_key=api_key)

print("\n🔍 사용 가능한 Gemini 모델 목록:")
try:
    models = genai.list_models()
    for model in models:
        print(f"- {model.name}: {model.display_name}")
        if 'image' in model.name.lower() or 'generate' in model.name.lower():
            print(f"  ⭐ 이미지 관련 모델일 가능성")
except Exception as e:
    print(f"❌ 모델 목록 조회 오류: {e}")

print("\n🧪 텍스트 생성 테스트 (gemini-pro):")
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello, world!")
    print(f"✅ 텍스트 생성 성공: {response.text[:100]}...")
except Exception as e:
    print(f"❌ 텍스트 생성 오류: {e}")

print("\n🎨 이미지 생성 테스트 (gemini-2.0-flash-exp):")
try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Generate an image of a sunset")
    print(f"✅ 이미지 생성 응답 타입: {type(response)}")
    print(f"Candidates: {len(response.candidates) if response.candidates else 0}")
    if response.candidates:
        for i, candidate in enumerate(response.candidates):
            print(f"  Candidate {i}: {candidate}")
except Exception as e:
    print(f"❌ 이미지 생성 오류: {e}")

print("\n🎨 다른 모델명으로 테스트:")
model_names = [
    'gemini-2.0-flash-thinking-exp',
    'gemini-exp-1121', 
    'imagen-3.0-generate-001',
    'imagegeneration@002'
]

for model_name in model_names:
    try:
        print(f"\n테스트: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Generate a simple image")
        print(f"✅ {model_name} 작동")
    except Exception as e:
        print(f"❌ {model_name} 오류: {e}")

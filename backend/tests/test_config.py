#!/usr/bin/env python3
"""
Settings 테스트 스크립트
"""
try:
    from src.config.settings import settings
    print("✅ Settings loaded successfully")
    print(f"📋 CORS origins: {settings.cors_origins_list}")
    print(f"🔑 Google API key configured: {'Yes' if settings.google_api_key else 'No'}")
    print(f"🏠 Base URL: {settings.BASE_URL}")
except Exception as e:
    print(f"❌ Error loading settings: {e}")
    import traceback
    traceback.print_exc()

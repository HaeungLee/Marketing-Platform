#!/usr/bin/env python3
"""
간단한 API 테스트
"""
import sys
import os
import asyncio
from fastapi.testclient import TestClient

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_api():
    try:
        print("🔄 Testing API endpoints...")
        
        # Import main app
        from main import app
        
        client = TestClient(app)
        
        # Test health endpoint (if exists)
        print("✅ FastAPI app imported successfully")
        
        # Test image generation endpoint
        print("🔄 Testing image generation endpoint...")
        response = client.post(
            "/api/images/generate",
            json={"prompt": "simple test image"}
        )
        
        print(f"📊 Response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Image generation API works! Data keys: {list(data.keys())}")
            if 'image_data' in data and data['image_data']:
                print(f"📊 Generated image data length: {len(data['image_data'])} characters")
        else:
            print(f"⚠️ API returned status {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Error in API test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api()

#!/usr/bin/env python3
"""
Image Service 간단 테스트
"""
import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_image_service():
    try:
        print("🔄 Testing image service...")
        
        # Import after path setup
        from domain.services.image_service import image_service
        
        print("✅ ImageService imported successfully")
        
        # Test placeholder generation
        result = await image_service.generate_placeholder_image("test")
        if result:
            print("✅ Placeholder image generation works")
            print(f"📊 Generated image data length: {len(result)} characters")
        else:
            print("❌ Placeholder image generation failed")
            
        # Test with a simple prompt (this will use Gemini API if available)
        print("\n🔄 Testing AI image generation...")
        ai_result = await image_service.generate_image("simple cat illustration")
        if ai_result:
            print("✅ AI image generation works")
            print(f"📊 AI Generated image data length: {len(ai_result)} characters")
        else:
            print("⚠️ AI image generation failed, but that's expected if API is not configured")
            
    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_image_service())

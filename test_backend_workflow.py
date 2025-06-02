import requests
import json
import base64
from PIL import Image
import io

def test_backend_api():
    """Test the backend API image generation"""
    print("🚀 Testing backend API...")
    
    # Test basic connection
    try:
        response = requests.get("http://localhost:8000/api/images/test")
        print(f"📊 Test endpoint status: {response.status_code}")
        if response.ok:
            print(f"✅ Test response: {response.json()}")
        else:
            print(f"❌ Test failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Test image generation
    try:
        payload = {"prompt": "카페 전단지, 모던한 스타일"}
        response = requests.post(
            "http://localhost:8000/api/images/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Generate endpoint status: {response.status_code}")
        
        if response.ok:
            data = response.json()
            print(f"✅ Response keys: {list(data.keys())}")
            print(f"🖼️ Has image_data: {bool(data.get('image_data'))}")
            
            if data.get('image_data'):
                image_data = data['image_data']
                print(f"📏 Image data length: {len(image_data)}")
                print(f"🔍 Image data preview: {image_data[:50]}...")
                
                # Try to decode and verify the image
                try:
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(io.BytesIO(image_bytes))
                    print(f"🎨 Image size: {image.size}")
                    print(f"🎨 Image format: {image.format}")
                    print(f"🎨 Image mode: {image.mode}")
                    
                    # Save test image
                    image.save("test_generated_image.png")
                    print("💾 Test image saved as 'test_generated_image.png'")
                    
                    return True
                except Exception as e:
                    print(f"❌ Image decode error: {e}")
                    return False
            else:
                print("❌ No image data in response")
                return False
        else:
            print(f"❌ Generate failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Generate request failed: {e}")
        return False

if __name__ == "__main__":
    test_backend_api()

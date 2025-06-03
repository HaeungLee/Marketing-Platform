#!/usr/bin/env python3
"""
Frontend Integration Test
Tests the complete workflow from frontend to backend for image generation.
"""

import requests
import json
import time
from datetime import datetime

def test_frontend_backend_integration():
    """Test the complete frontend-backend integration for image generation."""
    
    # Backend API URL
    base_url = "http://127.0.0.1:8001"
    
    print("🔄 Testing Frontend-Backend Integration...")
    print(f"Backend URL: {base_url}")
    print(f"Frontend URL: http://localhost:3001")
    print("-" * 50)
    
    # 1. Test backend health
    try:
        health_response = requests.get(f"{base_url}/")
        print(f"✅ Backend Health Check: {health_response.status_code}")
        print(f"   Response: {health_response.json()}")
    except Exception as e:
        print(f"❌ Backend Health Check Failed: {e}")
        return False
    
    # 2. Test image generation API (same as frontend would call)
    image_request = {
        "business_name": "Tech Startup Co",
        "business_category": "Technology",
        "image_style": "modern",
        "prompt": "A modern tech office with computers and innovative workspace design"
    }
    
    print(f"\n🎨 Testing Image Generation API...")
    print(f"Request: {json.dumps(image_request, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/api/v1/content/generate-image",
            json=image_request,
            headers={"Content-Type": "application/json"}
        )
        end_time = time.time()
        
        print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Image generated successfully!")
            print(f"   Filename: {result['filename']}")
            print(f"   URL: {result['url']}")
            print(f"   Full URL: {base_url}{result['url']}")
            
            # 3. Test image access
            image_url = f"{base_url}{result['url']}"
            image_response = requests.get(image_url)
            
            if image_response.status_code == 200:
                print(f"✅ Image accessible via URL")
                print(f"   Image size: {len(image_response.content):,} bytes")
                print(f"   Content type: {image_response.headers.get('content-type', 'unknown')}")
                return True
            else:
                print(f"❌ Image not accessible: {image_response.status_code}")
                return False
                
        else:
            print(f"❌ Image generation failed")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Image generation request failed: {e}")
        return False

def test_cors_headers():
    """Test CORS headers for frontend integration."""
    print(f"\n🌐 Testing CORS Headers...")
    
    try:
        # Simulate a CORS preflight request
        response = requests.options(
            "http://127.0.0.1:8001/api/v1/content/generate-image",
            headers={
                "Origin": "http://localhost:3001",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        print(f"📊 CORS Preflight Status: {response.status_code}")
        cors_headers = {
            key: value for key, value in response.headers.items() 
            if key.lower().startswith('access-control')
        }
        
        if cors_headers:
            print("✅ CORS Headers found:")
            for key, value in cors_headers.items():
                print(f"   {key}: {value}")
            return True
        else:
            print("❌ No CORS headers found")
            return False
            
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Frontend-Backend Integration Test")
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Run tests
    backend_test = test_frontend_backend_integration()
    cors_test = test_cors_headers()
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY:")
    print(f"   Backend Integration: {'✅ PASS' if backend_test else '❌ FAIL'}")
    print(f"   CORS Configuration: {'✅ PASS' if cors_test else '❌ FAIL'}")
    
    if backend_test and cors_test:
        print("\n🎉 All tests passed! Frontend-Backend integration is ready.")
        print("💡 You can now test the image generation in the browser at:")
        print("   http://localhost:3001/")
    else:
        print("\n⚠️  Some tests failed. Please check the backend configuration.")

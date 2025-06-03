import requests
import json

# 백엔드 이미지 생성 API 테스트
url = "http://localhost:8000/api/images/generate"
data = {
    "prompt": "A beautiful modern cafe interior", 
    "business_info": {
        "name": "Test Cafe",
        "category": "Restaurant"
    }
}

print("🔄 이미지 생성 API 테스트 중...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data)
    print(f"\n📊 Status Code: {response.status_code}")
    print(f"📋 Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 성공! 이미지 URL: {result.get('url', 'N/A')}")
    else:
        print(f"❌ 실패: {response.text}")
        
except Exception as e:
    print(f"❌ 오류: {e}")

import requests
import base64
import json

# API 요청
response = requests.post(
    "http://localhost:8000/api/images/generate",
    json={"prompt": "A beautiful sunset over mountains"},
    timeout=30
)

if response.status_code == 200:
    data = response.json()
    image_data = data.get("image_data")
    
    if image_data:
        # Base64 디코딩해서 이미지 파일로 저장
        try:
            image_bytes = base64.b64decode(image_data)
            with open("generated_image.png", "wb") as f:
                f.write(image_bytes)
            print("✅ 이미지가 generated_image.png에 저장되었습니다!")
            print(f"이미지 크기: {len(image_bytes)} bytes")
        except Exception as e:
            print(f"❌ 이미지 저장 오류: {e}")
    else:
        print("❌ image_data가 응답에 없습니다")
else:
    print(f"❌ API 오류: {response.status_code}")
    print(response.text)

# 🚀 Quick Start Guide - AI 마케팅 플랫폼

## 즉시 실행 가이드 (5분 안에 시작하기)

### 1️⃣ 프로젝트 확인
```bash
# 프로젝트 구조 확인
ls -la d:/FinalProjects/Marketing-Platform/
```

### 2️⃣ 백엔드 실행
```bash
# 백엔드 디렉토리 이동
cd "d:/FinalProjects/Marketing-Platform/backend"

# Python 의존성 설치 (1회만)
pip install fastapi uvicorn pydantic python-dotenv pydantic-settings

# 서버 시작
python run.py
```

✅ **백엔드 확인**: http://localhost:8000/docs

### 3️⃣ 프론트엔드 실행
```bash
# 새 터미널에서 프론트엔드 디렉토리 이동
cd "d:/FinalProjects/Marketing-Platform/frontend"

# 개발 서버 시작 (node_modules는 이미 설치됨)
npm run dev
```

✅ **프론트엔드 확인**: http://localhost:5173

### 4️⃣ 플랫폼 체험하기

#### 🏪 비즈니스 설정
1. **BusinessSetupPage**에서 업종 정보 입력
   - 업종: 카페/음식점/소매업 등
   - 위치: 지역 선택
   - 타겟 고객: 연령대/성별

#### 🤖 AI 콘텐츠 생성
1. **ContentGeneratorPage**에서 콘텐츠 생성
   - 상품/서비스 설명 입력
   - 콘텐츠 타입 선택 (블로그/인스타그램/유튜브/전단지)
   - 톤앤매너 설정
   - 생성 버튼 클릭

#### 📊 분석 대시보드
1. **AnalyticsPage**에서 성과 확인
   - 성과 지표 차트
   - 고객 세그먼트 분석
   - 트렌드 키워드
   - AI 추천 인사이트

#### ⚙️ 설정 관리
1. **SettingsPage**에서 개인화
   - 프로필 정보 수정
   - AI 생성 기본값 설정
   - 소셜미디어 계정 연동

## 🎯 데모 시나리오

### 시나리오: "신선한 과일 주스바" 마케팅

1. **비즈니스 정보 입력**
   ```
   업종: 음료/디저트
   상호명: 프레시 주스바
   위치: 홍대 근처
   주요 상품: 시즌 과일 주스
   타겟: 20-30대 직장인, 대학생
   ```

2. **AI 콘텐츠 생성 요청**
   ```
   상품: "여름 특별 메뉴 - 망고 패션후르츠 주스"
   톤앤매너: 친근하고 상큼하게
   키워드: 신선함, 건강, 여름, 시원함
   ```

3. **생성 결과 예시**
   - **블로그**: "여름 더위를 날려줄 망고 패션후르츠 주스! 매일 아침 신선하게..."
   - **인스타그램**: "☀️여름엔 망고🥭 #망고주스 #홍대맛집 #신선한과일 #건강음료"
   - **유튜브**: "30초 만에 알아보는 완벽한 망고 주스 레시피! #shorts"
   - **전단지**: "🎉 오픈 기념! 망고 패션후르츠 주스 30% 할인! 7/31까지!"

## 🛠️ 문제 해결

### 백엔드 실행 오류
```bash
# 의존성 재설치
pip install --upgrade fastapi uvicorn

# 포트 충돌 시 다른 포트 사용
python -c "
import uvicorn
uvicorn.run('src.main:app', host='0.0.0.0', port=8001, reload=True)
"
```

### 프론트엔드 실행 오류
```bash
# node_modules 재설치
rm -rf node_modules
npm install

# 캐시 클리어
npm run dev -- --force
```

### AI 기능 테스트 (선택적)
```bash
# Ollama 설치 후 (https://ollama.ai/)
ollama serve
ollama pull llama2

# 백엔드에서 AI 기능 활성화됨
```

## 📱 주요 기능 테스트 체크리스트

- [ ] 홈페이지 접속 및 네비게이션
- [ ] 비즈니스 정보 입력 및 저장
- [ ] AI 콘텐츠 4가지 타입 생성
- [ ] 분석 차트 및 데이터 시각화
- [ ] 설정 페이지 커스터마이징
- [ ] 반응형 디자인 (모바일/태블릿)

## 🎉 완료!

이제 AI 마케팅 플랫폼을 완전히 체험할 수 있습니다!

### 📞 지원
- 기술 문의: 프로젝트 이슈 트래커
- 기능 제안: 피드백 환영
- 버그 리포트: 상세 정보와 함께 제보

**🌟 훌륭한 마케팅 콘텐츠를 만들어보세요!**

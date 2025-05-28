# AI 마케팅 플랫폼 🚀

소상공인과 중소기업을 위한 종합 AI 마케팅 솔루션

## 📋 프로젝트 개요

본 프로젝트는 소상공인과 중소기업이 손쉽게 마케팅 콘텐츠를 생성하고 관리할 수 있도록 도와주는 AI 기반 플랫폼입니다. 업종 정보와 상품 정보를 입력하면 공공데이터와 업종 특성을 바탕으로 타겟층을 분석하고, 네이버 블로그, 인스타그램, 유튜브 숏폼, 전단지용 마케팅 콘텐츠를 자동 생성합니다.

## ✨ 주요 기능

### 🎯 타겟 고객 분석
- 공공데이터 기반 업종별 고객 세그먼트 분석
- 연령대, 성별, 지역별 고객 분포 시각화
- AI 기반 고객 행동 패턴 분석

### 📝 AI 콘텐츠 생성
- **네이버 블로그**: SEO 최적화된 블로그 포스트 자동 생성
- **인스타그램**: 해시태그와 함께 매력적인 소셜 미디어 콘텐츠
- **유튜브 숏폼**: 짧고 임팩트 있는 영상 스크립트
- **전단지**: 인쇄용 홍보물 텍스트 및 레이아웃 제안

### 📊 성과 분석 및 인사이트
- 콘텐츠별 성과 지표 추적
- 경쟁사 대비 성과 비교 분석
- 트렌드 키워드 및 시장 동향 분석
- AI 기반 개선 제안

### ⚙️ 비즈니스 설정
- 업종별 맞춤형 설정 워크플로우
- 소셜 미디어 계정 연동
- 브랜드 톤앤매너 설정

## 🏗️ 기술 스택

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Architecture**: Clean Architecture (Domain-Driven Design)
- **AI Service**: Ollama (로컬 LLM)
- **Testing**: pytest (TDD 방식)
- **Design Patterns**: SOLID 원칙 준수

### Frontend
- **Framework**: React 18 + TypeScript
- **UI Library**: Chakra UI
- **Charts**: Recharts
- **Maps**: React Leaflet
- **State Management**: React Query
- **Build Tool**: Vite

### 개발 원칙
- **TDD**: 테스트 주도 개발
- **Clean Architecture**: 계층 분리 및 의존성 역전
- **SOLID Principles**: 객체지향 설계 원칙
- **무료 티어**: 최소 비용으로 실제 서비스 구현

## 📁 프로젝트 구조

```
Marketing-Platform/
├── backend/                    # 백엔드 (FastAPI)
│   ├── src/
│   │   ├── domain/            # 도메인 계층
│   │   │   ├── entities/      # 엔티티
│   │   │   └── value_objects/ # 값 객체
│   │   ├── application/       # 애플리케이션 계층
│   │   │   └── interfaces/    # 인터페이스
│   │   ├── infrastructure/    # 인프라 계층
│   │   │   └── ai/           # AI 서비스 구현
│   │   ├── presentation/      # 프레젠테이션 계층
│   │   │   └── api/v1/       # API 엔드포인트
│   │   ├── config/           # 설정
│   │   └── main.py           # 메인 애플리케이션
│   ├── tests/                # 테스트
│   │   └── unit/
│   ├── requirements.txt      # 의존성
│   └── run.py               # 시작 스크립트
├── frontend/                 # 프론트엔드 (React)
│   ├── src/
│   │   ├── components/      # 공통 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── services/       # API 서비스
│   │   ├── types/          # TypeScript 타입
│   │   └── theme.ts        # UI 테마
│   ├── package.json        # 의존성
│   └── vite.config.ts      # 빌드 설정
├── data/                    # 공공데이터 및 리소스
├── docs/                    # 문서
└── scripts/                 # 유틸리티 스크립트
```

## 🚀 빠른 시작

### 사전 요구사항
- Python 3.9+
- Node.js 18+
- npm 또는 yarn

### 백엔드 설정 및 실행

```bash
# 백엔드 디렉토리로 이동
cd backend

# Python 가상환경 생성 (선택사항)
python -m venv venv
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python run.py
```

백엔드 서버가 http://localhost:8000 에서 실행됩니다.

### 프론트엔드 설정 및 실행

```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드 서버가 http://localhost:5173 에서 실행됩니다.

### 테스트 실행

```bash
# 백엔드 테스트
cd backend
python -m pytest tests/ -v

# 프론트엔드 테스트
cd frontend
npm test
```

## 🔧 설정

### 환경 변수
백엔드의 `src/config/settings.py`에서 다음 설정을 확인하세요:

- `OLLAMA_BASE_URL`: Ollama 서버 주소 (기본: http://localhost:11434)
- `CORS_ORIGINS`: CORS 허용 도메인
- `DEBUG`: 디버그 모드 설정

### AI 모델 설정
Ollama를 사용하여 로컬 LLM을 실행해야 합니다:

```bash
# Ollama 설치 후
ollama pull llama2  # 또는 다른 모델
ollama serve
```

## 📱 페이지 구성

### 🏠 홈페이지
- 플랫폼 소개 및 주요 기능 안내
- 시작하기 버튼으로 빠른 접근

### 📊 대시보드
- 실시간 성과 지표 모니터링
- KPI 카드 및 차트 시각화
- 최근 생성된 콘텐츠 현황

### 🎨 콘텐츠 생성
- 4가지 콘텐츠 타입 선택 (블로그/인스타그램/유튜브/전단지)
- AI 기반 맞춤형 콘텐츠 생성
- 톤앤매너 및 타겟 고객 설정

### 📈 분석 & 인사이트
- 성과 분석 대시보드
- 고객 세그먼트 분석
- 경쟁사 대비 성과 비교
- 트렌드 키워드 분석

### ⚙️ 설정
- 프로필 및 비즈니스 정보 관리
- AI 생성 설정 및 알림 설정
- 소셜 미디어 계정 연동

### 🏢 비즈니스 설정
- 업종별 맞춤 설정 워크플로우
- 지도 기반 위치 설정
- 브랜드 정보 및 타겟 고객 정의

## 🧪 테스트 전략

### 백엔드 (TDD)
- **Unit Tests**: 도메인 엔티티 및 값 객체 테스트
- **Integration Tests**: API 엔드포인트 테스트
- **Service Tests**: AI 서비스 인터페이스 테스트

### 프론트엔드
- **Component Tests**: React 컴포넌트 단위 테스트
- **Integration Tests**: API 통신 테스트
- **E2E Tests**: 사용자 시나리오 테스트

## 🏆 경쟁력

### 🔥 차별화 요소
1. **업종별 특화**: 공공데이터 기반 업종별 맞춤 분석
2. **원클릭 생성**: 하나의 입력으로 다양한 플랫폼 콘텐츠 생성
3. **실시간 트렌드**: 키워드 트렌드 및 경쟁사 분석
4. **무료 접근**: 로컬 LLM 활용으로 API 비용 최소화

### 🎯 타겟 사용자
- 마케팅 예산이 제한적인 소상공인
- 콘텐츠 제작 노하우가 부족한 중소기업
- 디지털 마케팅 전문가가 없는 자영업자

## 🛣️ 로드맵

### Phase 1 (현재)
- ✅ 기본 플랫폼 구조 완성
- ✅ AI 콘텐츠 생성 기능
- ✅ 분석 대시보드
- ✅ 사용자 설정

### Phase 2 (예정)
- [ ] 실제 소셜 미디어 API 연동
- [ ] 고급 분석 알고리즘
- [ ] 콘텐츠 스케줄링
- [ ] 모바일 앱

### Phase 3 (예정)
- [ ] 협업 기능
- [ ] 고급 AI 모델 지원
- [ ] 마켓플레이스
- [ ] 기업용 버전

## 📞 문의 및 지원

프로젝트에 대한 문의사항이나 개선 제안이 있으시면 언제든 연락주세요.

---

**Made with ❤️ for 소상공인들**

이 프로젝트는 소상공인과 중소기업의 디지털 마케팅 성공을 위해 만들어졌습니다.

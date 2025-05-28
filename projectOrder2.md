# Marketing Platform 프로젝트 명세서 v2.0

> **프로젝트 목적**: 공모전용 - '실제 서비스가 가능한 것처럼' 보이는 소상공인/중소기업 마케팅 플랫폼 개발
> **핵심 전략**: 최소한의 비용(무료 티어 중심), 최소한의 GPU 사용, 최대한의 완성도

## 🎯 프로젝트 개요

소상공인 및 중소기업이 업종 정보와 홍보 상품을 입력하면, 공공데이터와 업종 특성을 바탕으로 타겟층을 분석/시각화하고, 네이버 블로그, 인스타그램, 유튜브 숏폼, 전단지용 마케팅 콘텐츠를 자동 생성하는 웹 플랫폼.

## 🛠 기술 스택 (최적화된 구성)

### Backend
- **Framework**: FastAPI (경량, 빠른 개발)
- **Database**: PostgreSQL (메인), Redis (세션/캐싱)
- **AI/ML**: 
  - 로컬 LLM: HyperCLOVA 0.5b/1.5b → gemma3:1b/4b → qwen3:1.7b/4b → OpenAI GPT (최종)
  - 분석: scikit-learn (타겟층 클러스터링)
  - 이미지: Stable Diffusion (외부 API - Google Drive/Kaggle)
- **형태소 분석**: KoNLPy/Komoran → LLM 프롬프트 엔지니어링 (성능 우선)

### Frontend  
- **Framework**: React + TypeScript + Vite
- **UI Library**: Chakra UI (반응형 디자인)
- **지도**: Leaflet + 카카오맵 API
- **차트**: Recharts
- **상태관리**: Context API + useReducer

### Infrastructure (무료 티어 중심)
- **배포**: 
  - Backend: Render/Railway (무료 티어)
  - Frontend: Vercel/Netlify (무료 티어)
  - Database: Supabase PostgreSQL (500MB 무료)
  - Cache: Redis Cloud (30MB 무료)
- **컨테이너**: Docker + Docker Compose (개발환경)
- **CI/CD**: GitHub Actions (무료)

### 테스트
- **Backend**: Pytest, Pytest-asyncio
- **Frontend**: Jest, React Testing Library, Cypress
- **Performance**: Locust (부하 테스트)
- **Accessibility**: axe-core

## 🗂 데이터 소스 전략

### 공공데이터 (API + CSV 파일)
1. **업종별 통계**: 소상공인시장진흥공단, 통계청 KOSIS
2. **소비 트렌드**: 한국은행, 카드사 공개 데이터
3. **지역별 인구**: 행정안전부, 통계청 인구총조사
4. **유동인구/상권**: SKT 빅데이터, 서울시 열린데이터광장

### 데이터 처리 방식
- **실시간 처리 없음**: 배치 처리로 일정 주기 업데이트
- **캐싱 전략**: Redis로 자주 조회되는 분석 결과 캐싱
- **대체 데이터**: API 장애 시 CSV 파일 기반 분석 제공

## 🏗 Clean Architecture 설계

```
src/
├── domain/              # 비즈니스 로직 (프레임워크 독립)
│   ├── entities/        # User, Business, Content, Analytics
│   ├── repositories/    # 인터페이스 정의
│   ├── services/        # 도메인 서비스
│   └── value_objects/   # Email, Coordinates, Category
├── application/         # 유스케이스 (비즈니스 규칙)
│   ├── use_cases/       # 각 기능별 유스케이스
│   ├── dto/            # 데이터 전송 객체
│   └── interfaces/     # 외부 서비스 인터페이스
├── infrastructure/      # 외부 시스템 연동
│   ├── database/       # PostgreSQL, Redis 구현체
│   ├── external/       # AI 서비스, 공공데이터 API
│   ├── email/          # SMTP 서비스
│   └── security/       # JWT, 암호화
└── presentation/       # API 엔드포인트
    ├── api/v1/         # REST API
    ├── middleware/     # 인증, CORS, 에러처리
    └── schemas/        # Pydantic 스키마
```

## 🔥 핵심 기능 구현 계획

### 1. 사용자 인증 시스템 (SOLID + TDD)
```python
# 도메인 주도 설계 예시
class AuthService:  # 단일 책임
    def __init__(self, user_repo: UserRepository, jwt_handler: JWTHandler):
        self._user_repo = user_repo  # 의존성 역전
        self._jwt_handler = jwt_handler
    
    async def authenticate(self, credentials: LoginCredentials) -> AuthResult:
        # 비즈니스 로직 구현
```

**지원 인증 방식**:
- 자체 회원가입/로그인 (이메일 + 비밀번호)
- 소셜 로그인: 구글, 네이버, 카카오 (Firebase Auth)
- 게스트 모드: Redis 24시간 세션

**보안 요소**:
- JWT 토큰 (액세스 + 리프레시)
- 비밀번호 해시 (bcrypt)
- HTTPS 강제
- 비밀번호 재설정 (SMTP)

### 2. 업종/지역 정보 입력 시스템
**업종 분류**:
- 대분류/소분류 드롭다운 (JSON 데이터)
- 자유 텍스트 입력 시 AI 기반 업종 자동 분류
- 사용자 정의 업종 추가 가능

**지도 연동**:
- Leaflet + 카카오맵 API
- 주소 입력 또는 지도 클릭으로 위치 선택
- 반경 설정 (100m~2km) 및 상권 분석 영역 표시
- GeoJSON 기반 유동인구/경쟁업체 히트맵

### 3. 타겟층 분석 엔진
**분석 알고리즘**:
```python
# scikit-learn 기반 클러스터링
class TargetAnalysisService:
    def analyze_demographics(self, business_data: BusinessData) -> TargetAnalysis:
        # K-means 클러스터링으로 연령/성별/소득 구간 분석
        # 업종별 특성 + 지역 데이터 조합
        # 시각화용 차트 데이터 생성
```

**시각화**:
- Recharts 기반 대시보드
- 연령대별 원형 차트
- 성별 분포 막대 차트  
- 소비 패턴 시계열 차트
- 경쟁사 분석 히트맵

### 4. AI 콘텐츠 생성 시스템
**LLM 모델 우선순위**:
1. HyperCLOVA 0.5b/1.5b (.safetensors, 로컬)
2. gemma3:1b/4b (LoRA 파인튜닝 고려)
3. qwen3:1.7b/4b (한국어 성능 테스트)
4. OpenAI GPT-3.5/4 (최종 대안, 프롬프트 엔지니어링)

**채널별 콘텐츠**:
```python
class ContentGenerationService:
    def generate_blog_post(self, business_info, target_analysis) -> BlogContent:
        # SEO 최적화된 블로그 포스트
        # 지역명 + 업종 키워드 자동 삽입
        
    def generate_instagram_post(self, business_info) -> InstagramContent:
        # 짧은 문장 + 해시태그
        # AI 기반 키워드 추출
        
    def generate_youtube_script(self, business_info) -> YouTubeContent:
        # 30-60초 숏폼 스크립트 + 자막
        
    def generate_flyer_design(self, business_info) -> FlyerContent:
        # Stable Diffusion API 호출
        # Google Drive/Kaggle 연동
```

**프롬프트 템플릿 시스템**:
- 업종별 특화 프롬프트
- 타겟층 맞춤 톤앤매너
- 지역 특성 반영 키워드
- 재사용 가능한 템플릿 구조

### 5. 콘텐츠 미리보기 및 공유
**Chakra UI 기반 편집기**:
- 채널별 미리보기 (블로그: HTML, 인스타: 모바일 프레임)
- 실시간 편집 (Textarea + 마크다운 지원)
- 다운로드: PDF, PNG, TXT 형식 지원
- QR 코드 생성 및 URL 공유

**저장 시스템**:
- PostgreSQL 기반 즐겨찾기
- 사용자별 콘텐츠 히스토리
- 개인정보 제거된 공유 링크

## 📊 성능 최적화 전략

### 캐싱 계층
```python
# Redis 기반 다단계 캐싱
@cache(ttl=3600)  # 1시간 캐싱
async def get_area_demographics(coordinates: Coordinates) -> Demographics:
    # 공공데이터 API 결과 캐싱

@cache(ttl=86400)  # 24시간 캐싱  
async def get_business_categories() -> List[Category]:
    # 업종 분류 데이터 캐싱
```

### 데이터베이스 최적화
- PostgreSQL 전용 설계 (MongoDB 제거로 복잡도 감소)
- 인덱싱 최적화 (지역 기반 쿼리)
- Connection pooling
- 읽기 전용 복제본 고려 (스케일링 시)

### 프론트엔드 최적화
- Vite 기반 빠른 개발 빌드
- 코드 스플리팅 (React.lazy)
- 이미지 최적화 (WebP, 지연 로딩)
- Chakra UI 테마 커스터마이징

## 🧪 TDD 구현 전략

### 테스트 우선순위
1. **Unit Tests** (도메인 로직)
2. **Integration Tests** (API 엔드포인트)  
3. **E2E Tests** (사용자 시나리오)

### 예시 테스트 구조
```python
# tests/unit/domain/test_auth_service.py
class TestAuthService:
    def test_should_authenticate_valid_user(self):
        # Given: 유효한 사용자 정보
        # When: 인증 시도
        # Then: 성공적인 인증 결과
        
    def test_should_reject_invalid_credentials(self):
        # Given: 잘못된 인증 정보  
        # When: 인증 시도
        # Then: 인증 실패
```

### Mock 데이터 전략
- 공공데이터 API는 Mock 데이터로 테스트
- AI 모델은 가짜 응답으로 테스트
- 외부 서비스 의존성 제거

## 🚀 배포 전략 (무료 티어 최적화)

### 단계별 배포
1. **개발**: Docker Compose (로컬)
2. **스테이징**: Render (무료 티어)
3. **프로덕션**: 무료 호스팅 조합

### 환경별 설정
```yaml
# docker-compose.yml (개발)
services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://localhost/marketing_dev
      - REDIS_URL=redis://localhost:6379
      
  frontend:
    build: ./frontend
    environment:
      - VITE_API_URL=http://localhost:8000
```

### 모니터링
- 로그 수집 (stdout 기반)
- 성능 메트릭 (기본 HTTP 메트릭)
- 에러 추적 (Sentry 무료 티어)

## 📈 개발 로드맵

### Phase 1: 핵심 인증 및 UI (1-2주)
- [ ] 사용자 인증 시스템 (TDD)
- [ ] 기본 UI 컴포넌트 (Chakra UI)
- [ ] 데이터베이스 설계 및 마이그레이션
- [ ] Docker 개발 환경 구성

### Phase 2: 데이터 입력 및 분석 (2-3주)
- [ ] 업종 분류 시스템
- [ ] 카카오맵 API 연동
- [ ] 공공데이터 API/CSV 처리
- [ ] 기본 타겟 분석 알고리즘

### Phase 3: AI 콘텐츠 생성 (2-3주)
- [ ] LLM 모델 테스트 및 선택
- [ ] 채널별 콘텐츠 생성 엔진
- [ ] Stable Diffusion API 연동
- [ ] 프롬프트 최적화

### Phase 4: 완성도 및 배포 (1-2주)
- [ ] 콘텐츠 미리보기/편집/다운로드
- [ ] 성능 최적화 및 캐싱
- [ ] E2E 테스트 및 품질 보증
- [ ] 무료 티어 배포 및 데모

## 🎯 성공 지표 (공모전 관점)

### 기술적 완성도
- [ ] 모든 핵심 기능 동작 (데모 가능)
- [ ] 반응형 UI (모바일/데스크톱)
- [ ] 실제 공공데이터 연동
- [ ] AI 콘텐츠 생성 품질

### 사용자 경험
- [ ] 직관적인 UI/UX
- [ ] 빠른 응답 속도 (<3초)
- [ ] 오류 처리 및 사용자 가이드
- [ ] 접근성 준수 (axe-core 통과)

### 확장 가능성 시연
- [ ] Clean Architecture 구조 설명
- [ ] TDD 테스트 커버리지 >80%
- [ ] 성능 테스트 결과 제시
- [ ] 실제 서비스 배포 가능성 입증

---

**다음 단계**: `project-needed.md`의 HIGH PRIORITY 항목 조사 완료 후 구현 시작

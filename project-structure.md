# Marketing Platform 프로젝트 구조

## 전체 프로젝트 구조

```
Marketing-Platform/
├── backend/                          # FastAPI 백엔드
│   ├── src/
│   │   ├── domain/                   # 도메인 계층 (비즈니스 로직)
│   │   │   ├── entities/             # 엔티티
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   ├── business.py
│   │   │   │   ├── content.py
│   │   │   │   └── analytics.py
│   │   │   ├── repositories/         # 리포지토리 인터페이스
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_repository.py
│   │   │   │   ├── business_repository.py
│   │   │   │   └── content_repository.py
│   │   │   ├── services/             # 도메인 서비스
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_service.py
│   │   │   │   ├── target_analysis_service.py
│   │   │   │   └── content_generation_service.py
│   │   │   └── value_objects/        # 값 객체
│   │   │       ├── __init__.py
│   │   │       ├── email.py
│   │   │       ├── coordinates.py
│   │   │       └── business_category.py
│   │   ├── application/              # 애플리케이션 계층 (유스케이스)
│   │   │   ├── use_cases/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth/
│   │   │   │   │   ├── signup_use_case.py
│   │   │   │   │   ├── login_use_case.py
│   │   │   │   │   └── reset_password_use_case.py
│   │   │   │   ├── business/
│   │   │   │   │   ├── register_business_use_case.py
│   │   │   │   │   └── analyze_target_use_case.py
│   │   │   │   └── content/
│   │   │   │       ├── generate_content_use_case.py
│   │   │   │       └── save_content_use_case.py
│   │   │   ├── dto/                  # 데이터 전송 객체
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_dto.py
│   │   │   │   ├── business_dto.py
│   │   │   │   └── content_dto.py
│   │   │   └── interfaces/           # 애플리케이션 인터페이스
│   │   │       ├── __init__.py
│   │   │       ├── email_service.py
│   │   │       ├── ai_service.py
│   │   │       └── public_data_service.py
│   │   ├── infrastructure/           # 인프라 계층
│   │   │   ├── database/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── postgresql/
│   │   │   │   │   ├── models.py
│   │   │   │   │   ├── repositories.py
│   │   │   │   │   └── connection.py
│   │   │   │   ├── mongodb/
│   │   │   │   │   ├── models.py
│   │   │   │   │   ├── repositories.py
│   │   │   │   │   └── connection.py
│   │   │   │   └── redis/
│   │   │   │       ├── session_manager.py
│   │   │   │       └── cache_manager.py
│   │   │   ├── external/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── firebase_auth.py
│   │   │   │   ├── public_data_api.py
│   │   │   │   ├── hyperclova_service.py
│   │   │   │   ├── stable_diffusion_service.py
│   │   │   │   └── map_api_service.py
│   │   │   ├── email/
│   │   │   │   ├── __init__.py
│   │   │   │   └── smtp_service.py
│   │   │   └── security/
│   │   │       ├── __init__.py
│   │   │       ├── jwt_handler.py
│   │   │       └── password_handler.py
│   │   ├── presentation/             # 프레젠테이션 계층 (API)
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── v1/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── business.py
│   │   │   │   │   ├── content.py
│   │   │   │   │   ├── analytics.py
│   │   │   │   │   └── public_data.py
│   │   │   │   └── middleware/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── auth_middleware.py
│   │   │   │       ├── cors_middleware.py
│   │   │   │       └── error_handler.py
│   │   │   └── schemas/              # Pydantic 스키마
│   │   │       ├── __init__.py
│   │   │       ├── auth_schemas.py
│   │   │       ├── business_schemas.py
│   │   │       └── content_schemas.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   └── database.py
│   │   └── main.py                   # FastAPI 애플리케이션 진입점
│   ├── tests/                        # 테스트 (TDD)
│   │   ├── unit/                     # 단위 테스트
│   │   │   ├── domain/
│   │   │   │   ├── test_entities/
│   │   │   │   ├── test_services/
│   │   │   │   └── test_value_objects/
│   │   │   ├── application/
│   │   │   │   └── test_use_cases/
│   │   │   └── infrastructure/
│   │   │       ├── test_database/
│   │   │       └── test_external/
│   │   ├── integration/              # 통합 테스트
│   │   │   ├── test_api/
│   │   │   ├── test_database/
│   │   │   └── test_external_services/
│   │   ├── e2e/                      # 엔드투엔드 테스트
│   │   │   └── test_user_flows/
│   │   ├── fixtures/                 # 테스트 픽스처
│   │   │   ├── __init__.py
│   │   │   ├── database_fixtures.py
│   │   │   └── mock_data.py
│   │   └── conftest.py              # Pytest 설정
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/                         # React 프론트엔드
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/               # 재사용 가능한 컴포넌트
│   │   │   ├── common/
│   │   │   │   ├── Layout.tsx
│   │   │   │   ├── Navigation.tsx
│   │   │   │   ├── Loading.tsx
│   │   │   │   └── ErrorBoundary.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── SignupForm.tsx
│   │   │   │   └── SocialLogin.tsx
│   │   │   ├── business/
│   │   │   │   ├── BusinessForm.tsx
│   │   │   │   ├── CategorySelector.tsx
│   │   │   │   └── LocationPicker.tsx
│   │   │   ├── map/
│   │   │   │   ├── MapContainer.tsx
│   │   │   │   ├── MarkerLayer.tsx
│   │   │   │   └── RadiusSelector.tsx
│   │   │   ├── analytics/
│   │   │   │   ├── TargetChart.tsx
│   │   │   │   ├── DemographicChart.tsx
│   │   │   │   └── PerformanceChart.tsx
│   │   │   └── content/
│   │   │       ├── ContentGenerator.tsx
│   │   │       ├── ContentPreview.tsx
│   │   │       ├── ContentEditor.tsx
│   │   │       └── ContentDownload.tsx
│   │   ├── pages/                    # 페이지 컴포넌트
│   │   │   ├── Home.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Signup.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── BusinessSetup.tsx
│   │   │   ├── TargetAnalysis.tsx
│   │   │   ├── ContentGeneration.tsx
│   │   │   └── Analytics.tsx
│   │   ├── hooks/                    # 커스텀 훅
│   │   │   ├── useAuth.ts
│   │   │   ├── useBusinessData.ts
│   │   │   ├── useContentGeneration.ts
│   │   │   └── useAnalytics.ts
│   │   ├── services/                 # API 서비스
│   │   │   ├── api.ts
│   │   │   ├── authService.ts
│   │   │   ├── businessService.ts
│   │   │   ├── contentService.ts
│   │   │   └── analyticsService.ts
│   │   ├── utils/                    # 유틸리티 함수
│   │   │   ├── constants.ts
│   │   │   ├── formatters.ts
│   │   │   ├── validators.ts
│   │   │   └── helpers.ts
│   │   ├── types/                    # TypeScript 타입 정의
│   │   │   ├── auth.ts
│   │   │   ├── business.ts
│   │   │   ├── content.ts
│   │   │   └── analytics.ts
│   │   ├── store/                    # 상태 관리 (Context API)
│   │   │   ├── AuthContext.tsx
│   │   │   ├── BusinessContext.tsx
│   │   │   └── ContentContext.tsx
│   │   ├── styles/                   # 스타일 (Chakra UI 테마)
│   │   │   ├── theme.ts
│   │   │   └── globals.css
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── tests/                        # 프론트엔드 테스트
│   │   ├── unit/                     # Jest 단위 테스트
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   ├── integration/              # React Testing Library
│   │   │   ├── auth/
│   │   │   ├── business/
│   │   │   └── content/
│   │   ├── e2e/                      # Cypress E2E 테스트
│   │   │   ├── auth.cy.ts
│   │   │   ├── business-setup.cy.ts
│   │   │   ├── content-generation.cy.ts
│   │   │   └── analytics.cy.ts
│   │   └── setup.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── cypress.config.ts
│   ├── Dockerfile
│   └── .env.example
├── infrastructure/                   # 인프라 설정
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   └── docker-compose.prod.yml
│   ├── pulumi/                       # AWS 배포 (영문 Description)
│   │   ├── __main__.py
│   │   ├── Pulumi.yaml
│   │   ├── requirements.txt
│   │   └── config/
│   │       ├── dev.yaml
│   │       └── prod.yaml
│   └── kubernetes/                   # 선택적 K8s 배포
│       ├── namespace.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
├── data/                            # 데이터 파일
│   ├── business_categories.json      # 업종 분류 데이터
│   ├── sample_data/                 # 테스트용 샘플 데이터
│   │   ├── users.json
│   │   ├── businesses.json
│   │   └── public_data.json
│   └── scripts/                     # 데이터 처리 스크립트
│       ├── import_categories.py
│       └── setup_sample_data.py
├── docs/                            # 문서
│   ├── README.md
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── TESTING.md
├── scripts/                         # 프로젝트 스크립트
│   ├── setup.sh                     # Linux/Mac 설정 스크립트
│   ├── setup.bat                    # Windows 설정 스크립트
│   ├── test.sh                      # 테스트 실행 스크립트
│   └── deploy.sh                    # 배포 스크립트
├── .github/                         # GitHub Actions CI/CD
│   └── workflows/
│       ├── backend-test.yml
│       ├── frontend-test.yml
│       └── deploy.yml
├── .gitignore
├── README.md
└── docker-compose.yml               # 개발 환경용
```

## 핵심 설계 원칙

### 1. Clean Architecture 적용
- **Domain Layer**: 비즈니스 로직과 엔티티 (프레임워크 독립적)
- **Application Layer**: 유스케이스와 애플리케이션 서비스
- **Infrastructure Layer**: 외부 시스템과의 연동 (DB, API, 파일시스템)
- **Presentation Layer**: API 엔드포인트와 HTTP 처리

### 2. SOLID 원칙 준수
- **단일 책임 원칙**: 각 클래스와 모듈은 하나의 책임만
- **개방/폐쇄 원칙**: 확장에는 열려있고 수정에는 닫혀있음
- **리스코프 치환 원칙**: 인터페이스 구현체는 상호 교체 가능
- **인터페이스 분리 원칙**: 클라이언트는 사용하지 않는 인터페이스에 의존하지 않음
- **의존성 역전 원칙**: 추상화에 의존하고 구체화에 의존하지 않음

### 3. TDD 구조
- **테스트 먼저 작성**: 모든 기능은 테스트 케이스부터 시작
- **계층별 테스트**: Unit → Integration → E2E 순서로 테스트
- **모의 객체 활용**: 외부 의존성은 Mock으로 처리

## 주요 기술 결정사항

### Backend (FastAPI)
- **ORM**: SQLAlchemy (PostgreSQL), Motor (MongoDB)
- **캐싱**: Redis (세션, 데이터 캐싱)
- **인증**: JWT + Firebase Auth
- **AI/ML**: LangChain (HyperCLOVA), scikit-learn, Stable Diffusion
- **테스트**: Pytest, Pytest-asyncio

### Frontend (React + TypeScript)
- **UI Framework**: Chakra UI (반응형 디자인)
- **상태 관리**: Context API + useReducer
- **지도**: Leaflet + 카카오/네이버 지도 API
- **차트**: Recharts
- **테스트**: Jest, React Testing Library, Cypress
- **빌드**: Vite

### 인프라
- **컨테이너**: Docker + Docker Compose
- **배포**: Pulumi (AWS) 또는 Heroku/Render
- **CI/CD**: GitHub Actions
- **모니터링**: 로그 수집 및 성능 모니터링

## 개발 순서 (TDD 기반)

1. **Domain Entities 및 Value Objects** (테스트 먼저)
2. **Repository Interfaces** (테스트 먼저)
3. **Use Cases** (테스트 먼저)
4. **Infrastructure Implementation** (테스트 먼저)
5. **API Endpoints** (테스트 먼저)
6. **Frontend Components** (테스트 먼저)
7. **Integration Tests**
8. **E2E Tests**

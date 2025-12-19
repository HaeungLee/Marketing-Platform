# 📊 마케팅 플랫폼 리팩토링 분석 보고서

**작성일**: 2025-12-20
**프로젝트**: AI-Powered Marketing Platform
**분석 범위**: 전체 프로젝트 (Backend + Frontend)

---

## 📌 개요

전체적으로 **Clean Architecture**와 **DDD(Domain-Driven Design)** 원칙을 잘 따르고 있는 프로젝트입니다.
하지만 몇 가지 리팩토링이 필요한 부분들을 발견했습니다.

**프로젝트 통계**:
- Backend: 78개 Python 파일
- Frontend: 35개 TypeScript/TSX 파일
- Architecture: 4-Layer Clean Architecture (Domain, Application, Infrastructure, Presentation)
- 현재 완성도: ~68% (Mock 데이터 의존성으로 인한)

---

## 🔴 1. 중복 코드 제거 필요 (우선순위: **높음**)

### 문제: 중복된 Content Router 파일들

현재 3개의 거의 동일한 content 라우터가 존재합니다:

| 파일 | 라인 수 | 상태 |
|------|---------|------|
| `backend/src/presentation/api/v1/content.py` | 703줄 | ✅ 사용 중 |
| `backend/src/presentation/api/v1/content_backup.py` | 297줄 | ❌ 미사용 |
| `backend/src/presentation/api/v1/content_simple.py` | 138줄 | ❌ 미사용 |

**현재 상태**:
- `main.py:28`에서 `content.py`만 import하여 사용
- `content_backup.py`와 `content_simple.py`는 dead code

**리팩토링 권장사항**:
```bash
# 불필요한 파일 삭제
rm backend/src/presentation/api/v1/content_backup.py
rm backend/src/presentation/api/v1/content_simple.py
```

**예상 효과**:
- 코드베이스 정리: ~435줄 감소
- 유지보수 부담 감소
- 개발자 혼란 방지

---

## 🟡 2. Import 경로 불일치 (우선순위: **중간**)

### 문제: 일관성 없는 import 경로

**올바른 예시 (content.py)**:
```python
from src.application.interfaces.ai_service import AIService
from src.infrastructure.ai.gemini_service import GeminiService
```

**잘못된 예시 (content_backup.py, content_simple.py)**:
```python
from application.interfaces.ai_service import AIService  # ❌ src. 누락
from infrastructure.ai.gemini_service import GeminiService  # ❌ src. 누락
```

**리팩토링 권장사항**:
1. 모든 import를 `src.`로 시작하는 **절대 경로**로 통일
2. 중복 파일 삭제 후 남은 파일들에서 import 경로 검증
3. `pyproject.toml` 또는 `setup.py`에서 패키지 루트 명확히 설정

**영향받는 파일들**:
- `backend/src/presentation/api/v1/content_backup.py`
- `backend/src/presentation/api/v1/content_simple.py`
- (삭제 예정이므로 추가 작업 불필요)

---

## 🟠 3. Mock 데이터 의존성 제거 (우선순위: **높음**)

### 문제: 프론트엔드에 하드코딩된 Mock 데이터

**Mock 데이터 사용 파일들**:

| 파일 | 라인 | 내용 |
|------|------|------|
| `CommercialAnalysisPage.tsx` | 98-100 | 45개 가짜 상가 데이터 |
| `TargetInsightsPage.tsx` | - | mockLocationData |
| `TrendAnalysisPage.tsx` | - | 가짜 트렌드 데이터 |

**예시 코드 (CommercialAnalysisPage.tsx:98-100)**:
```typescript
// API 실패 시 풍부한 mockup 데이터 제공
const mockNearbyStores: BusinessStore[] = Array.from({ length: 45 }, (_, i) => {
  const storeTypes = businessType ? [businessType] : [
    "일반음식점", "카페", "편의점", "미용실", "의류",
    "치킨", "피자", "족발·보쌈", ...
  ];
  // ... 45개의 가짜 데이터 생성
});
```

**문제점**:
- 사용자가 실제 데이터와 가짜 데이터를 구분하기 어려움
- 프로덕션에서 API 실패 시 잘못된 정보 제공 가능성
- 테스트 데이터와 프로덕션 코드가 혼재

**리팩토링 권장사항**:

### 단기 (즉시 적용)
```typescript
// 개선된 에러 처리 - API 실패 시
catch (error) {
  console.error("상권 분석 데이터 로딩 실패:", error);

  toast({
    title: "데이터를 불러올 수 없습니다",
    description: "공공데이터 API 연결에 실패했습니다. 잠시 후 다시 시도해주세요.",
    status: "error",
    duration: 5000,
  });

  setNearbyStores([]);
  setStatistics(null);
}
```

### 중기 (공공데이터 API 완전 통합 확인)
- 공공데이터포털 API 키 확인
- `businessStoreService` 안정성 검증
- 에러 핸들링 강화

### 장기 (테스트 환경 분리)
```typescript
// __mocks__/businessStoreData.ts (별도 파일)
export const MOCK_STORES = [...];

// CommercialAnalysisPage.tsx
import { MOCK_STORES } from '../__mocks__/businessStoreData';

// 개발 환경에서만 사용
if (process.env.NODE_ENV === 'development' && import.meta.env.VITE_USE_MOCK) {
  setNearbyStores(MOCK_STORES);
}
```

---

## 🔵 4. TODO 항목 처리 (우선순위: **중간**)

### 발견된 TODO 항목들

#### 4.1 Redis Rate Limiting 미구현
**파일**: `backend/src/main.py:123`
```python
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window,
    redis_client=None,  # TODO: Redis 연결 시 추가
    exclude_paths=["/health", "/docs", "/redoc", "/openapi.json", "/static"],
    enabled=settings.rate_limit_enabled
)
```

**개선안**:
```python
# Redis 연결 추가
from redis.asyncio import Redis

async def get_redis_client() -> Redis:
    return await Redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True
    )

# main.py에서 사용
@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_client()

app.add_middleware(
    RateLimitMiddleware,
    redis_client=app.state.redis,  # ✅ Redis 클라이언트 전달
    ...
)
```

#### 4.2 Business API 미완성 엔드포인트
**파일**: `backend/src/presentation/api/v1/business.py`

**라인 89, 108, 127**:
```python
@router.get("/businesses/{business_id}")
async def get_business(business_id: str):
    # TODO: 실제 구현 필요
    pass

@router.put("/businesses/{business_id}")
async def update_business(business_id: str, business_data: dict):
    # TODO: 실제 구현 필요
    pass

@router.delete("/businesses/{business_id}")
async def delete_business(business_id: str):
    # TODO: 실제 구현 필요 (JWT 토큰에서 사용자 ID 추출)
    pass
```

**개선안**:
```python
from src.domain.repositories.business_repository import BusinessRepository
from src.infrastructure.security.jwt import get_current_user

@router.get("/businesses/{business_id}")
async def get_business(
    business_id: str,
    db: AsyncSession = Depends(get_db)
):
    """비즈니스 정보 조회"""
    repository = BusinessRepository(db)
    business = await repository.get_by_id(business_id)

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    return business

@router.put("/businesses/{business_id}")
async def update_business(
    business_id: str,
    business_data: BusinessUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """비즈니스 정보 수정"""
    repository = BusinessRepository(db)
    business = await repository.get_by_id(business_id)

    # 권한 확인
    if business.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated = await repository.update(business_id, business_data.dict())
    return updated

@router.delete("/businesses/{business_id}")
async def delete_business(
    business_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """비즈니스 삭제"""
    repository = BusinessRepository(db)
    business = await repository.get_by_id(business_id)

    # 권한 확인
    if business.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await repository.delete(business_id)
    return {"message": "Business deleted successfully"}
```

---

## 🟢 5. 코드 품질 개선 (우선순위: **낮음**)

### 5.1 중복된 AI 서비스 초기화

**문제**: `content.py`에 2개의 Dependency Injection 함수 존재

```python
def get_ai_service() -> AIService:  # 라인 110
    """AI 서비스 의존성 주입"""
    from src.config.settings import settings
    api_key = os.getenv("GOOGLE_API_KEY", settings.google_api_key)
    try:
        from src.infrastructure.ai.gemini_service import GeminiService
        return GeminiService(api_key)
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"AI 서비스를 사용할 수 없습니다: {str(e)}")

def get_gemini_service():  # 라인 123
    """Gemini 서비스 의존성 주입"""
    from src.config.settings import settings
    api_key = os.getenv("GOOGLE_API_KEY", settings.google_api_key)
    # ... 거의 동일한 로직
```

**개선안**: 하나의 함수로 통합
```python
from functools import lru_cache
from typing import Protocol

class AIServiceProtocol(Protocol):
    """AI 서비스 인터페이스"""
    async def generate_content(self, **kwargs): ...
    async def generate_image(self, **kwargs): ...
    async def generate_hashtags(self, **kwargs): ...

@lru_cache()
def get_ai_service_instance() -> AIServiceProtocol:
    """싱글톤 AI 서비스 인스턴스 생성"""
    from src.config.settings import settings
    from src.infrastructure.ai.gemini_service import GeminiService

    api_key = os.getenv("GOOGLE_API_KEY", settings.google_api_key)
    if not api_key:
        raise ValueError("Google API key not configured")

    return GeminiService(api_key)

def get_ai_service() -> AIServiceProtocol:
    """FastAPI 의존성 주입용"""
    try:
        return get_ai_service_instance()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI 서비스를 초기화할 수 없습니다: {str(e)}"
        )
```

### 5.2 하드코딩된 데이터를 상수로 분리

**문제**: `CommercialAnalysisPage.tsx:53-59`
```typescript
const POPULAR_LOCATIONS: LocationCoordinates[] = [
  { lat: 37.5665, lng: 126.9780, name: "서울역" },
  { lat: 37.5662, lng: 126.9784, name: "명동" },
  { lat: 37.4979, lng: 127.0276, name: "강남역" },
  { lat: 37.5563, lng: 126.9233, name: "홍대입구" },
  { lat: 37.5443, lng: 127.0557, name: "건대입구" },
];
```

**개선안**: 별도 상수 파일로 분리
```typescript
// frontend/src/constants/locations.ts
export interface LocationCoordinates {
  lat: number;
  lng: number;
  name: string;
  region: string;
}

export const SEOUL_LANDMARKS: LocationCoordinates[] = [
  { lat: 37.5665, lng: 126.9780, name: "서울역", region: "중구" },
  { lat: 37.5662, lng: 126.9784, name: "명동", region: "중구" },
  { lat: 37.4979, lng: 127.0276, name: "강남역", region: "강남구" },
  { lat: 37.5563, lng: 126.9233, name: "홍대입구", region: "마포구" },
  { lat: 37.5443, lng: 127.0557, name: "건대입구", region: "광진구" },
];

export const BUSAN_LANDMARKS: LocationCoordinates[] = [
  { lat: 35.1581, lng: 129.0598, name: "서면", region: "부산진구" },
  { lat: 35.1796, lng: 129.0756, name: "해운대", region: "해운대구" },
];

// CommercialAnalysisPage.tsx에서 사용
import { SEOUL_LANDMARKS } from "../constants/locations";

const [selectedLocation, setSelectedLocation] = useState<LocationCoordinates>(
  SEOUL_LANDMARKS[2] // 강남역
);
```

### 5.3 매직 넘버 제거

**문제**: 여러 곳에 숫자가 하드코딩됨
```typescript
// CommercialAnalysisPage.tsx
const [radius, setRadius] = useState(1000);  // 1000이 무엇을 의미하는지 불명확

// content.py
hashtag_count: int = Field(10, ge=1, le=30, description="생성할 해시태그 최대 개수")
```

**개선안**:
```typescript
// constants/businessAnalysis.ts
export const DEFAULT_SEARCH_RADIUS = 1000; // meters
export const MIN_SEARCH_RADIUS = 100;
export const MAX_SEARCH_RADIUS = 5000;

export const HASHTAG_LIMITS = {
  MIN: 1,
  DEFAULT: 10,
  MAX: 30,
} as const;

// 사용 예시
const [radius, setRadius] = useState(DEFAULT_SEARCH_RADIUS);
```

---

## 📋 리팩토링 우선순위 요약

### 🚨 즉시 처리 (High Priority)
1. **중복 파일 삭제**
   - `content_backup.py`, `content_simple.py` 제거
   - 예상 소요 시간: 5분
   - 영향도: 낮음 (사용되지 않는 파일)

2. **Mock 데이터 제거/분리**
   - Frontend fallback UI로 교체
   - Mock 데이터를 테스트 전용으로 분리
   - 예상 소요 시간: 2-3시간
   - 영향도: 높음 (사용자 경험 개선)

### ⚠️ 단기 처리 (Medium Priority)
3. **Import 경로 통일**
   - 모든 파일에서 `src.` prefix 사용
   - 예상 소요 시간: 1시간
   - 영향도: 중간 (코드 일관성)

4. **TODO 항목 처리**
   - Redis Rate Limiting 구현
   - Business API CRUD 완성
   - JWT 인증 미들웨어 통합
   - 예상 소요 시간: 1-2일
   - 영향도: 높음 (기능 완성도)

### ✅ 장기 개선 (Low Priority)
5. **의존성 주입 통합**
   - AI 서비스 초기화 로직 단일화
   - 예상 소요 시간: 2-3시간
   - 영향도: 낮음 (코드 품질)

6. **상수 분리**
   - 하드코딩된 데이터를 별도 파일로 관리
   - 매직 넘버 제거
   - 예상 소요 시간: 3-4시간
   - 영향도: 낮음 (유지보수성)

7. **테스트 커버리지 확대**
   - Integration 테스트 추가
   - E2E 테스트 추가
   - 예상 소요 시간: 1주일
   - 영향도: 중간 (품질 보증)

---

## 💡 추가 발견사항

### ✅ 프로젝트 장점

1. **아키텍처**
   - Clean Architecture 원칙 잘 준수
   - 계층 간 명확한 분리 (Domain, Application, Infrastructure, Presentation)
   - DDD 패턴 적용 (Entities, Value Objects, Repositories)

2. **보안**
   - Rate Limiting 미들웨어 구현
   - Security Headers 적용
   - JWT 인증 시스템
   - CORS 환경별 설정
   - 비밀번호 해싱 (bcrypt)

3. **로깅 & 모니터링**
   - 구조화된 로깅 시스템
   - Request ID 추적
   - 성능 메트릭 수집
   - Discord Webhook 알림

4. **타입 안정성**
   - Python Type Hints 전반적 사용
   - TypeScript 전체 적용
   - Pydantic 스키마 검증

5. **개발 환경**
   - Docker Compose 오케스트레이션
   - Health Check 엔드포인트
   - 환경별 설정 분리 (dev/staging/prod)

### ⚠️ 개선 가능 영역

1. **프로덕션 완성도**: ~68%
   - Mock 데이터 의존성으로 인한 낮은 완성도
   - 실제 공공데이터 API 완전 통합 필요

2. **MCP 서버 통신**
   - Subprocess 기반 통신으로 불안정
   - HTTP/WebSocket으로 마이그레이션 권장

3. **문서화**
   - 한글/영어 주석 혼용
   - API 문서 자동화 필요 (OpenAPI 활용)
   - 아키텍처 다이어그램 부재

4. **테스트**
   - Unit 테스트는 존재하지만 커버리지 불명확
   - Integration/E2E 테스트 부족
   - CI/CD 파이프라인 미구축

5. **에러 처리**
   - 일부 엔드포인트에서 일관성 없는 에러 응답
   - 전역 예외 핸들러 개선 필요

---

## 🎯 실행 계획 (Action Plan)

### Week 1: 긴급 리팩토링
- [ ] Day 1: 중복 파일 삭제 (`content_backup.py`, `content_simple.py`)
- [ ] Day 2-3: Mock 데이터 제거 및 Fallback UI 구현
- [ ] Day 4-5: Import 경로 통일 및 검증

### Week 2: 기능 완성
- [ ] Day 1-2: Redis Rate Limiting 완전 구현
- [ ] Day 3-4: Business API CRUD 엔드포인트 완성
- [ ] Day 5: JWT 인증 미들웨어 통합 테스트

### Week 3: 코드 품질
- [ ] Day 1-2: AI 서비스 의존성 주입 통합
- [ ] Day 3-4: 상수 분리 및 매직 넘버 제거
- [ ] Day 5: 코드 리뷰 및 문서화 업데이트

### Week 4: 테스트 & 안정화
- [ ] Day 1-3: Integration 테스트 작성
- [ ] Day 4-5: E2E 테스트 시나리오 구현 및 실행

---

## 📚 참고 자료

### 관련 파일들

**중복 파일**:
- `backend/src/presentation/api/v1/content.py`
- `backend/src/presentation/api/v1/content_backup.py`
- `backend/src/presentation/api/v1/content_simple.py`

**Mock 데이터 사용**:
- `frontend/src/pages/CommercialAnalysisPage.tsx`
- `frontend/src/pages/TargetInsightsPage.tsx`
- `frontend/src/pages/TrendAnalysisPage.tsx`

**TODO 포함 파일**:
- `backend/src/main.py` (Redis)
- `backend/src/presentation/api/v1/business.py` (CRUD)

### 아키텍처 문서
- Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- DDD: https://martinfowler.com/bliki/DomainDrivenDesign.html
- FastAPI Best Practices: https://github.com/zhanymkanov/fastapi-best-practices

---

**보고서 작성**: Claude Sonnet 4.5
**분석 도구**: Claude Code CLI
**다음 리뷰 예정일**: 2026-01-03

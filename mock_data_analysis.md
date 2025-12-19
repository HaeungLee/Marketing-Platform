# 🎭 Mock 데이터 분석 보고서

**작성일**: 2025-12-20
**대상**: 긴급 리팩토링 준비
**우선순위**: 🔴 높음

---

## 📍 Mock 데이터 위치 및 상세 내역

### 1️⃣ CommercialAnalysisPage.tsx (상권 분석 페이지)

**파일 경로**: `frontend/src/pages/CommercialAnalysisPage.tsx`

#### Mock 데이터 내용

##### 📦 1.1 Mock 상가 데이터 (라인 98-136)
```typescript
// API 실패 시 45개의 가짜 상가 생성
const mockNearbyStores: BusinessStore[] = Array.from({ length: 45 }, (_, i) => {
  const storeTypes = businessType ? [businessType] : [
    "일반음식점", "카페", "편의점", "미용실", "의류", "치킨", "피자",
    "족발·보쌈", "중국집", "분식", "도시락", "빵집", "약국", "화장품", "휴대폰"
  ];

  const randomType = storeTypes[Math.floor(Math.random() * storeTypes.length)];

  return {
    id: i + 1,
    store_number: `STORE_${String(i + 1).padStart(6, '0')}`,
    store_name: `${[상호명 배열]} ${selectedLocation.name}점`,
    business_code: `BIZ_${String(i + 1).padStart(4, '0')}`,
    business_name: randomType,
    longitude: selectedLocation.lng + (Math.random() - 0.5) * 0.02,
    latitude: selectedLocation.lat + (Math.random() - 0.5) * 0.02,
    distance: Math.floor(Math.random() * radius) + 50,
    jibun_address: `서울특별시 ${selectedLocation.name} ${Math.floor(Math.random() * 500) + 1}번지`,
    road_address: `서울특별시 ${selectedLocation.name} ${["중앙로", "번영로", "평화로", "희망로", "미래로"]} ${Math.floor(Math.random() * 200) + 1}`,
    // ... 더 많은 가짜 필드
  };
});
```

**생성되는 Mock 데이터**:
- ✅ 45개의 가짜 상가
- ✅ 랜덤한 상호명 (스타벅스, GS25, 헤어샵 등)
- ✅ 가짜 좌표 (실제 위치 ±0.01° 랜덤)
- ✅ 가짜 주소 (서울특별시 강남구 중앙로 123)
- ✅ 가짜 거리 (50m ~ radius)

##### 📊 1.2 Mock 통계 데이터 (라인 141-172)
```typescript
// 업종별 통계 mockup
const businessTypeStats = [
  { business_name: "일반음식점", store_count: 1876, percentage: 28.5 },
  { business_name: "카페", store_count: 1234, percentage: 18.7 },
  { business_name: "편의점", store_count: 892, percentage: 13.5 },
  { business_name: "미용실", store_count: 723, percentage: 11.0 },
  // ... 10개 업종
];

// 지역별 통계 mockup
const regionStats = [
  { region_name: "강남구", store_count: 2847 },
  { region_name: "송파구", store_count: 2234 },
  // ... 8개 지역
];
```

**생성되는 Mock 데이터**:
- ✅ 10개 업종별 가짜 통계
- ✅ 8개 지역별 가짜 통계
- ✅ 고정된 숫자 (1876개, 2847개 등)

##### 🗺️ 1.3 Mock 지역 분석 (라인 191-234)
```typescript
const generateMockRegionAnalysis = async (stores: BusinessStore[]): Promise<RegionAnalysis[]> => {
  // 지역별로 그룹화
  const regionGroups: { [key: string]: BusinessStore[] } = {};

  // 경쟁 수준 계산
  let competitionLevel: 'LOW' | 'MEDIUM' | 'HIGH' = 'LOW';
  if (storeList.length > 15) competitionLevel = 'HIGH';
  else if (storeList.length > 8) competitionLevel = 'MEDIUM';

  // 트렌드 키워드 생성
  trends: topBusinessTypes.length > 0 ? topBusinessTypes : ["일반음식점", "카페", "편의점"],
};
```

**생성되는 Mock 데이터**:
- ✅ 지역별 경쟁 수준 (LOW/MEDIUM/HIGH)
- ✅ 평균 거리 계산
- ✅ 트렌드 키워드 (top 3 업종)

**발생 조건**: `catch (error)` 블록에서 API 호출 실패 시

---

### 2️⃣ TargetInsightsPage.tsx (타겟 인사이트 페이지)

**파일 경로**: `frontend/src/pages/TargetInsightsPage.tsx`

#### Mock 데이터 내용

##### 🎯 2.1 Mock 타겟 고객 데이터 (라인 101-123)
```typescript
setTargetData({
  primaryTarget: `${businessType === "카페" ? "20-35세 직장인" :
                 businessType === "일반음식점" ? "25-45세 가족층" :
                 businessType === "미용실" ? "20-40세 여성층" :
                 businessType === "편의점" ? "전 연령층" :
                 "20-40세 트렌드 추구층"}`,

  secondaryTarget: `${업종별 보조 타겟}`,

  strategy: businessType === "카페" ?
    ["인스타그램 마케팅", "디저트 이벤트", "모닝커피 할인", "스터디 공간 제공", "원두 판매"] :
    ["네이버 플레이스 관리", "점심특선 프로모션", ...],

  confidence: Math.floor(Math.random() * 15) + 80, // 80-95% 랜덤
  dataSource: `${region} 지역 ${businessType} 업종 분석 (공공데이터 기반)`
});
```

**생성되는 Mock 데이터**:
- ✅ 업종별 주요/보조 타겟
- ✅ 5개의 마케팅 전략
- ✅ 랜덤 신뢰도 (80-95%)
- ✅ 가짜 데이터 출처 표시

##### ⏰ 2.2 Mock 마케팅 타이밍 데이터 (라인 125-155)
```typescript
setTimingData({
  bestDays: businessType === "카페" ?
    ["월요일", "화요일", "금요일", "토요일"] :
    ["금요일", "토요일", "일요일"],

  peakHours: businessType === "카페" ?
    ["07:30-09:00", "12:00-13:30", "15:00-17:00", "19:00-21:00"] :
    ["11:30-13:30", "17:30-19:30", "19:00-21:00"],

  seasonalTrends: businessType === "카페" ?
    ["가을/겨울 음료 매출 증가", "여름 아이스음료 성수기", "봄 디저트 카페 인기", "연말 선물세트 판매"] :
    [...],

  confidence: Math.floor(Math.random() * 10) + 85, // 85-95%
  dataSource: `Google Trends + ${region} 지역 소비패턴 분석`
});
```

**생성되는 Mock 데이터**:
- ✅ 업종별 최적 요일
- ✅ 피크 시간대 (4개)
- ✅ 계절별 트렌드 (4개)
- ✅ 랜덤 신뢰도 (85-95%)

##### 🏪 2.3 Mock 입지 분석 데이터 (라인 158-266)
```typescript
const mockLocationData: RealLocationData[] = [
  {
    area: "강남구",
    totalStores: 2847,
    businessDensity: businessType === "카페" ? 156 :
                    businessType === "일반음식점" ? 312 :
                    businessType === "미용실" ? 89 :
                    businessType === "편의점" ? 67 : 134,
    competitionLevel: 'HIGH',
    dominantBusinessTypes: businessType === "카페" ? [
      { type: "프랜차이즈 카페", count: 89, percentage: 57.1 },
      { type: "독립 카페", count: 45, percentage: 28.8 },
      { type: "디저트 카페", count: 22, percentage: 14.1 }
    ] : [...],
    recommendationScore: 85,
    insights: [
      "고소득층 밀집지역으로 프리미엄 서비스 선호",
      "유동인구가 많아 브랜드 인지도 향상 효과 큼",
      "임대료 높지만 안정적인 매출 기대 가능"
    ]
  },
  // 홍대, 명동, 건대, 신촌 총 5개 지역
];
```

**생성되는 Mock 데이터**:
- ✅ 5개 주요 지역별 분석
- ✅ 업종별 상가 밀도 (고정값)
- ✅ 경쟁 수준 (HIGH/MEDIUM)
- ✅ 주요 업종 분포 (3개)
- ✅ 추천 점수 (85, 78, 72, 69, 66)
- ✅ 3개의 인사이트

##### 💰 2.4 Mock 투자 수익률 데이터 (라인 710-758)
```typescript
// 예상 월 매출
{businessType === "카페" ? "850만원" :
 businessType === "일반음식점" ? "1,200만원" :
 businessType === "미용실" ? "650만원" :
 businessType === "편의점" ? "900만원" : "750만원"}

// 손익분기점
{businessType === "카페" ? "7개월" :
 businessType === "일반음식점" ? "5개월" :
 businessType === "미용실" ? "8개월" :
 businessType === "편의점" ? "6개월" : "7개월"}

// 성공 확률
Math.floor(Math.random() * 20) + 70  // 70-90% 랜덤
```

**발생 조건**:
1. `/api/v1/insights/target-customer` API 실패 시
2. `/api/v1/insights/marketing-timing` API 실패 시
3. `analyzeRealLocations()` 함수에서 `businessStoreService` API 실패 시 (라인 339-369)

---

### 3️⃣ TrendAnalysisPage.tsx (트렌드 분석 페이지)

**파일 경로**: `frontend/src/pages/TrendAnalysisPage.tsx`

#### Mock 데이터 내용

##### 📈 3.1 Mock Google Trends 데이터 (라인 97-116)
```typescript
const mockTrendData: TrendData = {
  keyword: selectedBusinessType,
  interest: Math.floor(Math.random() * 100) + 1,  // 1-100 랜덤
  relatedQueries: [
    `${selectedBusinessType} 창업`,
    `${selectedBusinessType} 트렌드`,
    `${selectedBusinessType} 매출`,
    `${selectedBusinessType} 위치`,
  ],
  regions: [
    { name: "서울", value: Math.floor(Math.random() * 100) + 1 },
    { name: "경기", value: Math.floor(Math.random() * 100) + 1 },
    { name: "부산", value: Math.floor(Math.random() * 100) + 1 },
    { name: "대구", value: Math.floor(Math.random() * 100) + 1 },
  ],
  timeData: Array.from({ length: 12 }, (_, i) => ({
    date: `2024-${(i + 1).toString().padStart(2, '0')}`,
    value: Math.floor(Math.random() * 100) + 1,  // 1-100 랜덤
  })),
};
```

**생성되는 Mock 데이터**:
- ✅ 전체 관심도 (1-100 랜덤)
- ✅ 4개 관련 검색어
- ✅ 4개 지역별 관심도 (각각 1-100 랜덤)
- ✅ 12개월 월별 트렌드 (각각 1-100 랜덤)

##### 💡 3.2 Mock 비즈니스 인사이트 (라인 141-186)
```typescript
const generateBusinessInsights = async (trends: TrendData): Promise<BusinessInsight[]> => {
  const currentInterest = trends.interest;
  let marketState: 'HOT' | 'RISING' | 'STABLE' | 'DECLINING' = 'STABLE';

  if (currentInterest > 80) marketState = 'HOT';
  else if (currentInterest > 60) marketState = 'RISING';
  else if (currentInterest < 30) marketState = 'DECLINING';

  // marketState에 따라 다른 추천사항 제공
  switch (marketState) {
    case 'HOT':
      recommendations.push("지금이 진입하기 좋은 시기입니다");
      recommendations.push("프리미엄 전략으로 차별화하세요");
      opportunities.push("높은 관심도로 인한 빠른 고객 유입");
      threats.push("경쟁 진입 가능성 높음");
      break;
    // ... 다른 경우들
  }
};
```

**생성되는 Mock 데이터**:
- ✅ 시장 상태 (HOT/RISING/STABLE/DECLINING)
- ✅ 2-3개의 추천사항
- ✅ 1-2개의 기회 요소
- ✅ 1개의 위험 요소
- ✅ 트렌드 점수 (1-100)

##### 🌍 3.3 Mock 지역별 결합 분석 (라인 188-247)
```typescript
const generateCombinedAnalysis = async (trends: TrendData): Promise<CombinedAnalysis[]> => {
  // 5개 주요 지역 순회
  for (const region of majorRegions) {
    try {
      // 실제 API 호출 시도
      const nearbyStores = await businessStoreService.getNearbyStores(...);

      // 시장 기회 점수 계산
      const marketOpportunity = Math.max(0, Math.min(100,
        (trendInterest * 0.7) + ((100 - (realStoreCount / 50 * 100)) * 0.3)
      ));

    } catch (error) {
      // API 실패 시 기본값 제공
      analysis.push({
        region: region.name,
        realStoreCount: 0,
        trendInterest: 0,
        marketOpportunity: 0,
        recommendation: "데이터 수집 중...",
        insights: ["분석 데이터를 준비 중입니다"],
      });
    }
  }
};
```

**생성되는 Mock 데이터** (API 실패 시):
- ✅ 5개 지역 각각 빈 데이터
- ✅ "데이터 수집 중..." 메시지

**발생 조건**:
- `generateCombinedAnalysis()` 함수에서 `businessStoreService.getNearbyStores()` 실패 시

---

## 🔍 Mock 데이터 사용 패턴 분석

### Pattern 1: Catch 블록에서 Fallback
```typescript
try {
  // 실제 API 호출
  const response = await businessStoreService.getNearbyStores(...);
} catch (error) {
  console.error("상권 분석 데이터 로딩 실패:", error);

  // ❌ 문제: 가짜 데이터를 그대로 표시
  const mockNearbyStores = [/* 45개 가짜 데이터 */];
  setNearbyStores(mockNearbyStores);

  // ⚠️ 경고 메시지만 표시
  toast({
    title: "데모 데이터 로드됨",
    description: "실제 API 연결이 실패하여 데모 데이터를 표시합니다.",
    status: "warning",
  });
}
```

### Pattern 2: 조건부 Mock 데이터 생성
```typescript
// 업종에 따라 다른 가짜 값 제공
businessDensity: businessType === "카페" ? 156 :
                businessType === "일반음식점" ? 312 :
                businessType === "미용실" ? 89 : 134
```

### Pattern 3: 랜덤 값 생성
```typescript
// 매번 다른 값을 보여줘서 "실제 같은" 느낌 제공
confidence: Math.floor(Math.random() * 15) + 80  // 80-95%
interest: Math.floor(Math.random() * 100) + 1    // 1-100
```

---

## ⚠️ Mock 데이터의 문제점

### 1. 사용자 혼란
- ❌ 사용자가 실제 데이터인지 가짜 데이터인지 구분하기 어려움
- ❌ "공공데이터 기반"이라고 표시되지만 실제로는 하드코딩된 값
- ❌ Toast 메시지는 3초 후 사라지므로 나중에 확인 불가

### 2. 데이터 신뢰도 문제
- ❌ 신뢰도가 "80-95%"로 표시되지만 랜덤 값
- ❌ "강남구 2847개 상가"가 고정값 (실제 데이터가 아님)
- ❌ 추천 점수가 매번 동일 (85, 78, 72, 69, 66)

### 3. 비즈니스 리스크
- ❌ 사용자가 가짜 데이터를 믿고 의사결정할 위험
- ❌ "카페 월 매출 850만원"은 검증되지 않은 추정치
- ❌ "손익분기점 7개월"도 근거 없는 값

### 4. 개발/테스트 혼재
- ❌ 프로덕션 코드에 테스트용 Mock 데이터 포함
- ❌ API 에러 핸들링이 Mock 데이터 표시로 대체
- ❌ 실제 API 문제를 숨기는 효과

---

## ✅ 수정 방향

### Option A: 완전 제거 (권장)
```typescript
catch (error) {
  console.error("상권 분석 데이터 로딩 실패:", error);

  // Mock 데이터 제거 - 대신 에러 상태 표시
  setNearbyStores([]);
  setError("공공데이터 API 연결에 실패했습니다.");

  toast({
    title: "데이터를 불러올 수 없습니다",
    description: "잠시 후 다시 시도해주세요.",
    status: "error",
    duration: 5000,
  });
}

// UI에서 에러 상태 표시
{error && (
  <Alert status="error">
    <AlertIcon />
    <AlertTitle>데이터 로딩 실패</AlertTitle>
    <AlertDescription>{error}</AlertDescription>
  </Alert>
)}

{nearbyStores.length === 0 && !loading && !error && (
  <Alert status="info">
    <AlertIcon />
    <AlertTitle>데이터가 없습니다</AlertTitle>
    <AlertDescription>다른 조건으로 검색해보세요.</AlertDescription>
  </Alert>
)}
```

### Option B: 테스트 모드로 분리
```typescript
// .env 파일에서 설정
VITE_USE_MOCK_DATA=false  // 프로덕션에서는 false

// 코드에서 사용
catch (error) {
  console.error("상권 분석 데이터 로딩 실패:", error);

  if (import.meta.env.VITE_USE_MOCK_DATA === 'true') {
    // 개발 환경에서만 Mock 데이터 사용
    const mockData = await import('../__mocks__/commercialData');
    setNearbyStores(mockData.nearbyStores);

    toast({
      title: "개발 모드",
      description: "Mock 데이터를 표시합니다 (VITE_USE_MOCK_DATA=true)",
      status: "info",
    });
  } else {
    // 프로덕션에서는 에러만 표시
    setError("데이터를 불러올 수 없습니다.");
  }
}
```

### Option C: 점진적 마이그레이션
1. **Week 1**: 에러 상태 UI 구현
2. **Week 2**: Mock 데이터를 별도 파일로 분리 (`__mocks__/` 폴더)
3. **Week 3**: 환경변수 기반 조건부 로딩
4. **Week 4**: 프로덕션에서 Mock 데이터 완전 제거

---

## 📊 영향도 분석

### 수정 시 영향받는 컴포넌트

| 파일 | Mock 데이터 라인 수 | 영향도 | 예상 작업 시간 |
|------|---------------------|--------|---------------|
| CommercialAnalysisPage.tsx | ~140줄 | 🔴 높음 | 2-3시간 |
| TargetInsightsPage.tsx | ~270줄 | 🔴 높음 | 3-4시간 |
| TrendAnalysisPage.tsx | ~80줄 | 🟡 중간 | 1-2시간 |
| **합계** | **~490줄** | - | **6-9시간** |

### 사용자 경험 변화

**현재 (Mock 데이터 사용)**:
1. API 실패 → Toast 경고 표시 (3초)
2. 가짜 데이터가 화면에 표시됨
3. 사용자는 데이터가 로드된 것으로 착각

**수정 후 (Option A 적용)**:
1. API 실패 → 에러 Alert 표시 (계속 유지)
2. 빈 화면 또는 "재시도" 버튼 표시
3. 사용자는 에러 상황을 명확히 인지

**수정 후 (Option B 적용)**:
1. 개발 환경: Mock 데이터 표시 (명확한 배너 표시)
2. 프로덕션: 에러 Alert 표시
3. 환경에 따른 명확한 구분

---

## 🎯 리팩토링 실행 계획

### Phase 1: 에러 처리 개선 (1-2일)
- [ ] 에러 상태 관리 추가 (`error`, `setError`)
- [ ] 에러 UI 컴포넌트 추가
- [ ] "재시도" 버튼 구현
- [ ] Loading/Error/Empty 상태 분리

### Phase 2: Mock 데이터 분리 (1-2일)
- [ ] `frontend/src/__mocks__/` 폴더 생성
- [ ] Mock 데이터를 별도 파일로 이동
  - `commercialData.mock.ts`
  - `targetInsights.mock.ts`
  - `trendAnalysis.mock.ts`
- [ ] TypeScript 타입 정의 추가

### Phase 3: 조건부 로딩 (1일)
- [ ] 환경변수 설정 (`VITE_USE_MOCK_DATA`)
- [ ] 개발/프로덕션 분기 로직 구현
- [ ] Mock 데이터 사용 시 명확한 배너 표시

### Phase 4: 프로덕션 배포 (1일)
- [ ] `.env.production`에서 `VITE_USE_MOCK_DATA=false` 설정
- [ ] 프로덕션 빌드 테스트
- [ ] 실제 API 연동 확인
- [ ] 에러 상황 시나리오 테스트

---

## 📝 체크리스트

리팩토링 전 확인사항:
- [ ] 백엔드 API 엔드포인트 동작 확인
- [ ] 공공데이터 API 키 유효성 확인
- [ ] 데이터베이스 상가 데이터 존재 여부 확인
- [ ] API 에러 로그 확인 (왜 Mock으로 폴백하는지)

리팩토링 후 확인사항:
- [ ] API 성공 시 실제 데이터 표시 확인
- [ ] API 실패 시 에러 메시지 표시 확인
- [ ] 개발 환경에서 Mock 데이터 사용 가능 확인
- [ ] 프로덕션 환경에서 Mock 데이터 미사용 확인
- [ ] 사용자가 에러 상황을 명확히 인지하는지 확인

---

**다음 단계**: Option A (완전 제거) 또는 Option B (테스트 모드 분리) 중 선택 후 진행

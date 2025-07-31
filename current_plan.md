# 🛠️ 마케팅 플랫폼 기술 구현 로드맵

## 📊 현재 상황 정확한 분석

### 실제 완성도 재평가: **68%**
- ✅ **완료된 부분**: FastAPI 백엔드 구조, React 프론트엔드 구조, Docker 환경, 기본 UI/UX
- ⚠️ **부분 완료**: 공공데이터 API 연동 (네트워크 이슈로 Mock 데이터 의존)
- ❌ **미완료**: Fabric.js 편집기, AI 상담 특화, 실데이터 파이프라인

### 핵심 문제점 식별
1. **Mock Data 의존도 90%**: 대부분의 분석이 가상 데이터 기반
2. **Fabric.js 구현 실패**: 3-4번 시도했으나 복잡한 편집 기능 미완성
3. **MCP 서버 연결 불안정**: subprocess 기반 임시 구현, 하드코딩된 경로
4. **AI 모델 범용성**: gemma3:27b가 범용 용도로만 사용됨

---

## 🎯 Phase별 구현 계획

### Phase 0: 기술 부채 해결 (1-2주)
**목표**: 현재 시스템의 불안정 요소 제거

#### 0.1 MCP 서버 통신 개선
```python
# 현재 문제: subprocess 기반 불안적 통신
# 개선방안: HTTP/WebSocket 기반 안정적 통신

class StableMCPConnector:
    def __init__(self):
        self.base_url = "http://localhost:3001"  # MCP 서버 HTTP 엔드포인트
        self.session = aiohttp.ClientSession()
    
    async def call_tool_stable(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """HTTP 기반 안정적 MCP 서버 통신"""
        try:
            async with self.session.post(
                f"{self.base_url}/tools/call",
                json={"tool": tool_name, "arguments": arguments},
                timeout=30
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise HTTPException(status_code=500, detail="MCP server unavailable")
        except aiohttp.ClientError:
            # 그래도 실패하면 DB 기반 분석으로 fallback
            return await self._database_based_analysis(tool_name, arguments)
```

#### 0.2 하드코딩 경로 제거
```python
# 현재 문제: 절대경로 하드코딩
# server_path: str = "d:/FinalProjects/Marketing-Platform/mcp-server"

# 개선방안: 설정 기반 동적 경로
class Settings:
    mcp_server_host: str = os.getenv("MCP_SERVER_HOST", "localhost")
    mcp_server_port: int = int(os.getenv("MCP_SERVER_PORT", "3001"))
    mcp_server_path: str = os.getenv("MCP_SERVER_PATH", "./mcp-server")
    database_url: str = os.getenv("DATABASE_URL", "postgresql://...")
```

#### 0.3 Mock 데이터 의존성 분석
```bash
# Mock 데이터 사용 현황 파악
grep -r "mock\|Mock\|MOCK" frontend/src --include="*.tsx" --include="*.ts"
grep -r "sample\|demo\|fake" backend/src --include="*.py"

# 발견된 Mock 데이터 파일들:
# - frontend/src/pages/CommercialAnalysisPage.tsx (45개 가상 상가)
# - frontend/src/pages/TargetInsightsPage.tsx (mockLocationData)
# - backend/tests/test_business_api_detailed_analysis.py
# - backend/src/application/services/insights_analysis_service.py (_mock_tool_call)
```

### Phase 1: 실데이터 전환 (2-3주)
**목표**: Mock 데이터를 실제 DB 데이터로 완전 교체

#### 1.1 데이터베이스 실데이터 적재
```python
# 현재 상태: load_sample_data.py로 샘플 데이터만 적재
# 목표: 실제 공공데이터 수집 및 적재

class RealDataPipeline:
    """실제 공공데이터 수집 및 적재 파이프라인"""
    
    async def collect_sbiz_data(self):
        """소상공인시장진흥공단 API에서 실데이터 수집"""
        endpoints = [
            "storeListInRadius",   # 반경내 상가 조회
            "storeListInDong",     # 행정동별 상가 조회  
            "storeListInUpjong",   # 업종별 상가 조회
        ]
        
        collected_data = []
        for endpoint in endpoints:
            try:
                data = await self._fetch_api_data(endpoint)
                if data and 'response' in data:
                    items = data['response']['body']['items']
                    collected_data.extend(items)
            except Exception as e:
                logger.warning(f"API {endpoint} 실패: {e}")
                continue
        
        # 수집된 데이터를 DB에 적재
        await self._bulk_insert_to_db(collected_data)
    
    async def collect_population_data(self):
        """공공데이터포털 인구통계 수집"""
        api_endpoint = "https://apis.data.go.kr/1741000/admmSexdAgePpltn"
        # 실제 API 키로 데이터 수집
        population_data = await self._fetch_population_api()
        await self._insert_population_to_db(population_data)
```

#### 1.2 Frontend Mock 데이터 제거
```typescript
// 현재: CommercialAnalysisPage.tsx에서 45개 가상 상가 생성
// Array.from({ length: 45 }, (_, i) => { ... })

// 개선: 실제 API 호출로 교체
const fetchRealNearbyStores = async () => {
  try {
    const response = await businessStoreService.getNearbyStores(
      selectedLocation.lat,
      selectedLocation.lng,
      1000, // 1km 반경
      businessType
    );
    
    // DB에서 실제 상가 데이터 조회
    setNearbyStores(response.stores);
    setRegionAnalysis(response.analysis);
    
  } catch (error) {
    // API 실패 시에만 제한된 fallback 데이터 사용
    logger.error("실데이터 조회 실패, 최소한의 fallback 사용");
  }
};
```

#### 1.3 데이터 품질 검증 시스템
```python
class DataQualityValidator:
    """수집된 데이터의 품질을 검증"""
    
    async def validate_business_data(self):
        """상가 데이터 품질 검사"""
        checks = [
            ("좌표 유효성", "SELECT COUNT(*) FROM business_stores WHERE latitude IS NULL OR longitude IS NULL"),
            ("주소 완성도", "SELECT COUNT(*) FROM business_stores WHERE road_address IS NULL AND land_address IS NULL"),
            ("업종 정보", "SELECT COUNT(*) FROM business_stores WHERE business_name IS NULL"),
            ("중복 데이터", "SELECT store_id, COUNT(*) FROM business_stores GROUP BY store_id HAVING COUNT(*) > 1")
        ]
        
        quality_report = {}
        for check_name, query in checks:
            result = await self._execute_check(query)
            quality_report[check_name] = result
            
        return quality_report
```

### Phase 2: Fabric.js 대안 검토 및 구현 (2-3주)
**목표**: 전단지 편집 기능 완전 구현

#### 2.1 Fabric.js 문제점 재분석
```typescript
// 기존 실패 원인 추적:
// 1. Canvas 크기 반응형 이슈
// 2. 모바일 터치 이벤트 충돌
// 3. 레이어 관리 복잡성
// 4. 텍스트 편집 상태 관리

// 실패했던 구현 패턴:
const problematicPatterns = {
  canvas_resize: "window resize 이벤트에서 canvas 크기 조정 실패",
  touch_events: "터치와 마우스 이벤트 동시 처리 충돌",
  state_management: "React state와 Fabric.js object state 동기화 실패"
};
```

#### 2.2 대안 기술 스택 검토
```typescript
interface EditorAlternatives {
  // Option 1: Konva.js + React-Konva (권장)
  konva: {
    pros: ["React 네이티브 지원", "모바일 친화적", "가벼움"],
    cons: ["학습곡선", "템플릿 시스템 별도 구축 필요"],
    complexity: "중간",
    timeline: "2-3주"
  },
  
  // Option 2: 단순화된 Fabric.js v6
  fabric_simplified: {
    pros: ["기존 코드 활용", "풍부한 기능"],
    cons: ["이전 실패 패턴", "복잡성"],
    complexity: "높음", 
    timeline: "3-4주"
  },
  
  // Option 3: HTML5 Canvas + Custom Editor
  custom_canvas: {
    pros: ["완전 제어", "가벼움"],
    cons: ["모든 기능 직접 구현", "시간 소요"],
    complexity: "매우 높음",
    timeline: "5-6주"
  }
}
```

#### 2.3 Konva.js 기반 편집기 구현 (권장안)
```typescript
// React-Konva 기반 전단지 편집기
interface FlyerEditorProps {
  width: number;
  height: number;
  onSave: (imageData: string) => void;
}

const KonvaFlyerEditor: React.FC<FlyerEditorProps> = ({ width, height, onSave }) => {
  const [elements, setElements] = useState<EditorElement[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const stageRef = useRef<Konva.Stage>(null);

  // 텍스트 추가
  const addText = useCallback(() => {
    const newText: TextElement = {
      id: `text-${Date.now()}`,
      type: 'text',
      x: 50,
      y: 50,
      text: '텍스트를 입력하세요',
      fontSize: 24,
      fill: '#000000'
    };
    setElements(prev => [...prev, newText]);
  }, []);

  // 이미지 추가
  const addImage = useCallback((imageUrl: string) => {
    const img = new Image();
    img.onload = () => {
      const newImage: ImageElement = {
        id: `image-${Date.now()}`,
        type: 'image',
        x: 100,
        y: 100,
        image: img,
        width: img.width,
        height: img.height
      };
      setElements(prev => [...prev, newImage]);
    };
    img.src = imageUrl;
  }, []);

  return (
    <div className="konva-editor">
      <div className="editor-toolbar">
        <Button onClick={addText}>📝 텍스트 추가</Button>
        <Button onClick={() => document.getElementById('image-input')?.click()}>
          🖼️ 이미지 추가
        </Button>
        <Button onClick={() => onSave(exportStage())}>💾 저장</Button>
      </div>
      
      <Stage 
        width={width} 
        height={height} 
        ref={stageRef}
        onMouseDown={checkDeselect}
      >
        <Layer>
          {elements.map(element => (
            element.type === 'text' ? (
              <Text
                key={element.id}
                {...element}
                draggable
                onClick={() => setSelectedId(element.id)}
              />
            ) : element.type === 'image' ? (
              <Image
                key={element.id}
                {...element}
                draggable
                onClick={() => setSelectedId(element.id)}
              />
            ) : null
          ))}
          
          {selectedId && (
            <Transformer
              ref={transformerRef}
              boundBoxFunc={(oldBox, newBox) => {
                // 변형 제한 로직
                return newBox;
              }}
            />
          )}
        </Layer>
      </Stage>
    </div>
  );
};
```

#### 2.4 템플릿 시스템 구축
```typescript
// 업종별 템플릿 시스템
interface FlyerTemplate {
  id: string;
  name: string;
  category: string;
  preview: string;
  elements: EditorElement[];
}

const templates: FlyerTemplate[] = [
  {
    id: 'cafe-modern',
    name: '모던 카페',
    category: '음식점',
    preview: '/templates/cafe-modern.jpg',
    elements: [
      {
        id: 'title',
        type: 'text',
        text: '새로운 카페 오픈!',
        x: 50, y: 30,
        fontSize: 36,
        fill: '#2D3748'
      },
      {
        id: 'subtitle', 
        type: 'text',
        text: '프리미엄 원두와 함께하는 특별한 시간',
        x: 50, y: 80,
        fontSize: 18,
        fill: '#4A5568'
      }
      // ... 더 많은 요소들
    ]
  }
  // ... 30개 업종별 템플릿
];
```

### Phase 3: AI 상담 시스템 특화 (1-2주)
**목표**: gemma3:27b를 소상공인 상담에 특화

#### 3.1 프롬프트 엔지니어링 시스템
```python
class SmallBusinessConsultantPrompts:
    """소상공인 특화 프롬프트 템플릿"""
    
    SYSTEM_PROMPT = """
    당신은 20년 경력의 소상공인 경영 컨설턴트입니다.
    한국의 소상공인 시장을 깊이 이해하고 있으며, 다음 분야에 전문성을 가지고 있습니다:
    - 상권 분석 및 입지 선정
    - 업종별 창업 가이드  
    - 마케팅 전략 수립
    - 경영 개선 방안
    - 정부 지원사업 안내
    
    실제 데이터를 바탕으로 구체적이고 실행 가능한 조언을 제공하세요.
    """
    
    LOCATION_ANALYSIS_PROMPT = """
    다음 상권 데이터를 분석하여 {business_type} 창업에 대한 조언을 제공하세요:
    
    📍 지역 정보:
    - 위치: {region}
    - 인구 통계: {population_data}
    - 기존 경쟁업체: {competition_data}
    - 유동인구: {foot_traffic}
    
    다음 관점에서 분석해주세요:
    1. 해당 지역의 {business_type} 수요 전망
    2. 경쟁 강도 및 차별화 방안
    3. 예상 매출 및 손익분기점
    4. 마케팅 전략 제안
    5. 위험 요소 및 대응 방안
    """
    
    MARKETING_STRATEGY_PROMPT = """
    {business_type} 업종의 마케팅 전략을 수립해주세요:
    
    🎯 비즈니스 정보:
    - 업종: {business_type}
    - 위치: {location}
    - 타겟 고객: {target_customer}
    - 예산: {budget}
    
    📊 시장 데이터:
    - 지역 인구통계: {demographics}
    - 경쟁사 현황: {competitors}
    - 트렌드 분석: {trends}
    
    다음을 포함한 종합 마케팅 전략을 제안하세요:
    1. 온라인 마케팅 (SNS, 블로그, 검색광고)
    2. 오프라인 마케팅 (전단지, 현수막, 이벤트)
    3. 고객 유치 및 재방문 전략
    4. 월별 마케팅 캘린더
    5. 예산 배분 및 ROI 예측
    """

class SpecializedAIConsultant:
    def __init__(self):
        self.prompts = SmallBusinessConsultantPrompts()
        self.model_endpoint = "http://localhost:11434/api/generate"  # Ollama 엔드포인트
        
    async def provide_location_consultation(self, business_type: str, region: str) -> str:
        """실데이터 기반 입지 상담"""
        # 실제 DB에서 상권 데이터 조회
        market_data = await self._fetch_market_data(region, business_type)
        
        prompt = self.prompts.LOCATION_ANALYSIS_PROMPT.format(
            business_type=business_type,
            region=region,
            population_data=market_data['population'],
            competition_data=market_data['competition'],
            foot_traffic=market_data['foot_traffic']
        )
        
        return await self._call_gemma_with_prompt(
            system_prompt=self.prompts.SYSTEM_PROMPT,
            user_prompt=prompt
        )
```

#### 3.2 실시간 데이터 연동
```python
class RealTimeDataProvider:
    """AI 상담에 필요한 실시간 데이터 제공"""
    
    async def get_consultation_context(self, region: str, business_type: str) -> Dict:
        """상담에 필요한 모든 데이터를 실시간으로 수집"""
        
        # 1. 상권 내 경쟁업체 현황
        competitors = await self.db.fetch("""
            SELECT business_name, COUNT(*) as count,
                   AVG(latitude) as avg_lat, AVG(longitude) as avg_lng
            FROM business_stores 
            WHERE sigungu_name LIKE %s 
              AND business_name LIKE %s
              AND business_status = '영업'
            GROUP BY business_name
            ORDER BY count DESC
        """, f"%{region}%", f"%{business_type}%")
        
        # 2. 인구통계 데이터
        demographics = await self.db.fetch("""
            SELECT total_population, 
                   age_20s + age_30s as main_target_age,
                   (age_20s + age_30s) * 100.0 / total_population as target_ratio
            FROM population_statistics 
            WHERE region_name LIKE %s
        """, f"%{region}%")
        
        # 3. 최신 트렌드 데이터 (pytrends 활용)
        trends = await self._fetch_google_trends(business_type)
        
        return {
            "competitors": competitors,
            "demographics": demographics,
            "trends": trends,
            "consultation_timestamp": datetime.now().isoformat()
        }
```

### Phase 4: 성능 최적화 및 안정성 확보 (1-2주)
**목표**: 실서비스 가능한 안정성 확보

#### 4.1 데이터베이스 성능 최적화
```sql
-- 상가 조회 성능을 위한 공간 인덱스
CREATE INDEX CONCURRENTLY idx_business_stores_location 
ON business_stores USING GIST (
    ST_Point(longitude, latitude)
);

-- 업종별 검색을 위한 복합 인덱스  
CREATE INDEX CONCURRENTLY idx_business_stores_region_type
ON business_stores (sigungu_name, business_name, business_status);

-- 인구통계 조회 최적화
CREATE INDEX CONCURRENTLY idx_population_region
ON population_statistics (region_name, base_date);
```

#### 4.2 API 응답 시간 최적화
```python
class OptimizedBusinessService:
    """최적화된 비즈니스 로직"""
    
    @lru_cache(maxsize=1000)
    async def get_cached_region_analysis(self, region: str, business_type: str) -> Dict:
        """지역 분석 결과 캐싱"""
        cache_key = f"region_analysis:{region}:{business_type}"
        
        # Redis 캐시 먼저 확인
        cached_result = await self.redis.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        
        # DB에서 조회 후 캐시 저장
        result = await self._analyze_region_from_db(region, business_type)
        await self.redis.setex(cache_key, 3600, json.dumps(result))  # 1시간 캐시
        
        return result
```

#### 4.3 모니터링 시스템 구축
```python
class HealthCheckSystem:
    """시스템 상태 모니터링"""
    
    async def check_system_health(self) -> Dict[str, Any]:
        """전체 시스템 상태 확인"""
        health_status = {}
        
        # 1. 데이터베이스 연결 상태
        try:
            await self.db.fetch("SELECT 1")
            health_status["database"] = "healthy"
        except Exception as e:
            health_status["database"] = f"unhealthy: {str(e)}"
        
        # 2. MCP 서버 상태  
        try:
            response = await self.mcp_connector.call_tool("health_check", {})
            health_status["mcp_server"] = "healthy"
        except Exception as e:
            health_status["mcp_server"] = f"unhealthy: {str(e)}"
        
        # 3. AI 모델 상태
        try:
            test_response = await self._test_ai_model()
            health_status["ai_model"] = "healthy"
        except Exception as e:
            health_status["ai_model"] = f"unhealthy: {str(e)}"
        
        # 4. 외부 API 상태
        health_status["external_apis"] = await self._check_external_apis()
        
        return {
            "status": "healthy" if all("healthy" in status for status in health_status.values()) else "degraded",
            "components": health_status,
            "timestamp": datetime.now().isoformat()
        }
```

---

## 🚀 구현 우선순위 및 타임라인

### 즉시 착수 (Week 1-2): Phase 0
1. **MCP 서버 통신 안정화** - 가장 중요
2. **하드코딩 경로 설정화** - 배포 필수
3. **Mock 데이터 현황 파악** - 전환 계획 수립

### 단기 (Week 3-5): Phase 1  
1. **실데이터 파이프라인 구축** - 서비스 품질 핵심
2. **Frontend Mock 제거** - 사용자 경험 개선
3. **데이터 품질 검증** - 신뢰성 확보

### 중기 (Week 6-8): Phase 2
1. **Konva.js 편집기 구현** - 핵심 기능 완성
2. **템플릿 시스템 구축** - 사용성 향상
3. **모바일 편집 지원** - 접근성 확대

### 후기 (Week 9-10): Phase 3
1. **AI 상담 특화** - 차별화 포인트
2. **실시간 데이터 연동** - AI 품질 향상

### 마무리 (Week 11-12): Phase 4
1. **성능 최적화** - 실서비스 준비
2. **모니터링 구축** - 운영 안정성

---

## 🔧 기술적 의사결정 가이드

### Fabric.js vs 대안 기술
```typescript
// 권장: Konva.js + React-Konva
const decision_matrix = {
  "구현 복잡도": { konva: 7, fabric: 9, custom: 10 },
  "모바일 지원": { konva: 9, fabric: 6, custom: 8 },
  "React 호환": { konva: 10, fabric: 7, custom: 8 },
  "개발 시간": { konva: 8, fabric: 6, custom: 4 },
  "장기 유지보수": { konva: 9, fabric: 7, custom: 6 }
  // 총점: Konva 43, Fabric 35, Custom 36
};
```

### 데이터 전환 전략
```python
# 점진적 전환 방식
class GradualDataMigration:
    async def migrate_by_priority(self):
        """우선순위별 점진적 데이터 전환"""
        
        # Phase 1: 핵심 상가 데이터 (가장 중요)
        await self.migrate_business_stores()
        
        # Phase 2: 인구통계 데이터
        await self.migrate_population_data()
        
        # Phase 3: 트렌드 데이터 (상대적으로 덜 중요)
        await self.migrate_trend_data()
        
        # 각 단계마다 검증 및 롤백 계획 포함
```

### AI 모델 활용 전략
```python
# gemma3:27b 특화 방향
ai_strategy = {
    "현재_용도": "범용 블로그 글 생성",
    "목표_특화": "소상공인 상담 전문가",
    "개선_방안": [
        "소상공인 도메인 프롬프트 엔지니어링",
        "실제 상권데이터 컨텍스트 주입", 
        "한국 소상공인 시장 특화 응답 생성"
    ],
    "성공_지표": "상담 만족도 4.0+ (5점 만점)"
}
```

---

## 📊 예상 성과 및 검증 방법

### 기술적 성과 지표
- **Mock 데이터 의존도**: 90% → 10% 이하
- **API 응답 시간**: 평균 3초 → 1초 이하
- **시스템 안정성**: 가동률 95% → 99% 이상
- **편집기 완성도**: 0% → 90% (업종별 템플릿 30개)

### 검증 방법
```bash
# 1. Mock 데이터 사용률 측정
npm run analyze:mock-usage

# 2. API 성능 테스트
npm run test:performance

# 3. 편집기 기능 테스트  
npm run test:editor-functionality

# 4. AI 상담 품질 평가
python scripts/evaluate_ai_consultation.py
```

---

## 🎯 결론 및 다음 단계

이 계획은 **기술적 실현가능성**에 중점을 두고 작성되었습니다:

1. **Phase 0 (기술부채)**: 가장 중요한 안정성 확보
2. **Phase 1 (실데이터)**: 서비스 품질의 핵심  
3. **Phase 2 (편집기)**: 사용자 경험의 완성
4. **Phase 3 (AI특화)**: 차별화 포인트 구축

**즉시 시작할 작업**:
- MCP 서버 HTTP 통신 구현
- 환경 변수 기반 설정 시스템 구축  
- Mock 데이터 사용 현황 전수 조사

구현하면서 각 Phase별로 중간 점검을 통해 우선순위를 조정하고, 특히 Fabric.js 대안 검토는 신중하게 진행하는 것이 좋겠습니다.

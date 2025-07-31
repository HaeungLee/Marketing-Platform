# 🚀 마케팅 플랫폼 종합 개발 계획서

이 문서는 `servicePlan.md`, `serviceplan2.md`, `gemini_roadmap.md`, `gemini_suggest.md`의 모든 내용을 종합하여 **실제 구현 가능한** 단계별 개발 계획을 제시합니다.

---

## 📊 현재 상황 분석 (2025.07.31 기준)

### ✅ 이미 구축된 강점
- **실제 공공데이터 연동**: 소상공인시장진흥공단 API 4개 + 인구통계 API 완전 통합
- **AI 콘텐츠 생성**: Gemini 기반 블로그/SNS/전단지 자동 생성 (92% 완성도)  
- **실시간 상권 분석**: 주변 경쟁사, 인구통계, 트렌드 분석 완료
- **사용자 인증 시스템**: 개인/사업자 구분, JWT 토큰 기반 완료
- **Fabric.js 전단지 편집**: 기본 기능 구현 완료
- **Docker 컨테이너화**: 전체 시스템 컨테이너화 완료

### ⚠️ 해결해야 할 기술적 부채 (Critical Issues)
1. **MCP 서버 통신 불안정**: `subprocess` 호출 방식으로 인한 오류 처리 어려움
2. **하드코딩된 경로/URL**: 환경별 배포 불가능한 구조
3. **Mock 데이터 잔존**: 프론트엔드 일부 영역에 Mock 데이터 사용
4. **광범위한 예외 처리**: 구체적인 오류 처리 부재로 디버깅 어려움
5. **일관성 없는 API 호출**: 중앙 apiClient 미사용 영역 존재

### 🎯 시장 기회 및 차별화 포인트
- **저작권 안전 이미지 생성**: YOLO + SAM 기반 사용자 상품 활용
- **세무 자동화**: 사업자등록증 OCR → 자동 장부 관리 (Blue Ocean)
- **소셜미디어 자동화**: 다중 플랫폼 동시 업로드 시스템
- **법률 상담 AI**: 소상공인 특화 RAG 기반 법률 자문
- **React Native 모바일 앱**: 진정한 모바일 네이티브 경험

---

## 🗺️ 단계별 구현 로드맵

### 🔧 Phase 0: 기술 부채 해결 (2주) - **최우선 필수**

**목표**: 안정적인 상용 서비스 기반 마련을 위한 핵심 리팩토링

#### Week 1: 백엔드 아키텍처 안정화
**🎯 Day 1-3: MCP 서버 통신 개선**
```python
# 현재 문제: insights_analysis_service.py
subprocess.run([
    "node", f"{server_path}/build/index.js",  # 하드코딩된 경로
    "mcp_server", tool_name, json.dumps(args)
], shell=True)  # 불안정한 subprocess 호출

# 해결책: HTTP API 통신으로 전환
class MCPServerConnector:
    def __init__(self):
        self.base_url = os.getenv('MCP_SERVER_URL', 'http://mcp-server:3000')
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def call_tool(self, tool_name: str, args: dict):
        try:
            response = await self.client.post(
                f"{self.base_url}/api/tools/{tool_name}",
                json=args
            )
            return response.json()
        except httpx.ConnectError:
            raise MCPServerConnectionError("MCP 서버 연결 실패")
        except httpx.TimeoutError:
            raise MCPServerTimeoutError("MCP 서버 응답 시간 초과")
```

**🎯 Day 4-5: 환경 변수 분리 및 설정 통일**
```python
# backend/.env (생성)
DATABASE_URL=postgresql://user:pass@db:5432/marketing_platform
REDIS_URL=redis://redis:6379/0
MCP_SERVER_URL=http://mcp-server:3000
GEMINI_API_KEY=your_gemini_api_key
SBIZ_API_KEYS=key1,key2,key3,key4

# config/settings.py (개선)
class Settings:
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")
    mcp_server_url: str = Field(..., env="MCP_SERVER_URL")
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
```

#### Week 2: 프론트엔드 아키텍처 통일
**🎯 Day 1-3: React Query 도입**
```typescript
// 설치: npm install @tanstack/react-query
// providers/QueryProvider.tsx (신규 생성)
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5분
      cacheTime: 10 * 60 * 1000, // 10분
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
});

// hooks/usePopulationData.ts (신규 생성)
export function usePopulationData(region: string) {
  return useQuery({
    queryKey: ['population', region],
    queryFn: () => apiClient.get(`/api/population/${region}`),
    enabled: !!region,
  });
}
```

**🎯 Day 4-5: API 서비스 통일 및 코드 정리**
```typescript
// services/populationService.ts (개선)
import { apiClient } from './api';

// 기존: 별도 axios 인스턴스 사용
// const axiosInstance = axios.create({...});

// 개선: 중앙 apiClient 사용
export const populationService = {
  getPopulationData: (region: string) => 
    apiClient.get(`/api/population/${region}`),
  
  getBusinessTrends: (params: TrendParams) =>
    apiClient.post('/api/population/trends', params),
};

// 불필요한 .new 파일들 삭제
// - apiService.ts.new
// - PopulationDashboardPage.tsx.new
```

---

### 🛡️ Phase 1: 저작권 보호 시스템 구축 (3주)

**목표**: AI 이미지 생성의 법적 리스크를 완전히 해결하여 안전한 상용 서비스 구축

#### Week 1: YOLO + SAM 기반 상품 세그멘테이션
**🎯 핵심 구현: 사용자 상품 사진 활용 시스템**
```python
# services/image_segmentation_service.py (신규)
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamPredictor
import cv2
import numpy as np

class ProductSegmentationService:
    def __init__(self):
        # YOLO 모델 로드 (상품 검출용)
        self.yolo_model = YOLO('yolov8n.pt')
        
        # SAM 모델 로드 (정밀 세그멘테이션용)
        sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth")
        self.sam_predictor = SamPredictor(sam)
    
    async def extract_product_from_image(self, image_path: str):
        """사용자 상품 사진에서 상품만 추출"""
        # 1. YOLO로 상품 객체 검출
        results = self.yolo_model(image_path)
        
        # 2. SAM으로 정밀 세그멘테이션
        image = cv2.imread(image_path)
        self.sam_predictor.set_image(image)
        
        masks = []
        for result in results:
            for box in result.boxes:
                # YOLO 박스를 SAM 입력으로 사용
                input_box = box.xyxy.cpu().numpy()[0]
                mask = self.sam_predictor.predict(
                    box=input_box,
                    multimask_output=False,
                )[0]
                masks.append(mask)
        
        # 3. 상품 누끼 이미지 생성
        product_cutout = self.apply_mask_to_image(image, masks[0])
        
        return {
            "product_image": product_cutout,
            "original_size": image.shape[:2],
            "confidence": float(results[0].boxes[0].conf),
            "category": results[0].names[int(results[0].boxes[0].cls)]
        }

# API 엔드포인트 추가
@router.post("/api/images/segment-product")
async def segment_product(file: UploadFile = File(...)):
    segmentation_service = ProductSegmentationService()
    result = await segmentation_service.extract_product_from_image(file)
    return result
```

#### Week 2: AI 안전 배경 생성 및 합성
**🎯 저작권 안전한 배경 생성 시스템**
```python
class CopyrightSafeImageComposer:
    def __init__(self):
        self.gemini_client = genai.GenerativeModel('gemini-pro-vision')
        
    async def generate_safe_background(self, business_info: dict):
        """저작권 안전한 배경 생성"""
        safe_prompts = [
            f"abstract geometric pattern, {business_info['brand_colors']}, minimalist",
            f"clean gradient background, {business_info['business_type']} theme",
            f"simple texture pattern, professional, {business_info['mood']}"
        ]
        
        # 저작권 위험 키워드 필터링
        filtered_prompt = self.filter_copyright_risks(safe_prompts[0])
        
        # 이미지 생성
        background = await self.generate_image(filtered_prompt)
        
        # 저작권 데이터베이스 유사도 검사
        similarity_check = await self.check_copyright_similarity(background)
        
        if similarity_check['risk_score'] > 0.7:
            # 위험도가 높으면 다른 프롬프트로 재생성
            return await self.generate_safe_background(business_info)
            
        return background
    
    async def compose_promotional_image(self, product_cutout, safe_background):
        """상품과 배경 자연스럽게 합성"""
        # 1. 배경 크기 조정
        resized_background = cv2.resize(safe_background, (800, 600))
        
        # 2. 상품 위치 최적화 (AI 기반)
        optimal_position = await self.calculate_optimal_position(
            product_cutout, resized_background
        )
        
        # 3. 자연스러운 합성 (그림자, 조명 효과)
        composed = await self.natural_composition(
            product_cutout, resized_background, optimal_position
        )
        
        return composed
```

#### Week 3: 워터마킹 및 법적 보호 장치
**🎯 완전한 저작권 보호 시스템**
```python
class CopyrightProtectionSystem:
    def __init__(self):
        self.watermark_engine = WatermarkEngine()
        self.legal_compliance = LegalComplianceChecker()
    
    async def apply_copyright_protection(self, image, generation_method: str):
        """이미지에 저작권 보호 장치 적용"""
        
        # 1. 가시적 워터마크 추가
        visible_watermark = {
            "text": "AI Generated" if generation_method == "ai" else "User Content Enhanced",
            "position": "bottom_right",
            "opacity": 0.7,
            "font_size": 12
        }
        
        # 2. 비가시적 디지털 워터마크 삽입
        digital_signature = await self.create_digital_signature(image)
        
        # 3. 메타데이터 삽입
        metadata = {
            "generation_method": generation_method,
            "creation_timestamp": datetime.now().isoformat(),
            "platform": "Marketing-Platform",
            "copyright_notice": "본 이미지의 상업적 사용 시 저작권을 확인하세요."
        }
        
        protected_image = await self.watermark_engine.apply_protection(
            image, visible_watermark, digital_signature, metadata
        )
        
        return {
            "protected_image": protected_image,
            "copyright_safe": True,
            "legal_disclaimer": self.generate_legal_disclaimer(generation_method)
        }
```

---

### 💰 Phase 2: 세무 자동화 MVP (4주)

**목표**: 게임 체인저가 될 세무 자동화 기능의 MVP 구현

#### Week 1-2: 사업자등록증 OCR 시스템
**🎯 모바일/웹 OCR 스캔 기능**
```python
# services/business_license_ocr.py (신규)
import pytesseract
from PIL import Image
import cv2
import re

class BusinessLicenseOCR:
    def __init__(self):
        # Tesseract 한글 설정
        self.tesseract_config = '--oem 3 --psm 6 -l kor+eng'
        
    async def extract_business_info(self, image_file):
        """사업자등록증에서 정보 자동 추출"""
        
        # 1. 이미지 전처리
        processed_image = await self.preprocess_image(image_file)
        
        # 2. OCR 텍스트 추출
        text = pytesseract.image_to_string(
            processed_image, 
            config=self.tesseract_config
        )
        
        # 3. 정규식으로 핵심 정보 추출
        business_info = {
            "registration_number": self.extract_registration_number(text),
            "business_name": self.extract_business_name(text),
            "owner_name": self.extract_owner_name(text),
            "address": self.extract_address(text),
            "business_type": self.extract_business_type(text),
        }
        
        # 4. 사업자등록번호 실시간 검증
        validation = await self.validate_business_number(
            business_info["registration_number"]
        )
        
        return {
            **business_info,
            "validation": validation,
            "confidence_score": self.calculate_confidence(business_info)
        }
    
    def extract_registration_number(self, text: str) -> str:
        """사업자등록번호 추출 (XXX-XX-XXXXX 형식)"""
        pattern = r'\b\d{3}-\d{2}-\d{5}\b'
        matches = re.findall(pattern, text)
        return matches[0] if matches else None

# React Native 컴포넌트
const BusinessLicenseScanner = () => {
  const [image, setImage] = useState(null);
  const [extractedInfo, setExtractedInfo] = useState(null);
  
  const scanBusinessLicense = async () => {
    // 1. 카메라로 촬영
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });
    
    if (!result.cancelled) {
      setImage(result);
      
      // 2. 서버에 OCR 요청
      const formData = new FormData();
      formData.append('image', {
        uri: result.uri,
        type: 'image/jpeg',
        name: 'business_license.jpg',
      });
      
      const response = await apiClient.post('/api/ocr/business-license', formData);
      setExtractedInfo(response.data);
    }
  };
};
```

#### Week 3-4: 기본 장부 및 세무 계산
**🎯 간단한 장부 관리 시스템**
```python
# models/tax_models.py (신규)
class BusinessProfile(Base):
    __tablename__ = "business_profiles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # OCR로 추출된 정보
    registration_number = Column(String(12), unique=True, index=True)
    business_name = Column(String(100))
    owner_name = Column(String(50))
    business_type = Column(String(100))
    address = Column(Text)
    
    # 세무 설정
    tax_type = Column(String(20), default="individual")  # 개인/법인
    vat_exemption = Column(Boolean, default=False)
    
class TransactionRecord(Base):
    __tablename__ = "transaction_records"
    
    id = Column(Integer, primary_key=True)
    business_profile_id = Column(Integer, ForeignKey("business_profiles.id"))
    
    transaction_date = Column(Date)
    transaction_type = Column(String(10))  # 'income' or 'expense'
    amount = Column(Decimal(15, 2))
    description = Column(String(200))
    category = Column(String(50))
    
    # 부가세 관련
    vat_amount = Column(Decimal(15, 2), default=0)
    vat_included = Column(Boolean, default=True)

# services/tax_calculation_service.py (신규)
class TaxCalculationService:
    async def calculate_monthly_vat(self, business_id: str, year: int, month: int):
        """월별 부가세 계산"""
        
        # 해당 월의 거래 내역 조회
        transactions = await self.get_monthly_transactions(business_id, year, month)
        
        total_sales = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_purchases = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        
        # 부가세 계산 (10%)
        sales_vat = total_sales * 0.1 / 1.1  # 매출세액
        purchase_vat = total_purchases * 0.1 / 1.1  # 매입세액
        
        payable_vat = sales_vat - purchase_vat  # 납부할 부가세
        
        return {
            "period": f"{year}-{month:02d}",
            "total_sales": float(total_sales),
            "total_purchases": float(total_purchases),
            "sales_vat": float(sales_vat),
            "purchase_vat": float(purchase_vat),
            "payable_vat": float(payable_vat),
            "due_date": self.calculate_vat_due_date(year, month),
            "recommendations": await self.generate_tax_recommendations(payable_vat)
        }
```

---

### 📱 Phase 3: 소셜미디어 자동화 MVP (3주)

**목표**: 현실적이고 구현 가능한 소셜미디어 자동화 시스템

#### Week 1: 네이버 블로그 + 티스토리 API 연동
**🎯 정책적으로 안전한 API 우선 구현**
```python
# services/social_media_automation.py (신규)
class NaverBlogService:
    def __init__(self):
        self.client_id = os.getenv('NAVER_CLIENT_ID')
        self.client_secret = os.getenv('NAVER_CLIENT_SECRET')
        self.access_token = None
    
    async def authenticate_user(self, code: str):
        """네이버 OAuth 인증"""
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://nid.naver.com/oauth2.0/token',
                data=token_data
            )
            token_info = response.json()
            self.access_token = token_info['access_token']
            return token_info
    
    async def post_to_blog(self, content: BlogContent):
        """네이버 블로그 자동 포스팅"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/xml; charset=utf-8'
        }
        
        xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
        <post>
            <title>{content.title}</title>
            <content>{content.content}</content>
            <category>{content.category}</category>
            <tags>{','.join(content.tags)}</tags>
        </post>"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://openapi.naver.com/blog/writePost.xml',
                content=xml_data,
                headers=headers
            )
            
            return {
                "success": response.status_code == 200,
                "post_url": self.extract_post_url(response.text),
                "platform": "naver_blog"
            }

class TistoryService:
    async def post_to_tistory(self, content: BlogContent):
        """티스토리 자동 포스팅"""
        data = {
            'access_token': os.getenv('TISTORY_ACCESS_TOKEN'),
            'blogName': os.getenv('TISTORY_BLOG_NAME'),
            'title': content.title,
            'content': content.content,
            'visibility': '3',  # 공개
            'category': content.category,
            'tag': ','.join(content.tags)
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://www.tistory.com/apis/post/write',
                data=data
            )
            
            return response.json()
```

#### Week 2: Instagram/Facebook 반자동화 시스템
**🎯 정책 제약을 우회하는 스마트한 접근**
```typescript
// components/SocialMediaHelper.tsx (신규)
const SocialMediaHelper = ({ content, generatedImage }) => {
  const [optimizedContent, setOptimizedContent] = useState({});
  
  useEffect(() => {
    // 플랫폼별 콘텐츠 최적화
    const optimizeForPlatforms = async () => {
      const platforms = ['instagram', 'facebook', 'twitter'];
      const optimized = {};
      
      for (const platform of platforms) {
        optimized[platform] = await optimizeContentForPlatform(content, platform);
      }
      
      setOptimizedContent(optimized);
    };
    
    optimizeForPlatforms();
  }, [content]);
  
  const copyToClipboard = (platform: string) => {
    const text = optimizedContent[platform]?.caption || '';
    navigator.clipboard.writeText(text);
    toast.success(`${platform} 캡션이 클립보드에 복사되었습니다!`);
  };
  
  const downloadOptimizedImage = (platform: string) => {
    // 플랫폼별 최적 크기로 이미지 다운로드
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    const sizes = {
      instagram: { width: 1080, height: 1080 }, // 정사각형
      facebook: { width: 1200, height: 630 },   // 1.91:1
      twitter: { width: 1024, height: 512 }     // 2:1
    };
    
    const { width, height } = sizes[platform];
    canvas.width = width;
    canvas.height = height;
    
    // 이미지 리사이징 및 다운로드
    resizeAndDownload(generatedImage, canvas, `${platform}_optimized.jpg`);
  };
  
  return (
    <VStack spacing={4}>
      {Object.entries(optimizedContent).map(([platform, content]) => (
        <Box key={platform} p={4} border="1px" borderColor="gray.200" borderRadius="md">
          <HStack justify="space-between" mb={2}>
            <Text fontWeight="bold" textTransform="capitalize">{platform}</Text>
            <HStack>
              <Button size="sm" onClick={() => copyToClipboard(platform)}>
                📋 캡션 복사
              </Button>
              <Button size="sm" onClick={() => downloadOptimizedImage(platform)}>
                📥 이미지 다운로드
              </Button>
            </HStack>
          </HStack>
          
          <Text fontSize="sm" color="gray.600" mb={2}>
            최적화된 캡션 ({content.caption?.length || 0}자)
          </Text>
          <Textarea 
            value={content.caption || ''} 
            readOnly 
            size="sm"
            rows={4}
          />
          
          {content.hashtags && (
            <Text fontSize="xs" color="blue.500" mt={2}>
              추천 해시태그: {content.hashtags.join(' ')}
            </Text>
          )}
        </Box>
      ))}
    </VStack>
  );
};
```

#### Week 3: 콘텐츠 스케줄링 시스템
**🎯 Celery + Redis 기반 예약 시스템**
```python
# tasks/social_media_tasks.py (신규)
from celery import Celery
import redis

app = Celery('social_media_scheduler')
app.config_from_object('config.celery_config')

@app.task
async def schedule_blog_post(content_data: dict, platform: str, scheduled_time: str):
    """예약된 시간에 블로그 포스팅 실행"""
    
    if platform == 'naver_blog':
        service = NaverBlogService()
        result = await service.post_to_blog(BlogContent(**content_data))
    elif platform == 'tistory':
        service = TistoryService()
        result = await service.post_to_tistory(BlogContent(**content_data))
    
    # 결과를 데이터베이스에 저장
    await save_posting_result(content_data['user_id'], platform, result)
    
    return result

# services/content_scheduler.py (신규)
class ContentScheduler:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)
    
    async def schedule_multi_platform_post(self, content: dict, platforms: list, user_preferences: dict):
        """다중 플랫폼 예약 포스팅"""
        
        optimal_times = {
            "naver_blog": {
                "weekdays": ["09:00", "12:00", "21:00"],
                "weekends": ["11:00", "16:00", "20:00"]
            },
            "tistory": {
                "weekdays": ["08:00", "12:00", "18:00"],
                "weekends": ["10:00", "14:00", "19:00"]
            }
        }
        
        scheduled_tasks = []
        
        for platform in platforms:
            if platform in ['instagram', 'facebook', 'twitter']:
                # 반자동화 플랫폼은 스케줄링하지 않음
                continue
                
            # 다음 최적 시간 계산
            next_optimal_time = self.calculate_next_optimal_time(platform, optimal_times)
            
            # Celery 태스크 스케줄링
            task = schedule_blog_post.apply_async(
                args=[content, platform],
                eta=next_optimal_time
            )
            
            scheduled_tasks.append({
                "platform": platform,
                "scheduled_time": next_optimal_time.isoformat(),
                "task_id": task.id,
                "status": "scheduled"
            })
        
        return scheduled_tasks
```

---

### 🚀 Phase 4: React Native 모바일 앱 (4주)

**목표**: 진정한 모바일 네이티브 경험 제공

#### Week 1-2: 모바일 앱 기본 구조
**🎯 Expo + React Native 기반 앱 개발**
```bash
# 초기 설정
npx create-expo-app@latest MarketingPlatformApp --template tabs
cd MarketingPlatformApp
npx expo install @react-navigation/native @react-navigation/bottom-tabs
npx expo install expo-camera expo-image-picker expo-notifications
```

```typescript
// App.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const Tab = createBottomTabNavigator();
const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <NavigationContainer>
        <Tab.Navigator>
          <Tab.Screen 
            name="홈" 
            component={HomeScreen}
            options={{
              tabBarIcon: ({ color, size }) => (
                <Ionicons name="home" size={size} color={color} />
              ),
            }}
          />
          <Tab.Screen 
            name="분석" 
            component={AnalyticsScreen}
            options={{
              tabBarIcon: ({ color, size }) => (
                <Ionicons name="analytics" size={size} color={color} />
              ),
            }}
          />
          <Tab.Screen 
            name="콘텐츠" 
            component={ContentScreen}
            options={{
              tabBarIcon: ({ color, size }) => (
                <Ionicons name="create" size={size} color={color} />
              ),
            }}
          />
          <Tab.Screen 
            name="세무" 
            component={TaxScreen}
            options={{
              tabBarIcon: ({ color, size }) => (
                <Ionicons name="calculator" size={size} color={color} />
              ),
            }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </QueryClientProvider>
  );
}
```

#### Week 3-4: 모바일 특화 기능
**🎯 사업자등록증 스캔 + 푸시 알림**
```typescript
// screens/TaxScreen.tsx
import * as ImagePicker from 'expo-image-picker';
import { Camera } from 'expo-camera';

const BusinessLicenseScanner = () => {
  const [hasPermission, setHasPermission] = useState(null);
  
  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);
  
  const scanBusinessLicense = async () => {
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });
    
    if (!result.cancelled) {
      // OCR 처리를 위해 서버에 전송
      const formData = new FormData();
      formData.append('image', {
        uri: result.uri,
        type: 'image/jpeg',
        name: 'business_license.jpg',
      } as any);
      
      try {
        const response = await apiClient.post('/api/ocr/business-license', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        
        // 추출된 정보를 표시
        setExtractedInfo(response.data);
      } catch (error) {
        Alert.alert('오류', 'OCR 처리 중 오류가 발생했습니다.');
      }
    }
  };
};

// services/notificationService.ts
import * as Notifications from 'expo-notifications';

class NotificationService {
  async setupTaxReminders(businessInfo: any) {
    // 권한 요청
    const { status } = await Notifications.requestPermissionsAsync();
    if (status !== 'granted') return;
    
    // 부가세 신고 마감일 계산
    const taxDueDates = this.calculateTaxDueDates(businessInfo);
    
    for (const dueDate of taxDueDates) {
      await Notifications.scheduleNotificationAsync({
        content: {
          title: "세무 신고 마감일 임박! 📋",
          body: `${dueDate.type} 신고 마감일이 3일 남았습니다.`,
          data: { type: 'tax_reminder', taxType: dueDate.type },
        },
        trigger: {
          date: new Date(dueDate.deadline.getTime() - 3 * 24 * 60 * 60 * 1000),
        },
      });
    }
  }
  
  private calculateTaxDueDates(businessInfo: any) {
    // 개인사업자 기준 세무 일정
    const currentYear = new Date().getFullYear();
    
    return [
      {
        type: "부가세 예정신고",
        deadline: new Date(currentYear, 6, 25), // 7월 25일
      },
      {
        type: "부가세 확정신고", 
        deadline: new Date(currentYear + 1, 0, 25), // 1월 25일
      },
      {
        type: "종합소득세",
        deadline: new Date(currentYear + 1, 4, 31), // 5월 31일
      }
    ];
  }
}
```

---

### 💡 Phase 5: 상용화 및 결제 시스템 (2주)

**목표**: 실제 수익 창출을 위한 결제 및 구독 모델 구현

#### Week 1: PG사 연동 및 결제 시스템
**🎯 아임포트 기반 결제 시스템**
```python
# services/payment_service.py (신규)
import requests
from decimal import Decimal

class PaymentService:
    def __init__(self):
        self.imp_key = os.getenv('IAMPORT_API_KEY')
        self.imp_secret = os.getenv('IAMPORT_API_SECRET')
        self.access_token = None
    
    async def get_access_token(self):
        """아임포트 액세스 토큰 획득"""
        data = {
            'imp_key': self.imp_key,
            'imp_secret': self.imp_secret
        }
        
        response = requests.post('https://api.iamport.kr/users/getToken', data=data)
        result = response.json()
        
        if result['code'] == 0:
            self.access_token = result['response']['access_token']
            return self.access_token
        else:
            raise PaymentError(f"토큰 획득 실패: {result['message']}")
    
    async def create_subscription(self, user_id: int, plan: str):
        """구독 결제 생성"""
        plans = {
            'basic': {'price': 29000, 'name': 'Basic 플랜'},
            'professional': {'price': 69000, 'name': 'Professional 플랜'},
            'enterprise': {'price': 149000, 'name': 'Enterprise 플랜'}
        }
        
        plan_info = plans.get(plan)
        if not plan_info:
            raise ValueError("유효하지 않은 플랜입니다.")
        
        # 결제 정보 생성
        payment_data = {
            'merchant_uid': f'subscription_{user_id}_{int(time.time())}',
            'amount': plan_info['price'],
            'name': plan_info['name'],
            'buyer_name': user.name,
            'buyer_email': user.email,
        }
        
        return payment_data

# models/subscription_models.py (신규)
class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    plan = Column(String(20))  # basic, professional, enterprise
    status = Column(String(20), default="active")  # active, cancelled, expired
    
    started_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # 결제 정보
    payment_method = Column(String(50))
    merchant_uid = Column(String(100), unique=True)
    amount = Column(Decimal(10, 2))
    
class FeatureAccess(Base):
    __tablename__ = "feature_access"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 기능별 사용량 제한
    content_generation_limit = Column(Integer, default=10)  # 월 콘텐츠 생성 횟수
    ai_consultation_limit = Column(Integer, default=5)      # 월 AI 상담 횟수
    social_media_posts_limit = Column(Integer, default=20)  # 월 소셜미디어 포스팅
    
    # 사용량 추적
    content_generation_used = Column(Integer, default=0)
    ai_consultation_used = Column(Integer, default=0)
    social_media_posts_used = Column(Integer, default=0)
    
    reset_date = Column(DateTime)  # 사용량 리셋 날짜 (매월)
```

#### Week 2: Freemium 모델 적용
**🎯 기능별 접근 제한 시스템**
```python
# middleware/subscription_middleware.py (신규)
from functools import wraps

def require_subscription(required_plan: str = 'basic'):
    """구독 권한이 필요한 API에 적용하는 데코레이터"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 현재 사용자의 구독 정보 확인
            user = kwargs.get('current_user')
            subscription = await get_user_subscription(user.id)
            
            if not subscription or subscription.status != 'active':
                raise HTTPException(
                    status_code=403,
                    detail="이 기능을 사용하려면 구독이 필요합니다."
                )
            
            # 플랜 레벨 확인
            plan_levels = {'basic': 1, 'professional': 2, 'enterprise': 3}
            user_level = plan_levels.get(subscription.plan, 0)
            required_level = plan_levels.get(required_plan, 1)
            
            if user_level < required_level:
                raise HTTPException(
                    status_code=403,
                    detail=f"{required_plan} 플랜 이상이 필요합니다."
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# API 적용 예시
@router.post("/api/content/generate")
@require_subscription('basic')
async def generate_content(request: ContentRequest, current_user: User = Depends(get_current_user)):
    # 사용량 제한 확인
    feature_access = await get_feature_access(current_user.id)
    
    if feature_access.content_generation_used >= feature_access.content_generation_limit:
        raise HTTPException(
            status_code=429,
            detail="월 콘텐츠 생성 한도를 초과했습니다. 플랜을 업그레이드하세요."
        )
    
    # 콘텐츠 생성 로직
    result = await content_service.generate_content(request)
    
    # 사용량 업데이트
    await increment_feature_usage(current_user.id, 'content_generation')
    
    return result

@router.post("/api/tax/auto-calculate")
@require_subscription('professional')
async def auto_calculate_tax(current_user: User = Depends(get_current_user)):
    # Professional 플랜 이상만 세무 자동화 기능 사용 가능
    pass
```

---

## 🎯 성공 지표 및 마일스톤

### Phase별 완료 기준
- **Phase 0**: 모든 하드코딩 제거, MCP 서버 HTTP 통신, React Query 적용
- **Phase 1**: YOLO 상품 추출, 안전 배경 합성, 워터마킹 시스템 완료
- **Phase 2**: OCR 95% 이상 정확도, 부가세 자동 계산, 장부 기록 기능
- **Phase 3**: 네이버/티스토리 자동 포스팅, Instagram/Facebook 반자동화
- **Phase 4**: iOS/Android 앱 스토어 출시, 푸시 알림 시스템
- **Phase 5**: 첫 유료 구독자 획득, 결제 시스템 안정화

### 기술적 성능 목표
- **API 응답 시간**: 평균 500ms 이하
- **이미지 생성**: 30초 이내 완료
- **OCR 정확도**: 95% 이상
- **시스템 가동률**: 99.5% 이상
- **동시 접속자**: 100명 지원 (Phase 5 완료 시)

### 비즈니스 목표
- **6개월 후**: 유료 사용자 50명, 월 매출 200만원
- **1년 후**: 유료 사용자 300명, 월 매출 1,500만원
- **18개월 후**: 유료 사용자 1,000명, 월 매출 5,000만원

---

## 🚨 리스크 관리 계획

### 기술적 리스크
1. **YOLO/SAM 모델 성능**: 상품 인식률 95% 목표, 실패 시 수동 보정 UI 제공
2. **OCR 정확도**: 다양한 사업자등록증 형태 대응, 수동 수정 기능 필수
3. **소셜미디어 API 정책 변경**: 반자동화 방식으로 정책 리스크 최소화

### 법적 리스크  
1. **저작권 문제**: 사용자 상품 사진 우선 사용, AI 생성 시 워터마킹 의무화
2. **개인정보보호**: 사업자등록증 정보 암호화 저장, GDPR 준수
3. **세무 정보 정확성**: "참고용 정보"라는 면책 조항, 세무사 상담 권장

### 사업적 리스크
1. **초기 사용자 확보**: 무료 체험 3개월 제공, 입소문 마케팅 집중  
2. **경쟁사 대응**: 특허출원 가능한 기술 요소 발굴, 선점 효과 확보
3. **기술 의존성**: 주요 API (Gemini, 네이버 등) 대체재 준비

---

## 💡 결론 및 다음 단계

이 계획서는 **현실적이고 구현 가능한** 개발 로드맵을 제시합니다. 

### 핵심 성공 요소
1. **기술 부채 해결 우선**: 안정적인 기반 없이는 새로운 기능도 무의미
2. **법적 안전성 확보**: 저작권 보호 시스템으로 서비스의 신뢰성 구축
3. **차별화된 가치 제공**: 세무 자동화라는 Blue Ocean 시장 선점
4. **점진적 확장**: MVP → 개선 → 확장의 안전한 성장 전략

### 즉시 시작 가능한 작업
1. **환경 변수 분리**: `.env` 파일 생성 및 하드코딩 제거
2. **MCP 서버 HTTP 통신**: `subprocess` → `httpx` 마이그레이션  
3. **React Query 도입**: `PopulationDashboardPage` 리팩토링부터 시작
4. **YOLO 환경 구축**: YOLOv8 모델 다운로드 및 테스트

### 논의 필요 사항
1. **개발 우선순위**: Phase별 순서 조정 필요한지?
2. **기술 선택**: 제안된 기술 스택에 대한 의견?
3. **리소스 배분**: 각 Phase별 예상 개발 시간 적절한지?
4. **비즈니스 모델**: Freemium 가격 정책 적절한지?

**이제 구체적인 구현 작업에 들어갈 준비가 되었습니다!** 🚀

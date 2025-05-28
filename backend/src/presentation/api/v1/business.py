"""
비즈니스 관련 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter()


class BusinessCreateRequest(BaseModel):
    name: str
    category: str
    description: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    target_radius_km: float = 1.0


class BusinessResponse(BaseModel):
    id: str
    name: str
    category: str
    description: str
    latitude: float
    longitude: float
    address: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    target_radius_km: float
    created_at: str


class CategoryResponse(BaseModel):
    categories: List[Dict[str, Any]]


@router.get("/categories", response_model=CategoryResponse)
async def get_business_categories():
    """업종 카테고리 목록 조회"""
    # 하드코딩된 샘플 데이터
    categories = [
        {
            "id": "food",
            "name": "음식점",
            "subcategories": [
                {"id": "cafe", "name": "카페"},
                {"id": "restaurant", "name": "일반음식점"},
                {"id": "fastfood", "name": "패스트푸드"},
                {"id": "bakery", "name": "베이커리"},
                {"id": "chicken", "name": "치킨전문점"}
            ]
        },
        {
            "id": "retail",
            "name": "소매업",
            "subcategories": [
                {"id": "clothing", "name": "의류"},
                {"id": "cosmetics", "name": "화장품"},
                {"id": "electronics", "name": "전자제품"},
                {"id": "books", "name": "서점"},
                {"id": "grocery", "name": "식료품"}
            ]
        },
        {
            "id": "service",
            "name": "서비스업",
            "subcategories": [
                {"id": "beauty", "name": "미용실"},
                {"id": "laundry", "name": "세탁소"},
                {"id": "repair", "name": "수리점"},
                {"id": "education", "name": "학원"},
                {"id": "fitness", "name": "헬스장"}
            ]
        }
    ]
    
    return {"categories": categories}


@router.post("/", response_model=BusinessResponse)
async def create_business(request: BusinessCreateRequest):
    """비즈니스 등록"""
    # TODO: 실제 구현 필요
    return {
        "id": "business-123",
        "name": request.name,
        "category": request.category,
        "description": request.description,
        "latitude": request.latitude,
        "longitude": request.longitude,
        "address": request.address,
        "phone": request.phone,
        "website": request.website,
        "target_radius_km": request.target_radius_km,
        "created_at": "2024-01-01T00:00:00Z"
    }


@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(business_id: str):
    """비즈니스 정보 조회"""
    # TODO: 실제 구현 필요
    return {
        "id": business_id,
        "name": "샘플 카페",
        "category": "음식점>카페",
        "description": "맛있는 커피를 파는 카페입니다.",
        "latitude": 37.5665,
        "longitude": 126.9780,
        "address": "서울시 중구 태평로 1가",
        "phone": "02-1234-5678",
        "website": "https://example.com",
        "target_radius_km": 1.0,
        "created_at": "2024-01-01T00:00:00Z"
    }


@router.get("/")
async def get_user_businesses():
    """사용자의 비즈니스 목록 조회"""
    # TODO: 실제 구현 필요 (JWT 토큰에서 사용자 ID 추출)
    return {
        "businesses": [
            {
                "id": "business-123",
                "name": "샘플 카페",
                "category": "음식점>카페",
                "address": "서울시 중구 태평로 1가",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
    }


@router.get("/{business_id}/area-info")
async def get_area_info(business_id: str, radius_km: float = 1.0):
    """상권 정보 조회 (공공데이터 기반)"""
    # 구현이 필요한 기능임을 알림
    raise HTTPException(
        status_code=501,
        detail="공공데이터 연동이 필요합니다. 이 기능은 구현 예정입니다."
    )

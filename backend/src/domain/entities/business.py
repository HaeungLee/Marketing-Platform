"""
Business 엔티티 구현
"""
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from domain.value_objects.coordinates import Coordinates


@dataclass
class Business:
    """비즈니스 엔티티"""
    
    id: str
    user_id: str  # 소유자 ID
    name: str  # 사업체명
    category: str  # 업종 (예: "음식점>카페")
    description: str  # 사업체 설명
    coordinates: Coordinates  # 위치
    address: Optional[str] = None  # 주소
    phone: Optional[str] = None  # 전화번호
    website: Optional[str] = None  # 웹사이트
    operating_hours: Optional[Dict[str, str]] = None  # 운영시간
    target_radius_km: float = 1.0  # 타겟 반경 (km)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """생성 후 유효성 검증"""
        self._validate_name()
        self._validate_category()
        self._validate_target_radius()
    
    def _validate_name(self):
        """사업체명 유효성 검증"""
        if not self.name or not self.name.strip():
            raise ValueError("Business name cannot be empty")
        
        if len(self.name) > 100:
            raise ValueError("Business name must be less than 100 characters")
    
    def _validate_category(self):
        """업종 카테고리 유효성 검증"""
        if not self.category or not self.category.strip():
            raise ValueError("Business category cannot be empty")
    
    def _validate_target_radius(self):
        """타겟 반경 유효성 검증"""
        if self.target_radius_km <= 0:
            raise ValueError("Target radius must be positive")
        
        if self.target_radius_km > 10:  # 최대 10km
            raise ValueError("Target radius cannot exceed 10km")
    
    def update_info(self, 
                   name: Optional[str] = None,
                   description: Optional[str] = None,
                   address: Optional[str] = None,
                   phone: Optional[str] = None,
                   website: Optional[str] = None):
        """비즈니스 정보 업데이트"""
        if name is not None:
            old_name = self.name
            self.name = name
            try:
                self._validate_name()
            except ValueError:
                self.name = old_name
                raise
        
        if description is not None:
            self.description = description
        
        if address is not None:
            self.address = address
        
        if phone is not None:
            self.phone = phone
        
        if website is not None:
            self.website = website
        
        self.updated_at = datetime.utcnow()
    
    def update_location(self, coordinates: Coordinates, address: Optional[str] = None):
        """위치 정보 업데이트"""
        self.coordinates = coordinates
        if address is not None:
            self.address = address
        self.updated_at = datetime.utcnow()
    
    def update_target_radius(self, radius_km: float):
        """타겟 반경 업데이트"""
        old_radius = self.target_radius_km
        self.target_radius_km = radius_km
        
        try:
            self._validate_target_radius()
            self.updated_at = datetime.utcnow()
        except ValueError:
            self.target_radius_km = old_radius
            raise

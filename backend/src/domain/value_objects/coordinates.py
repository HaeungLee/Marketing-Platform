"""
Coordinates 값 객체 구현
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    """지리적 좌표 값 객체"""
    
    latitude: float  # 위도
    longitude: float  # 경도
    
    def __post_init__(self):
        """생성 후 유효성 검증"""
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
    
    def distance_to(self, other: 'Coordinates') -> float:
        """다른 좌표와의 거리 계산 (km)"""
        import math
        
        # Haversine 공식 사용
        R = 6371  # 지구 반지름 (km)
        
        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(other.latitude)
        delta_lat = math.radians(other.latitude - self.latitude)
        delta_lng = math.radians(other.longitude - self.longitude)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def __str__(self) -> str:
        return f"({self.latitude}, {self.longitude})"

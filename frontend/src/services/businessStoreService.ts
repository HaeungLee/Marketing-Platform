import api from './api';

export interface BusinessStore {
  id: number;
  store_name: string;
  business_name: string;
  business_code: string;
  latitude: number;
  longitude: number;
  road_address?: string;
  jibun_address?: string;
  sido_name: string;
  sigungu_name: string;
  dong_name: string;
  building_name?: string;
  floor_info?: string;
  business_status: string;
  open_date?: string;
  distance_km?: number;
  distance?: number;
}

export interface NearbyStoresResponse {
  stores: BusinessStore[];
  search_location: {
    latitude: number;
    longitude: number;
  };
  search_radius_km: number;
  total_count: number;
  business_type_filter?: string;
}

export interface BusinessStatistics {
  business_type_stats: {
    business_name: string;
    store_count: number;
    percentage: number;
  }[];
  region_stats: {
    region_name: string;
    store_count: number;
  }[];
  filters: {
    sido_name?: string;
    sigungu_name?: string;
  };
}

export const businessStoreService = {
  // 주변 상가 조회
  async getNearbyStores(
    latitude: number,
    longitude: number,
    radiusKm: number = 1.0,
    businessType?: string,
    limit: number = 100
  ): Promise<NearbyStoresResponse> {
    const params = new URLSearchParams({
      latitude: latitude.toString(),
      longitude: longitude.toString(),
      radius_km: radiusKm.toString(),
      limit: limit.toString(),
    });

    if (businessType) {
      params.append('business_type', businessType);
    }

    const response = await api.get(`/business-stores/nearby?${params}`);
    return response.data;
  },

  // 지역별 상가 조회
  async getStoresByRegion(
    sidoName?: string,
    sigunguName?: string,
    dongName?: string,
    businessType?: string,
    page: number = 1,
    pageSize: number = 50
  ) {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
    });

    if (sidoName) params.append('sido_name', sidoName);
    if (sigunguName) params.append('sigungu_name', sigunguName);
    if (dongName) params.append('dong_name', dongName);
    if (businessType) params.append('business_type', businessType);

    const response = await api.get(`/business-stores/by-region?${params}`);
    return response.data;
  },

  // 상가 통계 조회
  async getBusinessStatistics(
    sidoName?: string,
    sigunguName?: string
  ): Promise<BusinessStatistics> {
    const params = new URLSearchParams();
    if (sidoName) params.append('sido_name', sidoName);
    if (sigunguName) params.append('sigungu_name', sigunguName);

    const response = await api.get(`/business-stores/statistics?${params}`);
    return response.data;
  },

  // 데이터 동기화
  async syncBusinessData(sidoCd: string, sigunguCd?: string) {
    const params = new URLSearchParams({
      sido_cd: sidoCd,
    });

    if (sigunguCd) {
      params.append('sigungu_cd', sigunguCd);
    }

    const response = await api.post(`/business-stores/sync-data?${params}`);
    return response.data;
  },
}; 
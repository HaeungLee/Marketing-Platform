import apiClient from "./api";
import type {
  Business,
  ContentGenerationRequest,
  ContentGenerationResponse,
  TargetAudienceResponse,
  DashboardData,
} from "../types/api";

// 비즈니스 관련 API
export const businessApi = {
  // 업종 카테고리 조회
  getCategories: async () => {
    const response = await apiClient.get("/business/categories");
    return response.data;
  },

  // 비즈니스 생성
  createBusiness: async (data: Omit<Business, "id" | "created_at">) => {
    const response = await apiClient.post("/business/", {
      name: data.name,
      category: data.category,
      description: data.description,
      latitude: data.latitude,
      longitude: data.longitude,
      address: data.address,
      phone: data.phone,
      website: data.website,
      target_radius_km: data.target_radius_km,
    });
    return response.data;
  },

  // 비즈니스 조회
  getBusiness: async (businessId: string) => {
    const response = await apiClient.get(`/business/${businessId}`);
    return response.data;
  },

  // 사용자 비즈니스 목록 조회
  getUserBusinesses: async () => {
    const response = await apiClient.get("/business/");
    return response.data;
  },

  // 상권 정보 조회
  getAreaInfo: async (businessId: string, radiusKm: number = 1.0) => {
    const response = await apiClient.get(`/business/${businessId}/area-info`, {
      params: { radius_km: radiusKm },
    });
    return response.data;
  },
};

// 콘텐츠 생성 관련 API
export const contentApi = {
  // 콘텐츠 생성
  generateContent: async (
    data: ContentGenerationRequest
  ): Promise<ContentGenerationResponse> => {
    const response = await apiClient.post("/content/generate", data);
    return response.data;
  },

  // 해시태그 생성
  generateHashtags: async (data: {
    content: string;
    business_name: string;
    business_category: string;
    max_count?: number;
  }) => {
    const response = await apiClient.post("/content/hashtags", data);
    return response.data;
  },

  // 키워드 분석
  analyzeKeywords: async (text: string) => {
    const response = await apiClient.post("/content/keywords", { text });
    return response.data;
  },

  // 성능 측정
  measurePerformance: async (modelName: string, prompt: string) => {
    const response = await apiClient.post("/content/performance", {
      model_name: modelName,
      prompt,
    });
    return response.data;
  },

  // 사용 가능한 모델 목록
  getAvailableModels: async () => {
    const response = await apiClient.get("/content/models");
    return response.data;
  },

  // 콘텐츠 템플릿 조회
  getContentTemplate: async (contentType: string) => {
    const response = await apiClient.get(`/content/templates/${contentType}`);
    return response.data;
  },
};

// 분석 관련 API
export const analysisApi = {
  // 타겟 고객층 분석
  analyzeTargetAudience: async (data: {
    business_id: string;
    business_category: string;
    latitude: number;
    longitude: number;
    radius_km?: number;
    product_type?: string;
    price_range?: string;
  }): Promise<TargetAudienceResponse> => {
    const response = await apiClient.post("/analysis/target-audience", data);
    return response.data;
  },

  // 경쟁사 분석
  analyzeCompetitors: async (data: {
    business_category: string;
    latitude: number;
    longitude: number;
    radius_km?: number;
  }) => {
    const response = await apiClient.post("/analysis/competitors", data);
    return response.data;
  },

  // 트렌드 분석
  analyzeTrends: async (data: {
    business_category: string;
    period_months?: number;
    region?: string;
  }) => {
    const response = await apiClient.post("/analysis/trends", data);
    return response.data;
  },

  // 대시보드 데이터 조회
  getDashboardData: async (businessId: string): Promise<DashboardData> => {
    const response = await apiClient.get(`/analysis/dashboard/${businessId}`);
    return response.data;
  },

  // 샘플 데이터 조회
  getSampleData: async (dataType: string) => {
    const response = await apiClient.get(`/analysis/sample-data/${dataType}`);
    return response.data;
  },
};

// 인증 관련 API
export const authApi = {
  // 소셜 로그인 URL 조회
  getSocialLoginUrl: async (provider: string) => {
    const response = await apiClient.get(`/auth/social/${provider}/url`);
    return response.data;
  },

  // 소셜 로그인 콜백 처리
  handleSocialCallback: async (provider: string, code: string) => {
    const response = await apiClient.post(`/auth/social/${provider}/callback`, {
      code,
    });
    return response.data;
  },

  // 토큰 갱신
  refreshToken: async (refreshToken: string) => {
    const response = await apiClient.post("/auth/refresh", {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  // 로그아웃
  logout: async () => {
    const response = await apiClient.post("/auth/logout");
    return response.data;
  },

  // 개인 회원가입
  registerPersonal: async (data: any) => {
    const response = await apiClient.post("/auth/register/personal", data);
    return response.data;
  },

  // 사업자 회원가입
  registerBusiness: async (data: any) => {
    const response = await apiClient.post("/auth/register/business", data);
    return response.data;
  },
  // 로그인
  login: async (userId: string, password: string) => {
    const requestData = {
      user_id: userId,
      password: password,
    };
    console.log(
      "Sending login request with:",
      JSON.stringify(requestData, null, 2)
    ); // 디버깅용 로그
    try {
      const response = await apiClient.post("/auth/login", requestData);
      console.log("Login response:", response.data); // 디버깅용 로그
      return response.data;
    } catch (error: any) {
      console.error("Login request failed:", {
        requestData,
        error: error.response?.data,
        status: error.response?.status,
        headers: error.response?.headers,
      });
      throw error;
    }
  },

  // 사용자 정보 가져오기
  getCurrentUser: async () => {
    const response = await apiClient.get("/auth/me");
    return response.data;
  },

  // 이메일 인증 메일 발송
  sendVerificationEmail: async (email: string) => {
    const response = await apiClient.post("/auth/send-verification-email", {
      email,
    });
    return response.data;
  },

  // 이메일 인증 코드 확인
  verifyEmail: async (email: string, code: string) => {
    const response = await apiClient.post("/auth/verify-email", {
      email,
      code,
    });
    return response.data;
  },

  // 비밀번호 찾기 이메일 발송
  forgotPassword: async (email: string) => {
    const response = await apiClient.post("/auth/forgot-password", { email });
    return response.data;
  },

  // 비밀번호 재설정
  resetPassword: async (token: string, newPassword: string) => {
    const response = await apiClient.post("/auth/reset-password", {
      token,
      new_password: newPassword,
    });
    return response.data;
  },
};

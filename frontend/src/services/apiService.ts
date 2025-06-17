import apiClient from "./api";
import type {
  Business,
  ContentGenerationRequest,
  ContentGenerationResponse,
  ImageGenerationRequest,
  ImageGenerationResponse,
  TargetAudienceResponse,
  DashboardData,
} from "../types/api";

export const authApi = {
  // 소셜 로그인 URL 조회
  getSocialLoginUrl: async (provider: string) => {
    const response = await apiClient.get(`/auth/social/${provider}/url`);
    return response.data;
  },
  // 소셜 로그인 콜백 처리
  handleSocialCallback: async (
    provider: string,
    code: string,
    state: string
  ) => {
    const response = await apiClient.post(
      `/auth/social/${provider}/callback`,
      {
        code: code,
        state: state,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.data;
  },
  // 로그인
  login: async (userId: string, password: string) => {
    const requestData = {
      user_id: userId,
      password: password,
    };
    try {
      const response = await apiClient.post("/auth/login", requestData);
      return response.data;
    } catch (error: any) {
      console.error("Login error:", error);
      throw error;
    }
  },

  // 로그아웃
  logout: async () => {
    const response = await apiClient.post("/auth/logout");
    return response.data;
  },

  // 토큰 갱신
  refreshToken: async (refreshToken: string) => {
    const response = await apiClient.post("/auth/refresh", {
      refresh_token: refreshToken,
    });
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

  // 이메일 인증 코드 전송
  sendVerificationEmail: async (email: string) => {
    const response = await apiClient.post("/auth/verify-email/send", {
      email: email,
    });
    return response.data;
  },

  // 이메일 인증 코드 확인
  verifyEmail: async (email: string, code: string) => {
    const response = await apiClient.post("/auth/verify-email/verify", {
      email: email,
      code: code,
    });
    return response.data;
  },
};

export const businessApi = {
  // 업종 카테고리 조회
  getCategories: async () => {
    const response = await apiClient.get("/business/categories");
    return response.data;
  },

  // 비즈니스 생성
  createBusiness: async (data: Omit<Business, "id" | "created_at">) => {
    const response = await apiClient.post("/business/", data);
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
};

export const contentApi = {
  // 콘텐츠 생성
  generateContent: async (
    data: ContentGenerationRequest
  ): Promise<ContentGenerationResponse> => {
    const response = await apiClient.post("/content/generate", data);
    return response.data;
  },   // 이미지 생성
  generateImage: async (
    data: ImageGenerationRequest
  ): Promise<ImageGenerationResponse> => {
    // 이미지 생성 API는 /api/v1 prefix 밖에 있으므로 직접 호출
    const response = await fetch("http://localhost:8000/api/images/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(localStorage.getItem("access_token") && {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        }),
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  },
};

export const analysisApi = {
  // 타겟 고객층 분석
  analyzeTargetAudience: async (data: {
    business_id: string;
    business_category: string;
    latitude: number;
    longitude: number;
    radius_km?: number;
  }): Promise<TargetAudienceResponse> => {
    const response = await apiClient.post("/analysis/target-audience", data);
    return response.data;
  },

  // 대시보드 데이터 조회
  getDashboardData: async (businessId: string): Promise<DashboardData> => {
    const response = await apiClient.get(`/analysis/dashboard/${businessId}`);
    return response.data;
  },
};

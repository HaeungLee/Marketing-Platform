import React, { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useToast } from "@chakra-ui/react";
import { authApi } from "../services/apiService";

const AuthCallbackPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const toast = useToast();

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get("code");
      const state = searchParams.get("state");
      const provider = window.location.pathname.split("/")[3]; // /auth/callback/{provider}

      if (!code) {
        toast({
          title: "로그인 실패",
          description: "인증 코드를 받지 못했습니다.",
          status: "error",
          duration: 5000,
          isClosable: true,
        });
        navigate("/login");
        return;
      }
      try {
        // provider, code, state가 모두 있는지 확인
        if (!provider || !code || !state) {
          console.error("Missing required parameters:", {
            provider,
            code,
            state,
          });
          throw new Error("필수 파라미터가 누락되었습니다.");
        }

        const response = await authApi.handleSocialCallback(
          provider,
          code,
          state
        );
        console.log("Social callback response:", response);

        // 토큰 저장
        localStorage.setItem("access_token", response.access_token);
        localStorage.setItem("user_id", response.user_id);
        localStorage.setItem("user_type", response.user_type);

        toast({
          title: "로그인 성공",
          description: "환영합니다!",
          status: "success",
          duration: 3000,
          isClosable: true,
        });

        // /app으로 리다이렉션
        navigate("/app");
      } catch (error: any) {
        console.error("Social login callback error:", error);
        console.error("Error response:", error.response?.data);
        console.error("Error status:", error.response?.status);

        const errorMessage =
          error.response?.data?.detail ||
          "소셜 로그인 처리 중 오류가 발생했습니다.";
        console.error("Error message:", errorMessage);

        toast({
          title: "로그인 실패",
          description: errorMessage,
          status: "error",
          duration: 5000,
          isClosable: true,
        });

        // 에러가 발생해도 일단 콘솔에만 출력하고 사용자는 홈으로 리다이렉트
        navigate("/");
      }
    };

    handleCallback();
  }, [searchParams, navigate, toast]);

  return null; // 로딩 중에는 아무것도 표시하지 않음
};

export default AuthCallbackPage;

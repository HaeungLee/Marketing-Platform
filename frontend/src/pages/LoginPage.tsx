import { useState } from "react";
import {
  Button,
  FormControl,
  FormLabel,
  FormErrorMessage,
  Input,
  InputGroup,
  InputRightElement,
  Stack,
  VStack,
  Heading,
  Text,
  Container,
  useToast,
  IconButton,
  Link,
  HStack,
  Divider,
  Card,
  CardBody,
} from "@chakra-ui/react";
import { useForm, SubmitHandler } from "react-hook-form";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import { FiEye, FiEyeOff, FiArrowLeft } from "react-icons/fi";
import { FaGoogle } from "react-icons/fa";
import { SiKakaotalk, SiNaver } from "react-icons/si";
import { authApi } from "../services/apiService";

interface LoginFormData {
  user_id: string;
  password: string;
}

const LoginPage = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>();
  const handleFormSubmit: SubmitHandler<LoginFormData> = async (data) => {
    setIsSubmitting(true);
    try {
      const response = await authApi.login(data.user_id, data.password);

      // 토큰을 로컬 스토리지에 저장
      localStorage.setItem("access_token", response.access_token);
      localStorage.setItem("user_id", response.user_id);
      localStorage.setItem("user_type", response.user_type);

      toast({
        title: "로그인 성공",
        description: "환영합니다!",
        status: "success",
        duration: 3000,
        isClosable: true,
      }); // 로그인 성공 시 /app으로 리다이렉트
      navigate("/app");
    } catch (error: any) {
      console.error("Login error details:", {
        data: error.response?.data,
        status: error.response?.status,
        headers: error.response?.headers,
        config: error.config,
      });
      console.error(
        "Error response data:",
        JSON.stringify(error.response?.data, null, 2)
      ); // 추가된 로그
      let errorMessage = "로그인에 실패했습니다.";
      if (error.response?.data?.detail) {
        if (typeof error.response.data.detail === "string") {
          errorMessage = error.response.data.detail;
        } else if (Array.isArray(error.response.data.detail)) {
          errorMessage = error.response.data.detail[0]?.msg || errorMessage;
        }
      }

      toast({
        title: "로그인 실패",
        description: errorMessage,
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };
  const handleSocialLogin = async (provider: string) => {
    try {
      const response = await authApi.getSocialLoginUrl(provider);
      if (response.url) {
        window.location.href = response.url;
      } else {
        throw new Error("소셜 로그인 URL을 받지 못했습니다.");
      }
    } catch (error: any) {
      console.error("Social login error:", error);
      toast({
        title: "소셜 로그인 실패",
        description:
          error.response?.data?.detail ||
          "소셜 로그인을 시작할 수 없습니다. 잠시 후 다시 시도해주세요.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Container maxW="container.md" py={10}>
      <Card bg="white" shadow="xl" borderRadius="xl">
        <CardBody>
          <VStack spacing={6}>
            <HStack w="100%" mb={4}>
              <IconButton
                aria-label="홈으로"
                icon={<FiArrowLeft />}
                variant="ghost"
                onClick={() => navigate("/")}
              />
              <Heading size="lg" textAlign="center" flex="1">
                로그인
              </Heading>
            </HStack>

            <form
              onSubmit={handleSubmit(handleFormSubmit)}
              style={{ width: "100%" }}
            >
              <VStack spacing={4} w="full">
                {" "}
                <FormControl isInvalid={!!errors.user_id}>
                  <FormLabel>아이디</FormLabel>
                  <Input
                    type="text"
                    placeholder="사용자 아이디를 입력하세요"
                    {...register("user_id", {
                      required: "아이디는 필수입니다",
                      minLength: {
                        value: 4,
                        message: "아이디는 최소 4자 이상이어야 합니다",
                      },
                    })}
                  />
                  <FormErrorMessage>
                    {errors.user_id && errors.user_id.message}
                  </FormErrorMessage>
                </FormControl>
                <FormControl isInvalid={!!errors.password}>
                  <FormLabel>비밀번호</FormLabel>
                  <InputGroup>
                    <Input
                      type={showPassword ? "text" : "password"}
                      placeholder="비밀번호를 입력하세요"
                      {...register("password", {
                        required: "비밀번호는 필수입니다",
                        minLength: {
                          value: 8,
                          message: "비밀번호는 최소 8자 이상이어야 합니다",
                        },
                      })}
                    />
                    <InputRightElement>
                      <IconButton
                        aria-label={
                          showPassword ? "비밀번호 숨기기" : "비밀번호 보기"
                        }
                        icon={showPassword ? <FiEyeOff /> : <FiEye />}
                        variant="ghost"
                        onClick={() => setShowPassword(!showPassword)}
                      />
                    </InputRightElement>
                  </InputGroup>
                  <FormErrorMessage>
                    {errors.password && errors.password.message}
                  </FormErrorMessage>
                </FormControl>
                <Button
                  type="submit"
                  colorScheme="blue"
                  size="lg"
                  w="full"
                  isLoading={isSubmitting}
                >
                  로그인
                </Button>
              </VStack>
            </form>

            <HStack w="full" spacing={4}>
              <Divider />
              <Text color="gray.500" fontSize="sm">
                또는
              </Text>
              <Divider />
            </HStack>

            <Stack w="full" spacing={4}>
              <Button
                leftIcon={<FaGoogle />}
                variant="outline"
                onClick={() => handleSocialLogin("google")}
              >
                Google로 로그인
              </Button>
              <Button
                leftIcon={<SiKakaotalk />}
                variant="outline"
                colorScheme="yellow"
                onClick={() => handleSocialLogin("kakao")}
              >
                카카오로 로그인
              </Button>{" "}
              <Button
                leftIcon={<SiNaver />}
                variant="outline"
                bg="#03c75a"
                color="white"
                _hover={{ bg: "#02b350" }}
                onClick={() => handleSocialLogin("naver")}
              >
                네이버로 로그인
              </Button>
            </Stack>

            <HStack spacing={2} justify="center">
              <Text>계정이 없으신가요?</Text>
              <Link as={RouterLink} to="/register" color="blue.500">
                회원가입
              </Link>
            </HStack>

            <Link as={RouterLink} to="/forgot-password" color="blue.500">
              비밀번호를 잊으셨나요?
            </Link>
          </VStack>
        </CardBody>
      </Card>
    </Container>
  );
};

export default LoginPage;

import React, { useState } from "react";
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  FormErrorMessage,
  Input,
  InputGroup,
  InputRightElement,
  VStack,
  Heading,
  Text,
  Container,
  useToast,
  useColorModeValue,
  IconButton,
  Card,
  CardBody,
  Link,
  HStack,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import { useNavigate, Link as RouterLink, useSearchParams } from "react-router-dom";
import { FiEye, FiEyeOff, FiArrowLeft } from "react-icons/fi";
import { authApi } from "../services/apiService";

interface ForgotPasswordFormData {
  email: string;
  password?: string;
  confirmPassword?: string;
}

const ForgotPasswordPage = () => {
  const [searchParams] = useSearchParams();
  const resetToken = searchParams.get("token");
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();
  const bgGradient = useColorModeValue(
    "linear(to-br, brand.50, blue.50, purple.50)",
    "linear(to-br, gray.900, blue.900, purple.900)"
  );

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<ForgotPasswordFormData>();

  const password = watch("password");

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setIsSubmitting(true);
    try {
      await authApi.forgotPassword(data.email);
      toast({
        title: "이메일 전송 완료",
        description: "비밀번호 재설정 링크가 이메일로 전송되었습니다.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || "이메일 전송에 실패했습니다.";
      toast({
        title: "이메일 전송 실패",
        description: errorMessage,
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResetPassword = async (data: ForgotPasswordFormData) => {
    if (!data.password || !data.confirmPassword) return;
    
    if (data.password !== data.confirmPassword) {
      toast({
        title: "비밀번호 불일치",
        description: "비밀번호가 일치하지 않습니다.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsSubmitting(true);
    try {
      await authApi.resetPassword(resetToken!, data.password);
      toast({
        title: "비밀번호 재설정 완료",
        description: "비밀번호가 성공적으로 재설정되었습니다.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      navigate("/login");
    } catch (error) {
      toast({
        title: "비밀번호 재설정 실패",
        description: "비밀번호 재설정에 실패했습니다.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Box minH="100vh" bg={bgGradient}>
      <Container maxW="container.md" py={10}>
        <Card bg="white" shadow="xl" borderRadius="xl">
          <CardBody>
            <VStack spacing={6}>
              <HStack w="100%" mb={4}>
                <IconButton
                  aria-label="뒤로가기"
                  icon={<FiArrowLeft />}
                  variant="ghost"
                  onClick={() => navigate("/login")}
                />
                <Heading size="lg" textAlign="center" flex="1">
                  {resetToken ? "비밀번호 재설정" : "비밀번호 찾기"}
                </Heading>
              </HStack>

              {resetToken ? (
                <form onSubmit={handleSubmit(handleResetPassword)}>
                  <VStack spacing={4}>
                    <FormControl isRequired isInvalid={!!errors.password}>
                      <FormLabel>새 비밀번호</FormLabel>
                      <InputGroup>
                        <Input
                          type={showPassword ? "text" : "password"}
                          placeholder="새 비밀번호 (8자 이상)"
                          {...register("password", {
                            required: "비밀번호는 필수입니다",
                            minLength: {
                              value: 8,
                              message: "비밀번호는 8자 이상이어야 합니다",
                            },
                            pattern: {
                              value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
                              message: "비밀번호는 영문 대/소문자, 숫자, 특수문자를 포함해야 합니다",
                            },
                          })}
                        />
                        <InputRightElement>
                          <IconButton
                            aria-label={showPassword ? "비밀번호 숨기기" : "비밀번호 보기"}
                            icon={showPassword ? <FiEyeOff /> : <FiEye />}
                            variant="ghost"
                            onClick={() => setShowPassword(!showPassword)}
                          />
                        </InputRightElement>
                      </InputGroup>
                      <FormErrorMessage>{errors.password?.message}</FormErrorMessage>
                    </FormControl>

                    <FormControl isRequired isInvalid={!!errors.confirmPassword}>
                      <FormLabel>비밀번호 확인</FormLabel>
                      <InputGroup>
                        <Input
                          type={showPassword ? "text" : "password"}
                          placeholder="비밀번호를 다시 입력하세요"
                          {...register("confirmPassword", {
                            required: "비밀번호 확인은 필수입니다",
                            validate: (value) =>
                              value === password || "비밀번호가 일치하지 않습니다",
                          })}
                        />
                      </InputGroup>
                      <FormErrorMessage>{errors.confirmPassword?.message}</FormErrorMessage>
                    </FormControl>

                    <Button
                      type="submit"
                      colorScheme="brand"
                      w="100%"
                      size="lg"
                      isLoading={isSubmitting}
                      loadingText="처리중..."
                    >
                      비밀번호 재설정
                    </Button>
                  </VStack>
                </form>
              ) : (
                <form onSubmit={handleSubmit(onSubmit)}>
                  <VStack spacing={4}>
                    <FormControl isRequired isInvalid={!!errors.email}>
                      <FormLabel>이메일</FormLabel>
                      <Input
                        type="email"
                        placeholder="가입한 이메일을 입력하세요"
                        {...register("email", {
                          required: "이메일은 필수입니다",
                          pattern: {
                            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                            message: "올바른 이메일 형식이 아닙니다",
                          },
                        })}
                      />
                      <FormErrorMessage>{errors.email?.message}</FormErrorMessage>
                    </FormControl>

                    <Button
                      type="submit"
                      colorScheme="brand"
                      w="100%"
                      size="lg"
                      isLoading={isSubmitting}
                      loadingText="처리중..."
                    >
                      비밀번호 재설정 링크 받기
                    </Button>
                  </VStack>
                </form>
              )}

              <HStack spacing={1} fontSize="sm" color="gray.600">
                <Text>계정이 기억나셨나요?</Text>
                <Link
                  as={RouterLink}
                  to="/login"
                  color="brand.500"
                  fontWeight="medium"
                >
                  로그인하기
                </Link>
              </HStack>
            </VStack>
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
};

export default ForgotPasswordPage; 
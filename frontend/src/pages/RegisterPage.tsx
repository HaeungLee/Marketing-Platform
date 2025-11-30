import React, { useState } from "react";
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  FormErrorMessage,
  FormHelperText,
  Input,
  InputGroup,
  InputRightElement,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  VStack,
  Heading,
  Text,
  Container,
  useColorModeValue,
  IconButton,
  Select,
  Card,
  CardBody,
  Link,
  HStack,
  Divider,
  Checkbox,
} from "@chakra-ui/react";
import { useForm, SubmitHandler, FieldValues } from "react-hook-form";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import { FiEye, FiEyeOff, FiArrowLeft } from "react-icons/fi";
import { FaGoogle } from "react-icons/fa";
import { SiKakaotalk, SiNaver } from "react-icons/si";
import { authApi } from "../services/apiService";

const businessCategories = [
  { value: "cafe", label: "카페" },
  { value: "restaurant", label: "일반음식점" },
  { value: "retail", label: "소매업" },
  { value: "beauty", label: "미용업" },
  { value: "healthcare", label: "의료/건강관리" },
  { value: "education", label: "교육" },
  { value: "other", label: "기타" },
];

interface FormData extends FieldValues {
  user_id: string;
  email: string;
  username: string;
  password: string;
  confirmPassword: string;
  phone?: string;
  termsAgreed: boolean;
  business_profile?: {
    business_name: string;
    business_registration_number: string;
    business_type: string;
    business_category: string;
    address: string;
    representative_name: string;
  };
}

interface PersonalRegisterFormProps {
  onSubmit: (data: FormData) => Promise<void>;
}

const PersonalRegisterForm: React.FC<PersonalRegisterFormProps> = ({
  onSubmit,
}) => {
  const toast = useToast();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isEmailVerifying, setIsEmailVerifying] = useState(false);
  const [verificationCode, setVerificationCode] = useState("");
  const [isEmailVerified, setIsEmailVerified] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<FormData>();

  const email = watch("email");
  const password = watch("password");

  const handleSendVerificationEmail = async () => {
    if (!email) {
      toast({
        title: "이메일 입력 필요",
        description: "이메일을 먼저 입력해주세요.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsEmailVerifying(true);
    try {
      await authApi.sendVerificationEmail(email);
      toast({
        title: "인증 메일 발송",
        description: "입력하신 이메일로 인증 코드를 발송했습니다.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || "인증 메일 발송에 실패했습니다.";
      toast({
        title: "인증 메일 발송 실패",
        description:
          typeof errorMessage === "string"
            ? errorMessage
            : "인증 메일 발송에 실패했습니다.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsEmailVerifying(false);
    }
  };

  const handleVerifyEmail = async () => {
    if (!verificationCode) {
      toast({
        title: "인증 코드 입력 필요",
        description: "인증 코드를 입력해주세요.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    try {
      await authApi.verifyEmail(email, verificationCode);
      setIsEmailVerified(true);
      toast({
        title: "이메일 인증 완료",
        description: "이메일이 성공적으로 인증되었습니다.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || "이메일 인증에 실패했습니다.";
      toast({
        title: "이메일 인증 실패",
        description:
          typeof errorMessage === "string"
            ? errorMessage
            : "이메일 인증에 실패했습니다.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleFormSubmit: SubmitHandler<FormData> = async (data) => {
    if (!isEmailVerified) {
      toast({
        title: "이메일 인증 필요",
        description: "이메일 인증을 완료해주세요.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    if (!data.termsAgreed) {
      toast({
        title: "이용약관 동의 필요",
        description: "이용약관에 동의해주세요.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(data);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <VStack spacing={4}>
        <FormControl isRequired isInvalid={!!errors.user_id}>
          <FormLabel>아이디</FormLabel>
          <Input
            placeholder="아이디 (4-20자)"
            {...register("user_id", {
              required: "아이디는 필수입니다",
              minLength: {
                value: 4,
                message: "아이디는 4자 이상이어야 합니다",
              },
              maxLength: {
                value: 20,
                message: "아이디는 20자 이하여야 합니다",
              },
              pattern: {
                value: /^[a-zA-Z0-9_]+$/,
                message: "아이디는 영문, 숫자, 언더스코어(_)만 사용 가능합니다",
              },
            })}
          />
          <FormErrorMessage>
            {errors.user_id?.message as string}
          </FormErrorMessage>
        </FormControl>

        <FormControl isRequired isInvalid={!!errors.email}>
          <FormLabel>이메일</FormLabel>
          <InputGroup>
            <Input
              type="email"
              placeholder="example@domain.com"
              {...register("email", {
                required: "이메일은 필수입니다",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "올바른 이메일 형식이 아닙니다",
                },
              })}
            />
            <InputRightElement width="4.5rem">
              <Button
                h="1.75rem"
                size="sm"
                onClick={handleSendVerificationEmail}
                isLoading={isEmailVerifying}
                isDisabled={!email || isEmailVerified}
              >
                {isEmailVerified ? "인증완료" : "인증하기"}
              </Button>
            </InputRightElement>
          </InputGroup>
          <FormErrorMessage>{errors.email?.message as string}</FormErrorMessage>
        </FormControl>

        {!isEmailVerified && (
          <FormControl>
            <FormLabel>이메일 인증 코드</FormLabel>
            <InputGroup>
              <Input
                placeholder="인증 코드를 입력하세요"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
              />
              <InputRightElement width="4.5rem">
                <Button
                  h="1.75rem"
                  size="sm"
                  onClick={handleVerifyEmail}
                  isDisabled={!verificationCode}
                >
                  확인
                </Button>
              </InputRightElement>
            </InputGroup>
          </FormControl>
        )}

        <FormControl isRequired isInvalid={!!errors.username}>
          <FormLabel>사용자명</FormLabel>
          <Input
            placeholder="사용자명 (2-20자)"
            {...register("username", {
              required: "사용자명은 필수입니다",
              minLength: {
                value: 2,
                message: "사용자명은 2자 이상이어야 합니다",
              },
              maxLength: {
                value: 20,
                message: "사용자명은 20자 이하여야 합니다",
              },
            })}
          />
          <FormErrorMessage>
            {errors.username?.message as string}
          </FormErrorMessage>
        </FormControl>

        <FormControl isRequired isInvalid={!!errors.password}>
          <FormLabel>비밀번호</FormLabel>
          <InputGroup>
            <Input
              type={showPassword ? "text" : "password"}
              placeholder="비밀번호 (8자 이상)"
              {...register("password", {
                required: "비밀번호는 필수입니다",
                minLength: {
                  value: 8,
                  message: "비밀번호는 8자 이상이어야 합니다",
                },
                pattern: {
                  value:
                    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
                  message:
                    "비밀번호는 영문 대/소문자, 숫자, 특수문자를 포함해야 합니다",
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
          <FormErrorMessage>
            {errors.password?.message as string}
          </FormErrorMessage>
          <FormHelperText>
            영문 대/소문자, 숫자, 특수문자를 포함한 8자 이상
          </FormHelperText>
        </FormControl>

        <FormControl isRequired isInvalid={!!errors.confirmPassword}>
          <FormLabel>비밀번호 확인</FormLabel>
          <InputGroup>
            <Input
              type={showConfirmPassword ? "text" : "password"}
              placeholder="비밀번호를 다시 입력하세요"
              {...register("confirmPassword", {
                required: "비밀번호 확인은 필수입니다",
                validate: (value: string) =>
                  value === password || "비밀번호가 일치하지 않습니다",
              })}
            />
            <InputRightElement>
              <IconButton
                aria-label={
                  showConfirmPassword ? "비밀번호 숨기기" : "비밀번호 보기"
                }
                icon={showConfirmPassword ? <FiEyeOff /> : <FiEye />}
                variant="ghost"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              />
            </InputRightElement>
          </InputGroup>
          <FormErrorMessage>
            {errors.confirmPassword?.message as string}
          </FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.phone}>
          <FormLabel>전화번호</FormLabel>
          <Input
            placeholder="01012345678 (-없이 입력)"
            {...register("phone", {
              pattern: {
                value: /^01[0-9]{8,9}$/,
                message: "올바른 전화번호 형식이 아닙니다",
              },
            })}
          />
          <FormErrorMessage>{errors.phone?.message as string}</FormErrorMessage>
        </FormControl>

        <FormControl isRequired isInvalid={!!errors.termsAgreed}>
          <Checkbox
            {...register("termsAgreed", {
              required: "이용약관 동의는 필수입니다",
            })}
          >
            <Text fontSize="sm">
              <Link color="brand.500" href="/terms" isExternal>
                이용약관
              </Link>
              과{" "}
              <Link color="brand.500" href="/privacy" isExternal>
                개인정보처리방침
              </Link>
              에 동의합니다
            </Text>
          </Checkbox>
          <FormErrorMessage>
            {errors.termsAgreed?.message as string}
          </FormErrorMessage>
        </FormControl>

        <Button
          type="submit"
          colorScheme="brand"
          w="100%"
          size="lg"
          isLoading={isSubmitting}
          loadingText="처리중..."
        >
          회원가입
        </Button>
      </VStack>
    </form>
  );
};

interface BusinessRegisterFormProps {
  onSubmit: (data: FormData) => Promise<void>;
}

const BusinessRegisterForm: React.FC<BusinessRegisterFormProps> = ({
  onSubmit,
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>();

  const handleFormSubmit: SubmitHandler<FormData> = async (data) => {
    setIsSubmitting(true);
    try {
      await onSubmit(data);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)}>
      <VStack spacing={6}>
        {/* 기본 정보 */}
        <Box w="100%">
          <Text fontSize="lg" fontWeight="bold" mb={4}>
            기본 정보
          </Text>
          <VStack spacing={4}>
            <FormControl isRequired isInvalid={!!errors.user_id}>
              <FormLabel>아이디</FormLabel>
              <Input
                placeholder="아이디 (4-20자)"
                {...register("user_id", {
                  required: "아이디는 필수입니다",
                  minLength: {
                    value: 4,
                    message: "아이디는 4자 이상이어야 합니다",
                  },
                  maxLength: {
                    value: 20,
                    message: "아이디는 20자 이하여야 합니다",
                  },
                  pattern: {
                    value: /^[a-zA-Z0-9_]+$/,
                    message:
                      "아이디는 영문, 숫자, 언더스코어(_)만 사용 가능합니다",
                  },
                })}
              />
              <FormErrorMessage>
                {errors.user_id?.message as string}
              </FormErrorMessage>
            </FormControl>

            <FormControl isRequired isInvalid={!!errors.email}>
              <FormLabel>이메일</FormLabel>
              <Input
                type="email"
                placeholder="example@domain.com"
                {...register("email", {
                  required: "이메일은 필수입니다",
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: "올바른 이메일 형식이 아닙니다",
                  },
                })}
              />
              <FormErrorMessage>
                {errors.email?.message as string}
              </FormErrorMessage>
            </FormControl>

            <FormControl isRequired isInvalid={!!errors.username}>
              <FormLabel>사용자명</FormLabel>
              <Input
                placeholder="사용자명 (2-20자)"
                {...register("username", {
                  required: "사용자명은 필수입니다",
                  minLength: {
                    value: 2,
                    message: "사용자명은 2자 이상이어야 합니다",
                  },
                  maxLength: {
                    value: 20,
                    message: "사용자명은 20자 이하여야 합니다",
                  },
                })}
              />
              <FormErrorMessage>
                {errors.username?.message as string}
              </FormErrorMessage>
            </FormControl>

            <FormControl isRequired isInvalid={!!errors.password}>
              <FormLabel>비밀번호</FormLabel>
              <InputGroup>
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="비밀번호 (8자 이상)"
                  {...register("password", {
                    required: "비밀번호는 필수입니다",
                    minLength: {
                      value: 8,
                      message: "비밀번호는 8자 이상이어야 합니다",
                    },
                    pattern: {
                      value:
                        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
                      message:
                        "비밀번호는 영문 대/소문자, 숫자, 특수문자를 포함해야 합니다",
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
                {errors.password?.message as string}
              </FormErrorMessage>
              <FormHelperText>
                영문 대/소문자, 숫자, 특수문자를 포함한 8자 이상
              </FormHelperText>
            </FormControl>

            <FormControl isInvalid={!!errors.phone}>
              <FormLabel>전화번호</FormLabel>
              <Input
                placeholder="01012345678 (-없이 입력)"
                {...register("phone", {
                  pattern: {
                    value: /^01[0-9]{8,9}$/,
                    message: "올바른 전화번호 형식이 아닙니다",
                  },
                })}
              />
              <FormErrorMessage>
                {errors.phone?.message as string}
              </FormErrorMessage>
            </FormControl>
          </VStack>
        </Box>

        {/* 사업자 정보 */}
        <Box w="100%">
          <Text fontSize="lg" fontWeight="bold" mb={4}>
            사업자 정보
          </Text>
          <VStack spacing={4}>
            <FormControl
              isRequired
              isInvalid={!!errors.business_profile?.business_name}
            >
              <FormLabel>상호명</FormLabel>
              <Input
                placeholder="상호명을 입력하세요"
                {...register("business_profile.business_name", {
                  required: "상호명은 필수입니다",
                  maxLength: {
                    value: 100,
                    message: "상호명은 100자 이하여야 합니다",
                  },
                })}
              />
              <FormErrorMessage>
                {errors.business_profile?.business_name?.message as string}
              </FormErrorMessage>
            </FormControl>

            <FormControl
              isRequired
              isInvalid={
                !!errors.business_profile?.business_registration_number
              }
            >
              <FormLabel>사업자등록번호</FormLabel>
              <Input
                placeholder="사업자등록번호를 입력하세요 (-없이 10자리)"
                {...register("business_profile.business_registration_number", {
                  required: "사업자등록번호는 필수입니다",
                  pattern: {
                    value: /^\d{10}$/,
                    message: "올바른 사업자등록번호 형식이 아닙니다",
                  },
                })}
              />
              <FormErrorMessage>
                {
                  errors.business_profile?.business_registration_number
                    ?.message as string
                }
              </FormErrorMessage>
            </FormControl>

            <FormControl
              isRequired
              isInvalid={!!errors.business_profile?.business_type}
            >
              <FormLabel>업종</FormLabel>
              <Select
                placeholder="업종을 선택하세요"
                {...register("business_profile.business_type", {
                  required: "업종은 필수입니다",
                })}
              >
                {businessCategories.map((category) => (
                  <option key={category.value} value={category.value}>
                    {category.label}
                  </option>
                ))}
              </Select>
              <FormErrorMessage>
                {errors.business_profile?.business_type?.message as string}
              </FormErrorMessage>
            </FormControl>

            <FormControl
              isRequired
              isInvalid={!!errors.business_profile?.business_category}
            >
              <FormLabel>업태</FormLabel>
              <Input
                placeholder="업태를 입력하세요"
                {...register("business_profile.business_category", {
                  required: "업태는 필수입니다",
                })}
              />
              <FormErrorMessage>
                {errors.business_profile?.business_category?.message as string}
              </FormErrorMessage>
            </FormControl>

            <FormControl
              isRequired
              isInvalid={!!errors.business_profile?.address}
            >
              <FormLabel>사업장 주소</FormLabel>
              <Input
                placeholder="사업장 주소를 입력하세요"
                {...register("business_profile.address", {
                  required: "주소는 필수입니다",
                })}
              />
              <FormErrorMessage>
                {errors.business_profile?.address?.message as string}
              </FormErrorMessage>
            </FormControl>

            <FormControl
              isRequired
              isInvalid={!!errors.business_profile?.representative_name}
            >
              <FormLabel>대표자명</FormLabel>
              <Input
                placeholder="대표자명을 입력하세요"
                {...register("business_profile.representative_name", {
                  required: "대표자명은 필수입니다",
                })}
              />
              <FormErrorMessage>
                {
                  errors.business_profile?.representative_name
                    ?.message as string
                }
              </FormErrorMessage>
            </FormControl>
          </VStack>
        </Box>

        <Button
          type="submit"
          colorScheme="brand"
          w="100%"
          size="lg"
          isLoading={isSubmitting}
          loadingText="처리중..."
        >
          회원가입
        </Button>
      </VStack>
    </form>
  );
};

const SocialLoginButtons = () => {
  const toast = useToast();

  const handleSocialLogin = async (provider: string) => {
    try {
      const { url } = await authApi.getSocialLoginUrl(provider);
      window.location.href = url;
    } catch (error: any) {
      toast({
        title: "소셜 로그인 실패",
        description: "소셜 로그인 연결에 실패했습니다.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <VStack spacing={4} w="100%">
      <Text fontSize="sm" color="gray.500">
        소셜 계정으로 간편하게 가입하기
      </Text>
      <HStack spacing={4} w="100%">
        <Button
          w="100%"
          leftIcon={<FaGoogle />}
          onClick={() => handleSocialLogin("google")}
          colorScheme="red"
          variant="outline"
        >
          Google
        </Button>
        <Button
          w="100%"
          leftIcon={<SiKakaotalk />}
          onClick={() => handleSocialLogin("kakao")}
          colorScheme="yellow"
          variant="outline"
        >
          Kakao
        </Button>
        <Button
          w="100%"
          leftIcon={<SiNaver />}
          onClick={() => handleSocialLogin("naver")}
          colorScheme="green"
          variant="outline"
        >
          Naver
        </Button>
      </HStack>
    </VStack>
  );
};

const RegisterPage = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const bgGradient = useColorModeValue(
    "linear(to-br, brand.50, blue.50, purple.50)",
    "linear(to-br, gray.900, blue.900, purple.900)"
  );

  const handlePersonalRegister = async (data: FormData) => {
    try {
      const response = await authApi.registerPersonal(data);
      toast({
        title: "회원가입 성공",
        description: "회원가입이 완료되었습니다.",
        status: "success",
        duration: 5000,
        isClosable: true,
      });
      navigate("/login");
    } catch (error: any) {
      toast({
        title: "회원가입 실패",
        description:
          error.response?.data?.detail || "회원가입 중 오류가 발생했습니다.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleBusinessRegister = async (data: FormData) => {
    try {
      const response = await authApi.registerBusiness(data);
      toast({
        title: "회원가입 성공",
        description: "사업자 회원가입이 완료되었습니다.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      localStorage.setItem("token", response.data.access_token);
      navigate("/app/business/setup");
    } catch (error: any) {
      toast({
        title: "회원가입 실패",
        description:
          error.response?.data?.detail || "회원가입 중 오류가 발생했습니다.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
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
                  onClick={() => navigate("/")}
                />
                <Heading size="lg" textAlign="center" flex="1">
                  회원가입
                </Heading>
              </HStack>

              <SocialLoginButtons />

              <Divider />

              <Tabs isFitted variant="enclosed" w="100%">
                <TabList mb="1em">
                  <Tab>개인 회원가입</Tab>
                  <Tab>사업자 회원가입</Tab>
                </TabList>
                <TabPanels>
                  <TabPanel>
                    <PersonalRegisterForm onSubmit={handlePersonalRegister} />
                  </TabPanel>
                  <TabPanel>
                    <BusinessRegisterForm onSubmit={handleBusinessRegister} />
                  </TabPanel>
                </TabPanels>
              </Tabs>

              <HStack spacing={1} fontSize="sm" color="gray.600">
                <Text>이미 계정이 있으신가요?</Text>
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

export default RegisterPage;

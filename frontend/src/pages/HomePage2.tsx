import React from "react";
import {
  Box,
  Container,
  Heading,
  Text,
  Button,
  VStack,
  HStack,
  SimpleGrid,
  Icon,
  Image,
  useColorModeValue,
  Flex,
  Stack,
} from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";
import {
  FiTarget,
  FiTrendingUp,
  FiEdit3,
  FiBarChart,
  FiUsers,
  FiZap,
} from "react-icons/fi";

const features = [
  {
    icon: FiTarget,
    title: "타겟 고객 분석",
    description:
      "공공데이터 기반으로 정확한 타겟 고객층을 분석하고 시각화합니다.",
  },
  {
    icon: FiEdit3,
    title: "AI 콘텐츠 생성",
    description:
      "블로그, 인스타그램, 유튜브, 전단지용 마케팅 콘텐츠를 자동 생성합니다.",
  },
  {
    icon: FiBarChart,
    title: "경쟁사 분석",
    description: "주변 경쟁업체를 분석하여 차별화 전략을 제시합니다.",
  },
  {
    icon: FiTrendingUp,
    title: "트렌드 분석",
    description: "업종별 검색 트렌드와 시장 동향을 실시간으로 분석합니다.",
  },
  {
    icon: FiUsers,
    title: "고객 인사이트",
    description:
      "고객 행동 패턴과 선호도를 분석하여 마케팅 전략을 최적화합니다.",
  },
  {
    icon: FiZap,
    title: "자동화 시스템",
    description: "반복적인 마케팅 업무를 자동화하여 효율성을 극대화합니다.",
  },
];

const HomePage: React.FC = () => {
  const bgGradient = useColorModeValue(
    "linear(to-br, brand.50, blue.50, purple.50)",
    "linear(to-br, gray.900, blue.900, purple.900)"
  );

  return (
    <Box minH="100vh" bg={bgGradient}>
      {/* 네비게이션 */}
      <Box as="nav" py={4} px={6}>
        <Container maxW="1200px">
          <Flex justify="space-between" align="center">
            <Text fontSize="xl" fontWeight="bold" color="brand.600">
              🚀 AI 마케팅 플랫폼
            </Text>
            <Stack direction={{ base: "column", md: "row" }} spacing={4}>
              <Button
                as={RouterLink}
                to="/login"
                size="lg"
                variant="outline"
                colorScheme="blue"
                px={8}
                _hover={{
                  transform: "translateY(-2px)",
                  boxShadow: "lg",
                }}
              >
                로그인
              </Button>
              <Button
                as={RouterLink}
                to="/app"
                size="lg"
                colorScheme="blue"
                px={8}
                _hover={{
                  transform: "translateY(-2px)",
                  boxShadow: "lg",
                }}
              >
                시작하기
              </Button>
            </Stack>
          </Flex>
        </Container>
      </Box>

      {/* 히어로 섹션 */}
      <Container maxW="1200px" py={20}>
        <VStack spacing={8} textAlign="center">
          <Box className="fade-in">
            <Heading
              size="2xl"
              bgGradient="linear(to-r, brand.400, purple.400)"
              bgClip="text"
              mb={4}
            >
              소상공인을 위한 스마트 마케팅
            </Heading>
            <Text fontSize="xl" color="gray.600" maxW="600px">
              AI와 공공데이터를 활용하여 효과적인 마케팅 콘텐츠를 생성하고, 타겟
              고객을 정확히 분석하는 올인원 플랫폼입니다.
            </Text>
          </Box>

          <HStack spacing={4} className="slide-in-left">
            <Button
              as={RouterLink}
              to="/app"
              size="lg"
              colorScheme="brand"
              leftIcon={<FiZap />}
            >
              무료로 시작하기
            </Button>
            <Button size="lg" variant="outline" colorScheme="brand">
              데모 보기
            </Button>
          </HStack>

          {/* 통계 정보 */}
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8} pt={16}>
            <VStack>
              <Text fontSize="3xl" fontWeight="bold" color="brand.500">
                95%
              </Text>
              <Text color="gray.600">마케팅 효율성 향상</Text>
            </VStack>
            <VStack>
              <Text fontSize="3xl" fontWeight="bold" color="brand.500">
                80%
              </Text>
              <Text color="gray.600">콘텐츠 제작 시간 단축</Text>
            </VStack>
            <VStack>
              <Text fontSize="3xl" fontWeight="bold" color="brand.500">
                200+
              </Text>
              <Text color="gray.600">만족한 소상공인</Text>
            </VStack>
          </SimpleGrid>
        </VStack>
      </Container>

      {/* 기능 소개 섹션 */}
      <Box bg="white" py={20}>
        <Container maxW="1200px">
          <VStack spacing={16}>
            <Box textAlign="center">
              <Heading size="xl" mb={4}>
                강력한 기능으로 마케팅을 혁신하세요
              </Heading>
              <Text fontSize="lg" color="gray.600">
                복잡한 마케팅 업무를 간단하고 효과적으로 해결합니다
              </Text>
            </Box>

            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={8}>
              {features.map((feature, index) => (
                <Box
                  key={index}
                  p={6}
                  bg="white"
                  borderRadius="xl"
                  boxShadow="lg"
                  _hover={{
                    transform: "translateY(-4px)",
                    boxShadow: "xl",
                  }}
                  transition="all 0.3s"
                  className="fade-in"
                >
                  <VStack align="start" spacing={4}>
                    <Icon
                      as={feature.icon}
                      fontSize="2xl"
                      color="brand.500"
                      p={2}
                      bg="brand.50"
                      borderRadius="lg"
                    />
                    <Heading size="md">{feature.title}</Heading>
                    <Text color="gray.600" fontSize="sm">
                      {feature.description}
                    </Text>
                  </VStack>
                </Box>
              ))}
            </SimpleGrid>
          </VStack>
        </Container>
      </Box>

      {/* CTA 섹션 */}
      <Box bg={bgGradient} py={20}>
        <Container maxW="800px">
          <VStack spacing={8} textAlign="center">
            <Heading size="xl" color="gray.800">
              지금 바로 시작해보세요
            </Heading>
            <Text fontSize="lg" color="gray.600">
              복잡한 설정 없이 5분 만에 첫 번째 마케팅 콘텐츠를 생성할 수
              있습니다.
            </Text>
            <Button
              as={RouterLink}
              to="/app"
              size="lg"
              colorScheme="brand"
              className="pulse"
            >
              무료 체험 시작하기
            </Button>
          </VStack>
        </Container>
      </Box>

      {/* 푸터 */}
      <Box bg="gray.800" color="white" py={8}>
        <Container maxW="1200px">
          <Flex
            justify="space-between"
            align="center"
            direction={{ base: "column", md: "row" }}
            gap={4}
          >
            <Text fontSize="sm">
              © 2025 AI 마케팅 플랫폼. 공모전 프로토타입입니다.
            </Text>
            <HStack spacing={4}>
              <Text fontSize="sm" color="gray.400">
                문의: demo@marketing-platform.com
              </Text>
            </HStack>
          </Flex>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage;

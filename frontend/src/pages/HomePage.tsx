import React, { useEffect } from 'react';
import {
  Box,
  Container,
  Flex,
  HStack,
  VStack,
  Text,
  Heading,
  Button,
  Link,
  Image,
  useColorModeValue,
  useDisclosure,
  Grid,
  GridItem,
  IconButton,
  Collapse,
} from '@chakra-ui/react';
import { HamburgerIcon, ChevronRightIcon } from '@chakra-ui/icons';
import { Link as RouterLink } from 'react-router-dom';
import logoImage from '../assets/logo.png';
import targetImage from '../assets/target.jpg';
import aiImage from '../assets/ai.webp';
import marketingImage from '../assets/marketing.webp';

// TypeScript 인터페이스
interface NavbarProps {}

interface HomePageProps {}

// 네비게이션 바 컴포넌트
const Navbar: React.FC<NavbarProps> = () => {
  const { isOpen, onToggle } = useDisclosure();
  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  return (
    <Box
      position="fixed"
      top="0"
      left="0"
      right="0"
      zIndex="50"
      bg={bg}
      backdropFilter="blur(10px)"
      borderBottom="1px"
      borderColor={borderColor}
      boxShadow="sm"
    >
      <Container maxW="container.xl" px={6} py={4}>
        <Flex justify="space-between" align="center">
          <Link href="#" display="flex" alignItems="center">
            <Image src={logoImage} alt="Group Ppeodeona" h="50px" />
          </Link>
          
          <HStack display={{ base: 'none', md: 'flex' }} spacing={6}>
            <Link href="#" color="gray.700" _hover={{ color: 'brand.500' }} transition="colors 0.2s">
              플랫폼 소개
            </Link>
            <Link href="#" color="gray.700" _hover={{ color: 'brand.500' }} transition="colors 0.2s">
              AI 기능
            </Link>
            <Link href="#" color="gray.700" _hover={{ color: 'brand.500' }} transition="colors 0.2s">
              요금제
            </Link>
            <Button
              as={RouterLink}
              to="/login"
              variant="outline"
              colorScheme="brand"
              size="sm"
              px={6}
            >
              로그인
            </Button>
            <Button
              as={RouterLink}
              to="/app"
              colorScheme="brand"
              size="sm"
              px={6}
            >
              시작하기
            </Button>
          </HStack>
          
          <IconButton
            display={{ base: 'flex', md: 'none' }}
            aria-label="메뉴 열기"
            icon={<HamburgerIcon />}
            variant="ghost"
            onClick={onToggle}
          />
        </Flex>
        
        {/* 모바일 메뉴 */}
        <Collapse in={isOpen}>
          <Box display={{ md: 'none' }} bg={bg} py={2}>
            <VStack spacing={2} align="stretch">
              <Link href="#" p={2} _hover={{ bg: 'brand.50' }} borderRadius="md">
                플랫폼 소개
              </Link>
              <Link href="#" p={2} _hover={{ bg: 'brand.50' }} borderRadius="md">
                AI 기능
              </Link>
              <Link href="#" p={2} _hover={{ bg: 'brand.50' }} borderRadius="md">
                요금제
              </Link>
              <VStack spacing={2} p={2}>
                <Button
                  variant="outline"
                  colorScheme="brand"
                  size="sm"
                  w="full"
                >
                  로그인
                </Button>
                <Button
                  colorScheme="brand"
                  size="sm"
                  w="full"
                >
                  시작하기
                </Button>
              </VStack>
            </VStack>
          </Box>
        </Collapse>
      </Container>
    </Box>
  );
};

// 메인 App 컴포넌트
const HomePage: React.FC<HomePageProps> = () => {
  // Inter 폰트 로드 (이미 theme.ts에서 Noto Sans KR로 설정되어 있음)
  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }, []);

  const placeholderImage = (width: number, height: number, text: string, bgColor = 'E0E7FF', textColor = '6366F1') => 
    `https://placehold.co/${width}x${height}/${bgColor}/${textColor}?text=${encodeURIComponent(text)}&font=Inter`;

  return (
    <Box fontFamily="'Noto Sans KR', sans-serif" color="gray.800">
      <Navbar />

      {/* Hero Section */}
      <Box
        pt={{ base: '32', md: '48' }}
        pb={{ base: '16', md: '24' }}
        bgGradient="linear(135deg, blue.100, purple.50, pink.100)"
      >
        <Container maxW="container.xl" px={6} textAlign="center">
          <Heading
            as="h1"
            size={{ base: '2xl', md: '4xl', lg: '4xl' }}
            fontWeight="extrabold"
            mb={6}
            lineHeight="tight"
          >
            <Text as="span" display="block">
              AI 마케팅 플랫폼
            </Text>
            <Text as="span" display="block" color="brand.500">
              소상공인의 성공을 뻗어나게 하다
            </Text>
          </Heading>
          <Text
            fontSize={{ base: 'lg', md: 'xl' }}
            color="gray.700"
            mb={10}
            maxW="3xl"
            mx="auto"
          >
            공공데이터 기반 타겟 분석부터 AI 콘텐츠 생성까지, 한국 시장에 특화된 마케팅 솔루션으로 여러분의 비즈니스를 성장시켜보세요.
          </Text>
          <Button
            bg="brand.500"
            color="white"
            fontWeight="semibold"
            px={10}
            py={4}
            size="lg"
            fontSize="lg"
            _hover={{
              bg: 'brand.600',
              transform: 'translateY(-2px)',
            }}
            boxShadow="xl"
            rightIcon={<ChevronRightIcon />}
          >
            무료로 시작하기
          </Button>
        </Container>
      </Box>

      {/* Feature Section 1: AI Assistance */}
      <Box py={{ base: '16', md: '24' }} bg="blue.50">
        <Container maxW="container.xl" px={6}>
          <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={12} alignItems="center">
            <Box textAlign={{ base: 'center', md: 'left' }}>
              <Heading as="h2" size={{ base: 'xl', md: '2xl' }} fontWeight="bold" mb={4} color="brand.700">
                공공데이터 기반 타겟 분석
              </Heading>
              <Text fontSize={{ base: 'xl', md: '2xl' }} color="gray.700" mb={6}>
                정확한 고객층을 찾아 맞춤형 전략을 제공합니다.
              </Text>
              <Text color="gray.600" lineHeight="relaxed">
                인구통계, 유동인구, 카드소비 데이터를 분석하여 여러분의 사업에 가장 적합한 타겟 고객을 찾고, 
                효과적인 마케팅 전략을 수립할 수 있도록 도와드립니다.
              </Text>
            </Box>
            <Box>
              <Image 
                src={targetImage} 
                alt="공공데이터 기반 타겟 분석" 
                borderRadius="xl"
                boxShadow="2xl"
                mx="auto"
                w="100%"
                h="auto"
                objectFit="cover"
                onError={(e: any) => e.target.src = placeholderImage(600, 400, '이미지 로드 실패', 'FECACA', '991B1B')}
              />
            </Box>
          </Grid>
        </Container>
      </Box>

      {/* Feature Section 2: Just Typing */}
      <Box py={{ base: '16', md: '24' }} bg="white">
        <Container maxW="container.xl" px={6}>
          <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={12} alignItems="center">
            <GridItem order={{ base: 2, md: 1 }}>
              <Image 
                src={aiImage} 
                alt="AI 콘텐츠 자동 생성" 
                borderRadius="xl"
                boxShadow="2xl"
                mx="auto"
                w="100%"
                h="auto"
                objectFit="cover"
                onError={(e: any) => e.target.src = placeholderImage(600, 400, '이미지 로드 실패', 'FECACA', '991B1B')}
              />
            </GridItem>
            <GridItem order={{ base: 1, md: 2 }} textAlign={{ base: 'center', md: 'left' }}>
              <Heading as="h2" size={{ base: 'xl', md: '2xl' }} fontWeight="bold" mb={4} color="green.600">
                AI 콘텐츠 자동 생성
              </Heading>
              <Text fontSize={{ base: 'xl', md: '2xl' }} color="gray.700" mb={6}>
                블로그, SNS, 전단지까지 한 번에 제작하세요.
              </Text>
              <Text color="gray.600" lineHeight="relaxed">
                네이버 블로그, 인스타그램, 유튜브 숏폼, 전단지 등 다양한 마케팅 콘텐츠를 
                AI가 업종과 타겟에 맞춰 자동으로 생성해드립니다.
              </Text>
            </GridItem>
          </Grid>
        </Container>
      </Box>
      
      {/* Feature Section 3: Awesome Design */}
      <Box py={{ base: '16', md: '24' }} bg="purple.500" color="white">
        <Container maxW="container.xl" px={6} textAlign="center">
          <Heading as="h2" size={{ base: 'xl', md: '2xl' }} fontWeight="bold" mb={4}>
            경쟁사 분석 & 트렌드 인사이트
          </Heading>
          <Text fontSize={{ base: 'xl', md: '2xl' }} mb={6} maxW="xl" mx="auto">
            시장을 이해하고 차별화된 전략을 세우세요.
          </Text>
          <Text color="purple.100" lineHeight="relaxed" maxW="2xl" mx="auto">
            주변 경쟁업체 분석, 업종별 검색 트렌드, 고객 행동 패턴 분석을 통해 
            경쟁력 있는 마케팅 전략을 수립하고 시장에서 우위를 점하세요.
          </Text>
        </Container>
      </Box>

      {/* Feature Section 4: Live Editing */}
      <Box py={{ base: '16', md: '24' }} bg="gray.100">
        <Container maxW="container.xl" px={6}>
          <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={12} alignItems="center">
            <Box textAlign={{ base: 'center', md: 'left' }}>
              <Heading as="h2" size={{ base: 'xl', md: '2xl' }} fontWeight="bold" mb={4} color="brand.700">
                실시간 성과 분석
              </Heading>
              <Text fontSize={{ base: 'xl', md: '2xl' }} color="gray.700" mb={6}>
                마케팅 효과를 한눈에 확인하세요.
              </Text>
              <Text color="gray.600" lineHeight="relaxed">
                콘텐츠 성과, 고객 반응, 매출 변화를 실시간으로 모니터링하고 
                데이터 기반의 인사이트로 마케팅 전략을 지속적으로 개선해나가세요.
              </Text>
            </Box>
            <Box>
              <Image 
                src={marketingImage} 
                alt="실시간 성과 분석 기능" 
                borderRadius="xl"
                boxShadow="2xl"
                mx="auto"
                w="100%"
                h="auto"
                objectFit="cover"
                onError={(e: any) => e.target.src = placeholderImage(600, 400, '이미지 로드 실패', 'FECACA', '991B1B')}
              />
            </Box>
          </Grid>
        </Container>
      </Box>

      {/* Feature Section 5: Languages */}
      <Box py={{ base: '16', md: '24' }} bg="brand.600" color="white">
        <Container maxW="container.xl" px={6}>
          <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={12} alignItems="center">
            <Box textAlign={{ base: 'center', md: 'left' }}>
              <Heading as="h1" size={{ base: '6xl', md: '6xl' }} fontWeight="extrabold" mb={4} color="brand.100">
                95%
              </Heading>
              <Text fontSize={{ base: '2xl', md: '3xl' }} color="brand.200" mb={4}>
                고객 만족도 목표
              </Text>
              <Text fontSize="lg" color="brand.100" lineHeight="relaxed">
                한국 소상공인을 위해 특별히 설계된 플랫폼
              </Text>
            </Box>
            <Box textAlign={{ base: 'center', md: 'left' }}>
              <Text fontSize="lg" color="brand.100" lineHeight="relaxed">
                카페, 음식점, 미용실, 소매업 등 다양한 업종의 특성을 이해하고, 
                한국 시장의 트렌드와 소비자 행동을 반영한 맞춤형 마케팅 솔루션을 제공합니다.
              </Text>
            </Box>
          </Grid>
        </Container>
      </Box>

      {/* About Section */}
      <Box py={{ base: '20', md: '32' }} bgGradient="linear(135deg, brand.400, purple.400, pink.300)">
        <Container maxW="container.xl" px={6} textAlign="center" color="white">
          <Heading as="h2" size={{ base: 'xl', md: '2xl' }} fontWeight="bold" mb={4}>
            우리는 뻗어납니다
          </Heading>
          <Text fontSize={{ base: 'xl', md: '2xl' }} mb={8} maxW="2xl" mx="auto">
            소상공인의 성공이 곧 우리의 성공입니다. 
            데이터와 AI 기술로 한국의 모든 소상공인이 번영할 수 있도록 돕겠습니다.
          </Text>
          <Button
            bg="white"
            color="brand.600"
            fontWeight="semibold"
            px={10}
            py={4}
            size="lg"
            fontSize="lg"
            _hover={{
              bg: 'gray.100',
              transform: 'translateY(-2px)',
            }}
            boxShadow="xl"
          >
            뻗어나와 함께하기
          </Button>
        </Container>
      </Box>

      {/* Footer */}
      <Box bg="gray.900" color="gray.400" py={12}>
        <Container maxW="container.xl" px={6}>
          <Flex
            direction={{ base: 'column', md: 'row' }}
            justify="space-between"
            align="center"
            textAlign={{ base: 'center', md: 'left' }}
          >
            <Text mb={{ base: 4, md: 0 }}>
              &copy; {new Date().getFullYear()} Group Ppeodeona. All rights reserve.
            </Text>
            <HStack spacing={6} justify="center">
              <Link href="#" _hover={{ color: 'white' }} transition="colors 0.2s">
                개인정보처리방침
              </Link>
              <Link href="#" _hover={{ color: 'white' }} transition="colors 0.2s">
                이용약관
              </Link>
              <Link href="#" _hover={{ color: 'white' }} transition="colors 0.2s">
                고객지원
              </Link>
            </HStack>
          </Flex>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage;

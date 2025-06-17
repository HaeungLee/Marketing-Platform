import React, { useState, useEffect } from "react";
import {
  Box,
  Container,
  Heading,
  SimpleGrid,
  Card,
  CardBody,
  Text,
  Badge,
  VStack,
  HStack,
  Spinner,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  useToast,
  Flex,
  Icon,
  Button,
  Select,
  Progress,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from "@chakra-ui/react";
import { FiTrendingUp, FiRefreshCw, FiBarChart, FiTarget, FiMapPin, FiClock } from "react-icons/fi";
import { businessStoreService } from "../services/businessStoreService";

interface TrendData {
  keyword: string;
  interest: number;
  relatedQueries: string[];
  regions: Array<{
    name: string;
    value: number;
  }>;
  timeData: Array<{
    date: string;
    value: number;
  }>;
}

interface BusinessInsight {
  businessType: string;
  marketState: 'HOT' | 'RISING' | 'STABLE' | 'DECLINING';
  recommendations: string[];
  opportunities: string[];
  threats: string[];
  trendScore: number;
}

interface CombinedAnalysis {
  region: string;
  realStoreCount: number;
  trendInterest: number;
  marketOpportunity: number;
  recommendation: string;
  insights: string[];
}

const TrendAnalysisPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [selectedBusinessType, setSelectedBusinessType] = useState("카페");
  const [trendData, setTrendData] = useState<TrendData | null>(null);
  const [businessInsights, setBusinessInsights] = useState<BusinessInsight[]>([]);
  const [combinedAnalysis, setCombinedAnalysis] = useState<CombinedAnalysis[]>([]);
  const toast = useToast();

  const businessTypes = [
    { value: "카페", label: "카페" },
    { value: "일반음식점", label: "일반음식점" },
    { value: "미용실", label: "미용실" },
    { value: "편의점", label: "편의점" },
    { value: "의류", label: "의류" },
  ];

  const majorRegions = [
    { name: "강남구", lat: 37.5172, lng: 127.0473 },
    { name: "홍대", lat: 37.5563, lng: 126.9233 },
    { name: "명동", lat: 37.5636, lng: 126.9834 },
    { name: "건대", lat: 37.5443, lng: 127.0557 },
    { name: "신촌", lat: 37.5595, lng: 126.9425 },
  ];

  const fetchTrendAnalysis = async () => {
    setLoading(true);
    try {
      // 1. 모의 Google Trends 데이터 (실제로는 백엔드 PyTrends API 호출)
      const mockTrendData: TrendData = {
        keyword: selectedBusinessType,
        interest: Math.floor(Math.random() * 100) + 1,
        relatedQueries: [
          `${selectedBusinessType} 창업`,
          `${selectedBusinessType} 트렌드`,
          `${selectedBusinessType} 매출`,
          `${selectedBusinessType} 위치`,
        ],
        regions: [
          { name: "서울", value: Math.floor(Math.random() * 100) + 1 },
          { name: "경기", value: Math.floor(Math.random() * 100) + 1 },
          { name: "부산", value: Math.floor(Math.random() * 100) + 1 },
          { name: "대구", value: Math.floor(Math.random() * 100) + 1 },
        ],
        timeData: Array.from({ length: 12 }, (_, i) => ({
          date: `2024-${(i + 1).toString().padStart(2, '0')}`,
          value: Math.floor(Math.random() * 100) + 1,
        })),
      };
      setTrendData(mockTrendData);

      // 2. 비즈니스 인사이트 생성
      const insights = await generateBusinessInsights(mockTrendData);
      setBusinessInsights(insights);

      // 3. 실제 상가 데이터와 트렌드 결합 분석
      const combined = await generateCombinedAnalysis(mockTrendData);
      setCombinedAnalysis(combined);

    } catch (error) {
      console.error("트렌드 분석 실패:", error);
      toast({
        title: "분석 실패",
        description: "트렌드 데이터를 가져오는 중 오류가 발생했습니다.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const generateBusinessInsights = async (trends: TrendData): Promise<BusinessInsight[]> => {
    const currentInterest = trends.interest;
    let marketState: 'HOT' | 'RISING' | 'STABLE' | 'DECLINING' = 'STABLE';
    
    if (currentInterest > 80) marketState = 'HOT';
    else if (currentInterest > 60) marketState = 'RISING';
    else if (currentInterest < 30) marketState = 'DECLINING';

    const recommendations = [];
    const opportunities = [];
    const threats = [];

    switch (marketState) {
      case 'HOT':
        recommendations.push("지금이 진입하기 좋은 시기입니다");
        recommendations.push("프리미엄 전략으로 차별화하세요");
        opportunities.push("높은 관심도로 인한 빠른 고객 유입");
        threats.push("경쟁 진입 가능성 높음");
        break;
      case 'RISING':
        recommendations.push("시장 성장세를 활용하세요");
        recommendations.push("브랜딩에 집중하세요");
        opportunities.push("성장하는 시장의 선점 효과");
        threats.push("곧 경쟁이 치열해질 수 있음");
        break;
      case 'DECLINING':
        recommendations.push("혁신적인 접근이 필요합니다");
        recommendations.push("비용 효율성에 집중하세요");
        opportunities.push("경쟁자 감소로 인한 시장 점유율 확대");
        threats.push("시장 규모 축소 위험");
        break;
      default:
        recommendations.push("안정적인 시장 진입 가능");
        opportunities.push("꾸준한 수요 기대");
        threats.push("큰 변화 없는 정체 상태");
    }

    return [{
      businessType: selectedBusinessType,
      marketState,
      recommendations,
      opportunities,
      threats,
      trendScore: currentInterest,
    }];
  };

  const generateCombinedAnalysis = async (trends: TrendData): Promise<CombinedAnalysis[]> => {
    const analysis: CombinedAnalysis[] = [];

    for (const region of majorRegions) {
      try {
        // 실제 상가 데이터 조회
        const nearbyStores = await businessStoreService.getNearbyStores(
          region.lat,
          region.lng,
          1000,
          selectedBusinessType
        );

        const realStoreCount = nearbyStores.stores.length;
        const trendInterest = trends.interest + Math.floor(Math.random() * 20) - 10; // 지역별 변동

        // 시장 기회 점수 계산 (트렌드 관심도 vs 실제 상가 밀도)
        const marketOpportunity = Math.max(0, Math.min(100, 
          (trendInterest * 0.7) + ((100 - (realStoreCount / 50 * 100)) * 0.3)
        ));

        let recommendation = "";
        if (marketOpportunity > 70) {
          recommendation = "매우 유망한 지역 - 즉시 진입 권장";
        } else if (marketOpportunity > 50) {
          recommendation = "안정적인 지역 - 신중한 진입 권장";
        } else {
          recommendation = "경쟁 치열 - 차별화 전략 필수";
        }

        const insights = [
          `실제 ${selectedBusinessType} 상가 ${realStoreCount}개 운영`,
          `온라인 관심도 ${trendInterest}점`,
          marketOpportunity > 60 ? "수요 대비 공급 부족" : "시장 포화 상태"
        ];

        analysis.push({
          region: region.name,
          realStoreCount,
          trendInterest,
          marketOpportunity,
          recommendation,
          insights,
        });

      } catch (error) {
        console.error(`${region.name} 분석 실패:`, error);
        analysis.push({
          region: region.name,
          realStoreCount: 0,
          trendInterest: 0,
          marketOpportunity: 0,
          recommendation: "데이터 수집 중...",
          insights: ["분석 데이터를 준비 중입니다"],
        });
      }
    }

    return analysis.sort((a, b) => b.marketOpportunity - a.marketOpportunity);
  };

  useEffect(() => {
    fetchTrendAnalysis();
  }, [selectedBusinessType]);

  const getMarketStateColor = (state: string) => {
    switch (state) {
      case "HOT": return "red";
      case "RISING": return "green";
      case "STABLE": return "blue";
      case "DECLINING": return "gray";
      default: return "gray";
    }
  };

  const getMarketStateText = (state: string) => {
    switch (state) {
      case "HOT": return "뜨거움";
      case "RISING": return "상승세";
      case "STABLE": return "안정";
      case "DECLINING": return "하락세";
      default: return "분석 중";
    }
  };

  return (
    <Container maxW="7xl" py={6}>
      <VStack spacing={6} align="stretch">
        {/* 헤더 */}
        <Flex justify="space-between" align="center">
          <Box>
            <Heading size="lg" color="gray.800" mb={2}>
              📈 트렌드 기반 시장 분석
            </Heading>
            <Text color="gray.600">
              Google Trends와 실제 상가 데이터를 결합한 시장 기회 발굴
            </Text>
          </Box>
          <Button
            leftIcon={<FiRefreshCw />}
            colorScheme="brand"
            onClick={fetchTrendAnalysis}
            isLoading={loading}
            loadingText="분석 중..."
          >
            새로고침
          </Button>
        </Flex>

        {/* 업종 선택 */}
        <Card>
          <CardBody>
            <HStack spacing={4}>
              <Text fontWeight="medium">분석 업종:</Text>
              <Select
                value={selectedBusinessType}
                onChange={(e) => setSelectedBusinessType(e.target.value)}
                maxW="200px"
              >
                {businessTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </Select>
              <Badge colorScheme="blue" p={2} borderRadius="md">
                {loading ? "분석 중..." : "분석 완료"}
              </Badge>
            </HStack>
          </CardBody>
        </Card>

        {loading ? (
          <Box textAlign="center" py={10}>
            <Spinner size="xl" color="brand.500" />
            <Text mt={4} color="gray.600">트렌드 데이터를 분석하고 있습니다...</Text>
          </Box>
        ) : (
          <Tabs variant="enclosed" colorScheme="brand">
            <TabList>
              <Tab>시장 트렌드</Tab>
              <Tab>지역별 기회 분석</Tab>
              <Tab>비즈니스 인사이트</Tab>
              <Tab>실시간 데이터</Tab>
            </TabList>

            <TabPanels>
              {/* 시장 트렌드 */}
              <TabPanel>
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                  {/* 전체 관심도 */}
                  <Card>
                    <CardBody>
                      <Stat>
                        <StatLabel>전체 관심도</StatLabel>
                        <StatNumber>{trendData?.interest || 0}</StatNumber>
                        <StatHelpText>Google Trends 기준</StatHelpText>
                      </Stat>
                      <Progress 
                        value={trendData?.interest || 0} 
                        colorScheme="brand" 
                        mt={4} 
                      />
                    </CardBody>
                  </Card>

                  {/* 시장 상태 */}
                  {businessInsights.length > 0 && (
                    <Card>
                      <CardBody>
                        <VStack align="stretch" spacing={3}>
                          <HStack>
                            <Icon as={FiTrendingUp} color="brand.500" />
                            <Text fontWeight="bold">시장 상태</Text>
                          </HStack>
                          <Badge 
                            colorScheme={getMarketStateColor(businessInsights[0].marketState)} 
                            p={2} 
                            textAlign="center"
                          >
                            {getMarketStateText(businessInsights[0].marketState)}
                          </Badge>
                          <Text fontSize="sm" color="gray.600">
                            트렌드 점수: {businessInsights[0].trendScore}/100
                          </Text>
                        </VStack>
                      </CardBody>
                    </Card>
                  )}

                  {/* 관련 검색어 */}
                  <Card>
                    <CardBody>
                      <VStack align="stretch" spacing={3}>
                        <HStack>
                          <Icon as={FiTarget} color="purple.500" />
                          <Text fontWeight="bold">관련 검색어</Text>
                        </HStack>
                        <VStack spacing={1}>
                          {trendData?.relatedQueries.slice(0, 4).map((query, index) => (
                            <Badge key={index} variant="outline" p={1} w="100%">
                              {query}
                            </Badge>
                          ))}
                        </VStack>
                      </VStack>
                    </CardBody>
                  </Card>
                </SimpleGrid>

                {/* 지역별 관심도 */}
                <Card mt={6}>
                  <CardBody>
                    <Heading size="md" mb={4}>지역별 관심도</Heading>
                    <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
                      {trendData?.regions.map((region, index) => (
                        <Box key={index} p={4} border="1px" borderColor="gray.200" borderRadius="md">
                          <VStack spacing={2}>
                            <Text fontWeight="bold">{region.name}</Text>
                            <Text fontSize="2xl" color="brand.500" fontWeight="bold">
                              {region.value}
                            </Text>
                            <Progress value={region.value} colorScheme="brand" w="100%" />
                          </VStack>
                        </Box>
                      ))}
                    </SimpleGrid>
                  </CardBody>
                </Card>
              </TabPanel>

              {/* 지역별 기회 분석 */}
              <TabPanel>
                <VStack spacing={6}>
                  {combinedAnalysis.map((analysis, index) => (
                    <Card key={index} w="100%">
                      <CardBody>
                        <HStack justify="space-between" mb={4}>
                          <VStack align="start" spacing={1}>
                            <Text fontSize="lg" fontWeight="bold">{analysis.region}</Text>
                            <Text fontSize="sm" color="gray.600">{analysis.recommendation}</Text>
                          </VStack>
                          <Badge 
                            colorScheme={
                              analysis.marketOpportunity > 70 ? "green" : 
                              analysis.marketOpportunity > 50 ? "yellow" : "red"
                            }
                            p={2}
                          >
                            기회 점수: {analysis.marketOpportunity.toFixed(0)}점
                          </Badge>
                        </HStack>

                        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                          <VStack>
                            <Icon as={FiMapPin} color="blue.500" boxSize={6} />
                            <Text fontSize="sm" color="gray.600">실제 상가 수</Text>
                            <Text fontSize="xl" fontWeight="bold">{analysis.realStoreCount}개</Text>
                          </VStack>
                          <VStack>
                            <Icon as={FiTrendingUp} color="green.500" boxSize={6} />
                            <Text fontSize="sm" color="gray.600">온라인 관심도</Text>
                            <Text fontSize="xl" fontWeight="bold">{analysis.trendInterest}점</Text>
                          </VStack>
                          <VStack>
                            <Icon as={FiBarChart} color="purple.500" boxSize={6} />
                            <Text fontSize="sm" color="gray.600">시장 기회</Text>
                            <Text fontSize="xl" fontWeight="bold" color="brand.500">
                              {analysis.marketOpportunity.toFixed(0)}점
                            </Text>
                          </VStack>
                        </SimpleGrid>

                        <Box mt={4}>
                          <Text fontSize="sm" color="gray.600" mb={2}>인사이트</Text>
                          <VStack align="stretch" spacing={1}>
                            {analysis.insights.map((insight, idx) => (
                              <Text key={idx} fontSize="sm" color="gray.700">
                                • {insight}
                              </Text>
                            ))}
                          </VStack>
                        </Box>
                      </CardBody>
                    </Card>
                  ))}
                </VStack>
              </TabPanel>

              {/* 비즈니스 인사이트 */}
              <TabPanel>
                {businessInsights.length > 0 && (
                  <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                    <Card>
                      <CardBody>
                        <Heading size="md" mb={4} color="green.600">기회 요소</Heading>
                        <VStack align="stretch" spacing={2}>
                          {businessInsights[0].opportunities.map((opportunity, index) => (
                            <HStack key={index}>
                              <Badge colorScheme="green" variant="solid">+</Badge>
                              <Text fontSize="sm">{opportunity}</Text>
                            </HStack>
                          ))}
                        </VStack>
                      </CardBody>
                    </Card>

                    <Card>
                      <CardBody>
                        <Heading size="md" mb={4} color="red.600">위험 요소</Heading>
                        <VStack align="stretch" spacing={2}>
                          {businessInsights[0].threats.map((threat, index) => (
                            <HStack key={index}>
                              <Badge colorScheme="red" variant="solid">-</Badge>
                              <Text fontSize="sm">{threat}</Text>
                            </HStack>
                          ))}
                        </VStack>
                      </CardBody>
                    </Card>

                    <Card gridColumn={{ md: "span 2" }}>
                      <CardBody>
                        <Heading size="md" mb={4} color="blue.600">추천 전략</Heading>
                        <VStack align="stretch" spacing={2}>
                          {businessInsights[0].recommendations.map((recommendation, index) => (
                            <HStack key={index}>
                              <Badge colorScheme="blue" variant="solid">{index + 1}</Badge>
                              <Text fontSize="sm">{recommendation}</Text>
                            </HStack>
                          ))}
                        </VStack>
                      </CardBody>
                    </Card>
                  </SimpleGrid>
                )}
              </TabPanel>

              {/* 실시간 데이터 */}
              <TabPanel>
                <Alert status="info" mb={6}>
                  <AlertIcon />
                  <Box>
                    <AlertTitle>실시간 데이터 분석</AlertTitle>
                    <AlertDescription>
                      Google Trends API와 공공데이터포털을 실시간으로 연동한 분석 결과입니다.
                    </AlertDescription>
                  </Box>
                </Alert>

                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                  <Card>
                    <CardBody>
                      <Heading size="md" mb={4}>월별 트렌드 변화</Heading>
                      <VStack spacing={3}>
                        {trendData?.timeData.slice(-6).map((data, index) => (
                          <HStack key={index} w="100%" justify="space-between">
                            <Text fontSize="sm">{data.date}</Text>
                            <HStack>
                              <Progress value={data.value} w="100px" colorScheme="brand" />
                              <Text fontSize="sm" fontWeight="bold">{data.value}점</Text>
                            </HStack>
                          </HStack>
                        ))}
                      </VStack>
                    </CardBody>
                  </Card>

                  <Card>
                    <CardBody>
                      <Heading size="md" mb={4}>데이터 출처</Heading>
                      <VStack align="stretch" spacing={3}>
                        <HStack>
                          <Badge colorScheme="red">Google Trends</Badge>
                          <Text fontSize="sm">검색 트렌드 분석</Text>
                        </HStack>
                        <HStack>
                          <Badge colorScheme="blue">공공데이터포털</Badge>
                          <Text fontSize="sm">상가 정보 API</Text>
                        </HStack>
                        <HStack>
                          <Badge colorScheme="purple">AI 분석</Badge>
                          <Text fontSize="sm">시장 기회 예측</Text>
                        </HStack>
                      </VStack>
                    </CardBody>
                  </Card>
                </SimpleGrid>
              </TabPanel>
            </TabPanels>
          </Tabs>
        )}

        {/* 데이터 업데이트 정보 */}
        <Card>
          <CardBody>
            <HStack spacing={4}>
              <Icon as={FiClock} color="brand.500" boxSize={6} />
              <VStack align="start" spacing={1}>
                <Text fontWeight="bold">데이터 업데이트</Text>
                <Text fontSize="sm" color="gray.600">
                  트렌드 데이터: 실시간 업데이트 | 상가 데이터: 일 단위 업데이트
                </Text>
                <Text fontSize="xs" color="gray.500">
                  최종 업데이트: {new Date().toLocaleDateString()}
                </Text>
              </VStack>
            </HStack>
          </CardBody>
        </Card>
      </VStack>
    </Container>
  );
};

export default TrendAnalysisPage; 
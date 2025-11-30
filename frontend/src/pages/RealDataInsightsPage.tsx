import React, { useState } from 'react';
import {
  Box,
  VStack,
  HStack,
  Card,
  CardBody,
  CardHeader,
  Button,
  Input,
  Select,
  Text,
  Badge,
  Grid,
  GridItem,
  Alert,
  AlertIcon,
  Divider,
  useColorModeValue,
  useToast,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { FaUsers, FaMapMarkerAlt, FaClock, FaChartLine, FaLightbulb } from 'react-icons/fa';

interface TargetCustomerData {
  primaryTarget: string;
  secondaryTarget: string;
  strategy: string[];
  confidence: number;
  dataSource: string;
  regionAnalysis?: {
    totalPopulation: number;
    ageDistribution: Record<string, number>;
  };
}

interface LocationRecommendation {
  recommendedAreas: Array<{
    area: string;
    expectedROI: string;
    population: number;
    score: number;
  }>;
  analysisMetadata: {
    totalLocationsAnalyzed: number;
    floatingPopulationSites: number;
    budgetRange: string;
    analysisDate: string;
  };
  reasons: string[];
}

interface MarketingTimingData {
  bestDays: string[];
  bestHours: string[];
  seasonalTrends: string;
  confidence: number;
  dataSource: string;
  detailedAnalysis?: {
    dayPatterns: Record<string, number>;
    hourPatterns: Record<string, number>;
    totalTransactions: number;
  };
}

const RealDataInsightsPage: React.FC = () => {
  const [businessType, setBusinessType] = useState('카페');
  const [region, setRegion] = useState('강남구');
  const [budget, setBudget] = useState('50000000');
  const [targetAge, setTargetAge] = useState('30대');
  const [loading, setLoading] = useState(false);
  
  const [targetCustomerData, setTargetCustomerData] = useState<TargetCustomerData | null>(null);
  const [locationData, setLocationData] = useState<LocationRecommendation | null>(null);
  const [timingData, setTimingData] = useState<MarketingTimingData | null>(null);
  
  const toast = useToast();
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  const businessTypes = ['카페', '음식점', '미용실', '편의점', '의류', '화장품', '서점', '헬스장'];
  const regions = ['강남구', '서초구', '송파구', '홍대', '신촌', '이태원', '명동', '종로구', '마포구'];
  const targetAges = ['20대', '30대', '40대', '50대', '60대'];

  // 타겟 고객 분석 API 호출
  const fetchTargetCustomerAnalysis = async () => {
    try {
      const response = await fetch(
        `/api/v1/insights/target-customer?business_type=${businessType}&region=${region}`
      );
      if (response.ok) {
        const data = await response.json();
        setTargetCustomerData(data);
      } else {
        throw new Error('API 호출 실패');
      }
    } catch (error) {
      console.error('타겟 고객 분석 오류:', error);
      toast({
        title: '데이터 로딩 실패',
        description: '타겟 고객 분석 데이터를 불러올 수 없습니다.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  // 입지 추천 API 호출
  const fetchLocationRecommendation = async () => {
    try {
      const response = await fetch(
        `/api/v1/insights/optimal-location?business_type=${businessType}&budget=${budget}&target_age=${targetAge}`
      );
      if (response.ok) {
        const data = await response.json();
        setLocationData(data);
      } else {
        throw new Error('API 호출 실패');
      }
    } catch (error) {
      console.error('입지 추천 오류:', error);
      toast({
        title: '데이터 로딩 실패',
        description: '입지 추천 데이터를 불러올 수 없습니다.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  // 마케팅 타이밍 API 호출
  const fetchMarketingTiming = async () => {
    try {
      const response = await fetch(
        `/api/v1/insights/marketing-timing?target_age=${targetAge}&business_type=${businessType}`
      );
      if (response.ok) {
        const data = await response.json();
        setTimingData(data);
      } else {
        throw new Error('API 호출 실패');
      }
    } catch (error) {
      console.error('마케팅 타이밍 오류:', error);
      toast({
        title: '데이터 로딩 실패',
        description: '마케팅 타이밍 데이터를 불러올 수 없습니다.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  // 종합 분석 실행
  const runComprehensiveAnalysis = async () => {
    setLoading(true);
    try {
      await Promise.all([
        fetchTargetCustomerAnalysis(),
        fetchLocationRecommendation(),
        fetchMarketingTiming()
      ]);
      
      toast({
        title: '분석 완료',
        description: '실제 데이터 기반 비즈니스 인사이트가 생성되었습니다.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('종합 분석 오류:', error);
    } finally {
      setLoading(false);
    }
  };

  // 연령대별 분포 차트 데이터
  const getAgeDistributionData = () => {
    if (!targetCustomerData?.regionAnalysis?.ageDistribution) return [];
    
    const distribution = targetCustomerData.regionAnalysis.ageDistribution;
    return Object.entries(distribution).map(([age, count]) => ({
      age,
      count,
      percentage: ((count / targetCustomerData.regionAnalysis!.totalPopulation) * 100).toFixed(1)
    }));
  };

  // 입지별 ROI 차트 데이터  
  const getLocationROIData = () => {
    if (!locationData?.recommendedAreas) return [];
    
    return locationData.recommendedAreas.map(area => ({
      area: area.area.split(' ')[1] || area.area, // 구 이름만 표시
      roi: parseFloat(area.expectedROI.replace('%', '')),
      population: area.population
    }));
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  return (
    <Box p={6} maxW="1400px" mx="auto">
      <VStack spacing={6} align="stretch">
        {/* 헤더 */}
        <Box>
          <Text fontSize="2xl" fontWeight="bold" mb={2}>
            🎯 실제 데이터 기반 비즈니스 인사이트
          </Text>
          <Text color="gray.600">
            공공데이터와 실제 소비패턴을 분석하여 맞춤형 비즈니스 전략을 제공합니다
          </Text>
        </Box>

        {/* 분석 설정 패널 */}
        <Card bg={cardBg} borderWidth="1px" borderColor={borderColor}>
          <CardHeader>
            <Text fontSize="lg" fontWeight="semibold">분석 설정</Text>
          </CardHeader>
          <CardBody>
            <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={4}>
              <GridItem>
                <Text mb={2} fontSize="sm" fontWeight="medium">업종</Text>
                <Select value={businessType} onChange={(e) => setBusinessType(e.target.value)}>
                  {businessTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </Select>
              </GridItem>
              
              <GridItem>
                <Text mb={2} fontSize="sm" fontWeight="medium">지역</Text>
                <Select value={region} onChange={(e) => setRegion(e.target.value)}>
                  {regions.map(r => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </Select>
              </GridItem>
              
              <GridItem>
                <Text mb={2} fontSize="sm" fontWeight="medium">예산 (원)</Text>
                <Input 
                  value={budget} 
                  onChange={(e) => setBudget(e.target.value)}
                  placeholder="예: 50000000"
                />
              </GridItem>
              
              <GridItem>
                <Text mb={2} fontSize="sm" fontWeight="medium">타겟 연령대</Text>
                <Select value={targetAge} onChange={(e) => setTargetAge(e.target.value)}>
                  {targetAges.map(age => (
                    <option key={age} value={age}>{age}</option>
                  ))}
                </Select>
              </GridItem>
            </Grid>
            
            <Button 
              mt={4} 
              colorScheme="blue" 
              onClick={runComprehensiveAnalysis}
              isLoading={loading}
              loadingText="분석 중..."
              leftIcon={<FaChartLine />}
            >
              실제 데이터 분석 실행
            </Button>
          </CardBody>
        </Card>

        {/* 분석 결과 탭 */}
        <Tabs variant="enclosed" colorScheme="blue">
          <TabList>
            <Tab>
              <HStack>
                <FaUsers />
                <Text>타겟 고객 분석</Text>
              </HStack>
            </Tab>
            <Tab>
              <HStack>
                <FaMapMarkerAlt />
                <Text>최적 입지 추천</Text>
              </HStack>
            </Tab>
            <Tab>
              <HStack>
                <FaClock />
                <Text>마케팅 타이밍</Text>
              </HStack>
            </Tab>
          </TabList>

          <TabPanels>
            {/* 타겟 고객 분석 탭 */}
            <TabPanel>
              {targetCustomerData ? (
                <Grid templateColumns="repeat(auto-fit, minmax(300px, 1fr))" gap={6}>
                  <GridItem>
                    <Card>
                      <CardHeader>
                        <Text fontSize="lg" fontWeight="semibold">타겟 고객 분석 결과</Text>
                        <Badge colorScheme="green" ml={2}>
                          신뢰도 {targetCustomerData.confidence}%
                        </Badge>
                      </CardHeader>
                      <CardBody>
                        <VStack align="stretch" spacing={4}>
                          <Box>
                            <Text fontSize="sm" color="gray.600">주요 타겟</Text>
                            <Text fontSize="xl" fontWeight="bold" color="blue.500">
                              {targetCustomerData.primaryTarget}
                            </Text>
                          </Box>
                          
                          <Box>
                            <Text fontSize="sm" color="gray.600">보조 타겟</Text>
                            <Text fontSize="lg" fontWeight="semibold">
                              {targetCustomerData.secondaryTarget}
                            </Text>
                          </Box>
                          
                          <Divider />
                          
                          <Box>
                            <Text fontSize="sm" color="gray.600" mb={2}>추천 전략</Text>
                            <VStack align="stretch" spacing={2}>
                              {targetCustomerData.strategy.map((strategy, index) => (
                                <HStack key={index}>
                                  <FaLightbulb color="orange" />
                                  <Text fontSize="sm">{strategy}</Text>
                                </HStack>
                              ))}
                            </VStack>
                          </Box>
                          
                          <Box>
                            <Text fontSize="xs" color="gray.500">
                              데이터 출처: {targetCustomerData.dataSource}
                            </Text>
                          </Box>
                        </VStack>
                      </CardBody>
                    </Card>
                  </GridItem>

                  {/* 연령대별 분포 차트 */}
                  <GridItem>
                    <Card>
                      <CardHeader>
                        <Text fontSize="lg" fontWeight="semibold">지역 연령대 분포</Text>
                      </CardHeader>
                      <CardBody>
                        <Box h="300px">
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={getAgeDistributionData()}>
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="age" />
                              <YAxis />
                              <Tooltip 
                                formatter={(value, name) => [
                                  `${value}명 (${name === 'count' ? '인구수' : name})`, 
                                  ''
                                ]}
                              />
                              <Bar dataKey="count" fill="#3182CE" />
                            </BarChart>
                          </ResponsiveContainer>
                        </Box>
                      </CardBody>
                    </Card>
                  </GridItem>
                </Grid>
              ) : (
                <Alert status="info">
                  <AlertIcon />
                  분석을 실행하면 실제 인구통계 데이터 기반 타겟 고객 분석 결과가 표시됩니다.
                </Alert>
              )}
            </TabPanel>

            {/* 최적 입지 추천 탭 */}
            <TabPanel>
              {locationData ? (
                <Grid templateColumns="repeat(auto-fit, minmax(300px, 1fr))" gap={6}>
                  <GridItem>
                    <Card>
                      <CardHeader>
                        <Text fontSize="lg" fontWeight="semibold">추천 입지 순위</Text>
                      </CardHeader>
                      <CardBody>
                        <VStack align="stretch" spacing={3}>
                          {locationData.recommendedAreas.map((area, index) => (
                            <Box 
                              key={index} 
                              p={3} 
                              borderWidth="1px" 
                              borderRadius="md"
                              bg={index === 0 ? 'blue.50' : 'gray.50'}
                            >
                              <HStack justify="space-between">
                                <VStack align="start" spacing={1}>
                                  <HStack>
                                    <Badge colorScheme="blue">{index + 1}위</Badge>
                                    <Text fontWeight="semibold">{area.area}</Text>
                                  </HStack>
                                  <Text fontSize="sm" color="gray.600">
                                    인구: {area.population.toLocaleString()}명
                                  </Text>
                                </VStack>
                                <VStack align="end" spacing={1}>
                                  <Text fontSize="lg" fontWeight="bold" color="green.500">
                                    {area.expectedROI}
                                  </Text>
                                  <Text fontSize="xs" color="gray.500">예상 ROI</Text>
                                </VStack>
                              </HStack>
                            </Box>
                          ))}
                        </VStack>
                        
                        <Divider my={4} />
                        
                        <Box>
                          <Text fontSize="sm" fontWeight="semibold" mb={2}>선정 기준</Text>
                          <VStack align="stretch" spacing={1}>
                            {locationData.reasons.map((reason, index) => (
                              <Text key={index} fontSize="sm" color="gray.600">
                                • {reason}
                              </Text>
                            ))}
                          </VStack>
                        </Box>
                      </CardBody>
                    </Card>
                  </GridItem>

                  {/* ROI 차트 */}
                  <GridItem>
                    <Card>
                      <CardHeader>
                        <Text fontSize="lg" fontWeight="semibold">입지별 예상 ROI</Text>
                      </CardHeader>
                      <CardBody>
                        <Box h="300px">
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={getLocationROIData()}>
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="area" />
                              <YAxis />
                              <Tooltip 
                                formatter={(value) => [`${value}%`, 'ROI']}
                              />
                              <Bar dataKey="roi" fill="#38A169" />
                            </BarChart>
                          </ResponsiveContainer>
                        </Box>
                      </CardBody>
                    </Card>
                  </GridItem>
                </Grid>
              ) : (
                <Alert status="info">
                  <AlertIcon />
                  분석을 실행하면 실제 유동인구와 상권 데이터 기반 최적 입지 추천이 표시됩니다.
                </Alert>
              )}
            </TabPanel>

            {/* 마케팅 타이밍 탭 */}
            <TabPanel>
              {timingData ? (
                <Grid templateColumns="repeat(auto-fit, minmax(300px, 1fr))" gap={6}>
                  <GridItem>
                    <Card>
                      <CardHeader>
                        <Text fontSize="lg" fontWeight="semibold">최적 마케팅 타이밍</Text>
                        <Badge colorScheme="green" ml={2}>
                          신뢰도 {timingData.confidence}%
                        </Badge>
                      </CardHeader>
                      <CardBody>
                        <VStack align="stretch" spacing={4}>
                          <Box>
                            <Text fontSize="sm" color="gray.600" mb={2}>추천 요일</Text>
                            <HStack>
                              {timingData.bestDays.map((day, index) => (
                                <Badge key={index} colorScheme="blue" variant="solid">
                                  {day}
                                </Badge>
                              ))}
                            </HStack>
                          </Box>
                          
                          <Box>
                            <Text fontSize="sm" color="gray.600" mb={2}>추천 시간대</Text>
                            <VStack align="stretch" spacing={1}>
                              {timingData.bestHours.map((hour, index) => (
                                <Badge key={index} colorScheme="green" variant="outline">
                                  {hour}
                                </Badge>
                              ))}
                            </VStack>
                          </Box>
                          
                          <Divider />
                          
                          <Box>
                            <Text fontSize="sm" color="gray.600">계절 트렌드</Text>
                            <Text fontSize="md" fontWeight="medium">
                              {timingData.seasonalTrends}
                            </Text>
                          </Box>
                          
                          <Box>
                            <Text fontSize="xs" color="gray.500">
                              데이터 출처: {timingData.dataSource}
                            </Text>
                          </Box>
                        </VStack>
                      </CardBody>
                    </Card>
                  </GridItem>

                  {/* 시간대별 패턴 차트 (있을 경우) */}
                  {timingData.detailedAnalysis && (
                    <GridItem>
                      <Card>
                        <CardHeader>
                          <Text fontSize="lg" fontWeight="semibold">시간대별 거래 패턴</Text>
                        </CardHeader>
                        <CardBody>
                          <Box h="300px">
                            <ResponsiveContainer width="100%" height="100%">
                              <PieChart>
                                <Pie
                                  data={Object.entries(timingData.detailedAnalysis.hourPatterns).map(([hour, count]) => ({
                                    hour: `${hour}시`,
                                    count
                                  }))}
                                  cx="50%"
                                  cy="50%"
                                  labelLine={false}
                                  label={({ hour, percent }) => `${hour} ${(percent * 100).toFixed(0)}%`}
                                  outerRadius={80}
                                  fill="#8884d8"
                                  dataKey="count"
                                >
                                  {Object.entries(timingData.detailedAnalysis.hourPatterns).map((_, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                  ))}
                                </Pie>
                                <Tooltip />
                              </PieChart>
                            </ResponsiveContainer>
                          </Box>
                        </CardBody>
                      </Card>
                    </GridItem>
                  )}
                </Grid>
              ) : (
                <Alert status="info">
                  <AlertIcon />
                  분석을 실행하면 실제 카드 소비 패턴 기반 최적 마케팅 타이밍이 표시됩니다.
                </Alert>
              )}
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Box>
  );
};

export default RealDataInsightsPage;

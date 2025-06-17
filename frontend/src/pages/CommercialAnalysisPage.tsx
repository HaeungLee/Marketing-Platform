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
  Button,
  Select,
  Input,
  InputGroup,
  InputLeftElement,
} from "@chakra-ui/react";
import { FiMapPin, FiTrendingUp, FiUsers, FiDollarSign, FiBarChart, FiRefreshCw, FiSearch } from "react-icons/fi";
import { businessStoreService } from "../services/businessStoreService";
import type { BusinessStore, NearbyStoresResponse, BusinessStatistics } from "../services/businessStoreService";

interface RegionAnalysis {
  region: string;
  totalStores: number;
  businessTypes: { [key: string]: number };
  competitionLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  averageDistance: number;
  trends: string[];
}

interface LocationCoordinates {
  lat: number;
  lng: number;
  name: string;
}

const POPULAR_LOCATIONS: LocationCoordinates[] = [
  { lat: 37.5665, lng: 126.9780, name: "서울역" },
  { lat: 37.5662, lng: 126.9784, name: "명동" },
  { lat: 37.4979, lng: 127.0276, name: "강남역" },
  { lat: 37.5563, lng: 126.9233, name: "홍대입구" },
  { lat: 37.5443, lng: 127.0557, name: "건대입구" },
];

const CommercialAnalysisPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [nearbyStores, setNearbyStores] = useState<BusinessStore[]>([]);
  const [statistics, setStatistics] = useState<BusinessStatistics | null>(null);
  const [regionAnalysis, setRegionAnalysis] = useState<RegionAnalysis[]>([]);
  const [selectedLocation, setSelectedLocation] = useState<LocationCoordinates>(POPULAR_LOCATIONS[2]); // 강남역
  const [businessType, setBusinessType] = useState("");
  const [radius, setRadius] = useState(1000);
  const toast = useToast();

  const fetchCommercialData = async () => {
    setLoading(true);
    try {
      // 1. 주변 상가 조회
      const nearbyResponse = await businessStoreService.getNearbyStores(
        selectedLocation.lat,
        selectedLocation.lng,
        radius,
        businessType || undefined
      );
      setNearbyStores(nearbyResponse.stores);

      // 2. 통계 데이터 조회
      const statsResponse = await businessStoreService.getBusinessStatistics(
        undefined, // sido
        undefined  // sigungu
      );
      setStatistics(statsResponse);

      // 3. 지역 분석 데이터 생성
      const analysis = await generateRegionAnalysis(nearbyResponse);
      setRegionAnalysis(analysis);

    } catch (error) {
      console.error("상권 분석 데이터 로딩 실패:", error);
      toast({
        title: "데이터 로딩 실패",
        description: "상권 분석 데이터를 가져오는 중 오류가 발생했습니다. 서버가 실행 중인지 확인해주세요.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const generateRegionAnalysis = async (nearbyData: NearbyStoresResponse): Promise<RegionAnalysis[]> => {
    const stores = nearbyData.stores;
    
    // 지역별로 그룹화
    const regionGroups: { [key: string]: BusinessStore[] } = {};
    stores.forEach(store => {
      const region = `${store.sido_name} ${store.sigungu_name}`;
      if (!regionGroups[region]) {
        regionGroups[region] = [];
      }
      regionGroups[region].push(store);
    });

    // 각 지역별 분석 생성
    return Object.entries(regionGroups).map(([region, storeList]) => {
      const businessTypes: { [key: string]: number } = {};
      let totalDistance = 0;

      storeList.forEach(store => {
        businessTypes[store.business_name] = (businessTypes[store.business_name] || 0) + 1;
        totalDistance += store.distance || 0;
      });

      const averageDistance = totalDistance / storeList.length;
      
      // 경쟁 수준 계산
      let competitionLevel: 'LOW' | 'MEDIUM' | 'HIGH' = 'LOW';
      if (storeList.length > 50) competitionLevel = 'HIGH';
      else if (storeList.length > 20) competitionLevel = 'MEDIUM';

      // 트렌드 키워드 생성
      const topBusinessTypes = Object.entries(businessTypes)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 3)
        .map(([type]) => type);

      return {
        region,
        totalStores: storeList.length,
        businessTypes,
        competitionLevel,
        averageDistance,
        trends: topBusinessTypes,
      };
    });
  };

  useEffect(() => {
    fetchCommercialData();
  }, [selectedLocation, businessType, radius]);

  const getCompetitionColor = (level: string) => {
    switch (level) {
      case "HIGH": return "red";
      case "MEDIUM": return "yellow";
      case "LOW": return "green";
      default: return "gray";
    }
  };

  const getCompetitionText = (level: string) => {
    switch (level) {
      case "HIGH": return "높음";
      case "MEDIUM": return "중간";
      case "LOW": return "낮음";
      default: return "알 수 없음";
    }
  };

  return (
    <Container maxW="7xl" py={6}>
      <VStack spacing={6} align="stretch">
        {/* 헤더 */}
        <Flex justify="space-between" align="center">
          <Box>
            <Heading size="lg" color="gray.800" mb={2}>
              🏢 실시간 상권 분석
            </Heading>
            <Text color="gray.600">
              공공데이터 기반 실제 상가 정보와 위치별 상권 특성 분석
            </Text>
          </Box>
          <Button
            leftIcon={<FiRefreshCw />}
            colorScheme="brand"
            onClick={fetchCommercialData}
            isLoading={loading}
            loadingText="분석 중..."
          >
            새로고침
          </Button>
        </Flex>

        {/* 분석 설정 패널 */}
        <Card>
          <CardBody>
            <SimpleGrid columns={{ base: 1, md: 4 }} spacing={4}>
              <Box>
                <Text fontWeight="medium" mb={2}>분석 지역</Text>
                <Select
                  value={selectedLocation.name}
                  onChange={(e) => {
                    const location = POPULAR_LOCATIONS.find(loc => loc.name === e.target.value);
                    if (location) setSelectedLocation(location);
                  }}
                >
                  {POPULAR_LOCATIONS.map(location => (
                    <option key={location.name} value={location.name}>
                      {location.name}
                    </option>
                  ))}
                </Select>
              </Box>
              <Box>
                <Text fontWeight="medium" mb={2}>업종 필터</Text>
                <Select
                  value={businessType}
                  onChange={(e) => setBusinessType(e.target.value)}
                  placeholder="전체 업종"
                >
                  <option value="일반음식점">일반음식점</option>
                  <option value="카페">카페</option>
                  <option value="편의점">편의점</option>
                  <option value="미용실">미용실</option>
                  <option value="의류">의류</option>
                </Select>
              </Box>
              <Box>
                <Text fontWeight="medium" mb={2}>반경 (미터)</Text>
                <Select
                  value={radius}
                  onChange={(e) => setRadius(Number(e.target.value))}
                >
                  <option value={500}>500m</option>
                  <option value={1000}>1km</option>
                  <option value={2000}>2km</option>
                  <option value={5000}>5km</option>
                </Select>
              </Box>
              <Box>
                <Text fontWeight="medium" mb={2}>상태</Text>
                <Badge colorScheme={loading ? "yellow" : "green"} p={2} borderRadius="md">
                  {loading ? "분석 중..." : `${nearbyStores.length}개 상가 발견`}
                </Badge>
              </Box>
            </SimpleGrid>
          </CardBody>
        </Card>

        {loading ? (
          <Box textAlign="center" py={10}>
            <Spinner size="xl" color="brand.500" />
            <Text mt={4} color="gray.600">실제 상권 데이터를 분석 중입니다...</Text>
          </Box>
        ) : (
          <Tabs variant="enclosed" colorScheme="brand">
            <TabList>
              <Tab>상권 개요</Tab>
              <Tab>지역별 상세분석</Tab>
              <Tab>경쟁 현황</Tab>
              <Tab>업종별 통계</Tab>
            </TabList>

            <TabPanels>
              {/* 상권 개요 */}
              <TabPanel>
                <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                  {regionAnalysis.map((analysis, index) => (
                    <Card key={index} cursor="pointer" _hover={{ shadow: "lg" }}>
                      <CardBody>
                        <VStack align="stretch" spacing={4}>
                          <HStack justify="space-between">
                            <Text fontWeight="bold" fontSize="lg">{analysis.region}</Text>
                            <Badge colorScheme={getCompetitionColor(analysis.competitionLevel)}>
                              경쟁도: {getCompetitionText(analysis.competitionLevel)}
                            </Badge>
                          </HStack>

                          <Stat>
                            <StatLabel>총 상가 수</StatLabel>
                            <StatNumber>{analysis.totalStores}개</StatNumber>
                            <StatHelpText>반경 {radius}m 내</StatHelpText>
                          </Stat>

                          <Box>
                            <Text fontSize="sm" color="gray.600" mb={2}>주요 업종</Text>
                            <VStack spacing={2}>
                              {Object.entries(analysis.businessTypes)
                                .sort(([,a], [,b]) => b - a)
                                .slice(0, 3)
                                .map(([type, count]) => {
                                  const percentage = (count / analysis.totalStores) * 100;
                                  return (
                                    <Box key={type} w="100%">
                                      <HStack justify="space-between" fontSize="xs">
                                        <Text>{type}</Text>
                                        <Text>{count}개 ({percentage.toFixed(1)}%)</Text>
                                      </HStack>
                                      <Progress value={percentage} colorScheme="brand" size="sm" />
                                    </Box>
                                  );
                                })}
                            </VStack>
                          </Box>

                          <Box>
                            <Text fontSize="sm" color="gray.600" mb={1}>평균 거리</Text>
                            <Text fontSize="lg" fontWeight="bold" color="brand.500">
                              {analysis.averageDistance.toFixed(0)}m
                            </Text>
                          </Box>
                        </VStack>
                      </CardBody>
                    </Card>
                  ))}
                </SimpleGrid>
              </TabPanel>

              {/* 지역별 상세분석 */}
              <TabPanel>
                <VStack spacing={6}>
                  {nearbyStores.slice(0, 20).map((store, index) => (
                    <Card key={store.id || index} w="100%">
                      <CardBody>
                        <HStack justify="space-between">
                          <VStack align="start" spacing={2}>
                            <Text fontWeight="bold" fontSize="lg">{store.store_name}</Text>
                            <Text color="gray.600">{store.business_name}</Text>
                            <Text fontSize="sm" color="gray.500">{store.road_address || store.jibun_address}</Text>
                            <HStack>
                              <Badge colorScheme="blue">{store.sido_name} {store.sigungu_name}</Badge>
                              <Badge colorScheme="green">{store.business_status}</Badge>
                            </HStack>
                          </VStack>
                          <VStack align="end" spacing={2}>
                            <Text fontSize="lg" fontWeight="bold" color="brand.500">
                              {store.distance ? `${store.distance.toFixed(0)}m` : "거리 정보 없음"}
                            </Text>
                            <HStack>
                              <Icon as={FiMapPin} color="gray.400" />
                              <Text fontSize="sm" color="gray.500">
                                {store.latitude.toFixed(4)}, {store.longitude.toFixed(4)}
                              </Text>
                            </HStack>
                          </VStack>
                        </HStack>
                      </CardBody>
                    </Card>
                  ))}
                </VStack>
              </TabPanel>

              {/* 경쟁 현황 */}
              <TabPanel>
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                  <Card>
                    <CardBody>
                      <VStack align="stretch" spacing={4}>
                        <Heading size="md">경쟁 밀도 분석</Heading>
                        <Text color="gray.600">
                          선택된 지역 반경 {radius}m 내 상가 밀도와 경쟁 수준을 분석합니다.
                        </Text>
                        <Stat>
                          <StatLabel>총 발견된 상가</StatLabel>
                          <StatNumber>{nearbyStores.length}개</StatNumber>
                          <StatHelpText>
                            {nearbyStores.length > 50 ? "매우 높은 밀도" : 
                             nearbyStores.length > 20 ? "보통 밀도" : "낮은 밀도"}
                          </StatHelpText>
                        </Stat>
                      </VStack>
                    </CardBody>
                  </Card>

                  <Card>
                    <CardBody>
                      <VStack align="stretch" spacing={4}>
                        <Heading size="md">업종별 분포</Heading>
                        {statistics && (
                          <VStack spacing={3}>
                            {statistics.business_type_stats.slice(0, 5).map((item, index) => (
                              <Box key={index} w="100%">
                                <HStack justify="space-between" mb={1}>
                                  <Text fontSize="sm">{item.business_name}</Text>
                                  <Text fontSize="sm" fontWeight="bold">{item.store_count}개</Text>
                                </HStack>
                                <Progress 
                                  value={item.percentage} 
                                  colorScheme="brand" 
                                  size="sm" 
                                />
                              </Box>
                            ))}
                          </VStack>
                        )}
                      </VStack>
                    </CardBody>
                  </Card>
                </SimpleGrid>
              </TabPanel>

              {/* 업종별 통계 */}
              <TabPanel>
                {statistics ? (
                  <VStack spacing={6}>
                    <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} w="100%">
                      <Card>
                        <CardBody>
                          <Stat>
                            <StatLabel>발견된 상가 수</StatLabel>
                            <StatNumber>{nearbyStores.length.toLocaleString()}</StatNumber>
                            <StatHelpText>반경 {radius}m 내</StatHelpText>
                          </Stat>
                        </CardBody>
                      </Card>

                      <Card>
                        <CardBody>
                          <Stat>
                            <StatLabel>업종 수</StatLabel>
                            <StatNumber>{statistics.business_type_stats.length}</StatNumber>
                            <StatHelpText>서로 다른 업종</StatHelpText>
                          </Stat>
                        </CardBody>
                      </Card>

                      <Card>
                        <CardBody>
                          <Stat>
                            <StatLabel>지역 수</StatLabel>
                            <StatNumber>{statistics.region_stats.length}</StatNumber>
                            <StatHelpText>서로 다른 지역</StatHelpText>
                          </Stat>
                        </CardBody>
                      </Card>
                    </SimpleGrid>

                    <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} w="100%">
                      <Card>
                        <CardBody>
                          <Heading size="md" mb={4}>업종별 분포</Heading>
                          <VStack spacing={3}>
                            {statistics.business_type_stats.slice(0, 10).map((item, index) => (
                              <Box key={index} w="100%">
                                <HStack justify="space-between" mb={1}>
                                  <Text fontSize="sm">{item.business_name}</Text>
                                  <Text fontSize="sm" fontWeight="bold">{item.store_count}개 ({item.percentage}%)</Text>
                                </HStack>
                                <Progress 
                                  value={item.percentage} 
                                  colorScheme="brand" 
                                  size="sm" 
                                />
                              </Box>
                            ))}
                          </VStack>
                        </CardBody>
                      </Card>

                      <Card>
                        <CardBody>
                          <Heading size="md" mb={4}>지역별 분포</Heading>
                          <VStack spacing={3}>
                            {statistics.region_stats.slice(0, 10).map((item, index) => (
                              <Box key={index} w="100%">
                                <HStack justify="space-between" mb={1}>
                                  <Text fontSize="sm">{item.region_name}</Text>
                                  <Text fontSize="sm" fontWeight="bold">{item.store_count}개</Text>
                                </HStack>
                                <Progress 
                                  value={(item.store_count / Math.max(...statistics.region_stats.map(r => r.store_count))) * 100} 
                                  colorScheme="green" 
                                  size="sm" 
                                />
                              </Box>
                            ))}
                          </VStack>
                        </CardBody>
                      </Card>
                    </SimpleGrid>
                  </VStack>
                ) : (
                  <Alert status="info">
                    <AlertIcon />
                    <AlertTitle>통계 데이터 로딩 중</AlertTitle>
                    <AlertDescription>
                      업종별 통계를 집계하고 있습니다. 잠시만 기다려주세요.
                    </AlertDescription>
                  </Alert>
                )}
              </TabPanel>
            </TabPanels>
          </Tabs>
        )}

        {/* 데이터 소스 정보 */}
        <Card>
          <CardBody>
            <HStack spacing={4}>
              <Icon as={FiBarChart} color="brand.500" boxSize={6} />
              <VStack align="start" spacing={1}>
                <Text fontWeight="bold">데이터 소스</Text>
                <Text fontSize="sm" color="gray.600">
                  공공데이터포털 - 소상공인시장진흥공단 상가(상권)정보 API
                </Text>
                <Text fontSize="xs" color="gray.500">
                  실시간 공공데이터를 활용한 정확한 상권 분석 정보를 제공합니다.
                </Text>
              </VStack>
            </HStack>
          </CardBody>
        </Card>
      </VStack>
    </Container>
  );
};

export default CommercialAnalysisPage; 
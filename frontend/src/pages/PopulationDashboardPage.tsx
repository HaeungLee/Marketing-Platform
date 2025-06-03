import { FC } from 'react';
import {
  Box,
  Card,
  CardBody,
  FormControl,
  FormLabel,
  Grid,
  GridItem,
  Select,
  Heading,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Spinner,
  Center,
  Stack,
  Stat,
  StatLabel,
  StatNumber,
  useToast
} from '@chakra-ui/react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useState, useEffect } from 'react';
import axios from 'axios';

interface Location {
  provinces: string[];
  cities: string[] | Record<string, string[]>;
  districts: Record<string, Record<string, string[]>>;
}

interface PopulationData {
  province: string;
  city: string;
  district: string;
  reference_date: string;
  age_groups: {
    ageGroup: string;
    male: number;
    female: number;
  }[];
  total: {
    total: number;
    male: number;
    female: number;
  };
}

const PopulationDashboardPage: FC = () => {
  const [locations, setLocations] = useState<Location>({
    provinces: [],
    cities: [],
    districts: {},
  } as Location);
  const [selectedProvince, setSelectedProvince] = useState<string>('');
  const [selectedCity, setSelectedCity] = useState<string>('');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');  
  const [populationData, setPopulationData] = useState<Partial<PopulationData> | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const toast = useToast();

  // 지역 데이터 로드
  useEffect(() => {
    const fetchLocations = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await axios.get('/api/v1/population/locations');
        setLocations({
          provinces: response.data.provinces || [],
          cities: response.data.cities || [],
          districts: response.data.districts || [],
        });
      } catch (error) {
        const message = error instanceof Error ? error.message : '지역 데이터를 불러오는데 실패했습니다.';
        setError(message);
        toast({
          title: '데이터 로드 실패',
          description: message,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setIsLoading(false);
      }
    };
    fetchLocations();
  }, [toast]);

  // 시/도 선택 시 시/군/구 목록 업데이트
  useEffect(() => {
    if (selectedProvince) {
      const fetchCities = async () => {
        console.log('Fetching cities for province:', selectedProvince);
        setIsLoading(true);
        setError(null);
        try {
          const response = await axios.get(`/api/v1/population/locations?province=${encodeURIComponent(selectedProvince)}`);
          console.log('Cities API response:', JSON.stringify(response.data, null, 2));
          
          // cities가 객체로 오는 경우, 선택된 도시의 배열을 가져옵니다.
          const citiesData = response.data.cities;
          const selectedCities = Array.isArray(citiesData) 
            ? citiesData 
            : (citiesData && citiesData[selectedProvince]) || [];
          
          const districts = response.data.districts || {};
          
          console.log('Selected cities:', selectedCities);
          console.log('Districts structure:', JSON.stringify(districts, null, 2));
          
          setLocations(prev => ({
            ...prev,
            cities: selectedCities,
            districts
          }));
          
          console.log('Updated locations state:', {
            cities: selectedCities.length,
            districts: Object.keys(districts).length > 0 ? 'available' : 'empty'
          });
        } catch (error) {
          console.error('Error fetching cities:', error);
          const message = error instanceof Error ? error.message : '시/군/구 데이터를 불러오는데 실패했습니다.';
          setError(message);
          toast({
            title: '데이터 로드 실패',
            description: message,
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
        } finally {
          setIsLoading(false);
        }
      };
      fetchCities();
    } else {
      // 시/도 선택이 해제되면 시/군/구 목록 초기화
      setLocations(prev => ({ ...prev, cities: [], districts: {} }));
      setSelectedCity('');
      setSelectedDistrict('');
    }
  }, [selectedProvince, toast]);

  // 시/군/구 선택 시 읍/면/동 목록 업데이트
  useEffect(() => {
    if (selectedProvince && selectedCity) {
      const fetchDistricts = async () => {
        setIsLoading(true);
        setError(null);
        try {
          const response = await axios.get(
            `/api/v1/population/locations?province=${selectedProvince}&city=${selectedCity}`
          );
          // districts가 객체 형태로 오는 경우를 처리
          const districtsData = response.data.districts;
          setLocations(prev => ({
            ...prev,
            districts: districtsData || {}
          }));
        } catch (error) {
          const message = error instanceof Error ? error.message : '읍/면/동 데이터를 불러오는데 실패했습니다.';
          setError(message);
          toast({
            title: '데이터 로드 실패',
            description: message,
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
        } finally {
          setIsLoading(false);
        }
      };
      fetchDistricts();
    }
  }, [selectedProvince, selectedCity, toast]);

  // 지역 선택 시 인구 통계 데이터 로드
  useEffect(() => {
    if (selectedProvince && selectedCity && selectedDistrict) {
      console.log('인구 통계 데이터 요청 파라미터:', { 
        province: selectedProvince, 
        city: selectedCity, 
        district: selectedDistrict 
      });
      
      const fetchPopulationData = async () => {
        setIsLoading(true);
        setError(null);
        try {
          const response = await axios.get('/api/v1/population/statistics', {
            params: {
              province: selectedProvince,
              city: selectedCity, 
              district: selectedDistrict,
            },
          });
          
          console.log('=== API 응답 전체 구조 ===');
          console.log('응답 데이터 타입:', typeof response.data);
          console.log('응답 데이터:', response.data);
          
          // API 응답이 배열인 경우 첫 번째 항목 사용
          const responseData = Array.isArray(response.data) ? response.data[0] : response.data;
          
          // 응답 데이터의 모든 키 출력
          console.log('응답 데이터 키들:', Object.keys(responseData));
          
          // 연령대별 데이터를 배열로 변환
          const ageGroups = [
            { ageGroup: '0-9', male: parseInt(responseData.age_0_9_male) || 0, female: parseInt(responseData.age_0_9_female) || 0 },
            { ageGroup: '10-19', male: parseInt(responseData.age_10_19_male) || 0, female: parseInt(responseData.age_10_19_female) || 0 },
            { ageGroup: '20-29', male: parseInt(responseData.age_20_29_male) || 0, female: parseInt(responseData.age_20_29_female) || 0 },
            { ageGroup: '30-39', male: parseInt(responseData.age_30_39_male) || 0, female: parseInt(responseData.age_30_39_female) || 0 },
            { ageGroup: '40-49', male: parseInt(responseData.age_40_49_male) || 0, female: parseInt(responseData.age_40_49_female) || 0 },
            { ageGroup: '50-59', male: parseInt(responseData.age_50_59_male) || 0, female: parseInt(responseData.age_50_59_female) || 0 },
            { ageGroup: '60-69', male: parseInt(responseData.age_60_69_male) || 0, female: parseInt(responseData.age_60_69_female) || 0 },
            { ageGroup: '70-79', male: parseInt(responseData.age_70_79_male) || 0, female: parseInt(responseData.age_70_79_female) || 0 },
            { ageGroup: '80+', 
              male: (parseInt(responseData.age_80_89_male) || 0) + (parseInt(responseData.age_90_99_male) || 0) + (parseInt(responseData.age_100_plus_male) || 0), 
              female: (parseInt(responseData.age_80_89_female) || 0) + (parseInt(responseData.age_90_99_female) || 0) + (parseInt(responseData.age_100_plus_female) || 0) 
            }
          ];
          
          console.log('생성된 age_groups 데이터:', ageGroups);
          
          // 총 인구 데이터 설정 (API 응답에서 직접 가져오거나, 연령대별 합계 계산)
          const totalMale = ageGroups.reduce((sum, item) => sum + (item.male || 0), 0);
          const totalFemale = ageGroups.reduce((sum, item) => sum + (item.female || 0), 0);
          
          const totalData = {
            total: totalMale + totalFemale,
            male: totalMale,
            female: totalFemale
          };
          
          console.log('총 인구 데이터:', totalData);
          
          // 상태 업데이트
          setPopulationData({
            ...responseData,
            age_groups: ageGroups.length > 0 ? ageGroups : [
              { ageGroup: '0-9', male: 0, female: 0 },
              { ageGroup: '10-19', male: 0, female: 0 },
              { ageGroup: '20-29', male: 0, female: 0 },
              { ageGroup: '30-39', male: 0, female: 0 },
              { ageGroup: '40-49', male: 0, female: 0 },
              { ageGroup: '50-59', male: 0, female: 0 },
              { ageGroup: '60-69', male: 0, female: 0 },
              { ageGroup: '70-79', male: 0, female: 0 },
              { ageGroup: '80+', male: 0, female: 0 }
            ],
            total: totalData
          });
        } catch (error) {
          const message = error instanceof Error ? error.message : '인구 통계 데이터를 불러오는데 실패했습니다.';
          setError(message);
          toast({
            title: '데이터 로드 실패',
            description: message,
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
        } finally {
          setIsLoading(false);
        }
      };
      fetchPopulationData();
    }
  }, [selectedProvince, selectedCity, selectedDistrict, toast]);

  if (error) {
    return (
      <Alert status="error">
        <AlertIcon />
        <Box>
          <AlertTitle>오류 발생</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Box>
      </Alert>
    );
  }

  return (
    <Box p={5}>
      <Stack spacing={5}>
        <Heading size="lg">지역별 인구 통계</Heading>

        <Grid templateColumns="repeat(3, 1fr)" gap={4}>
          <GridItem>
            <FormControl isDisabled={isLoading}>
              <FormLabel>시/도</FormLabel>
              <Select
                placeholder="시/도 선택"
                value={selectedProvince}
                onChange={(e) => {
                  setSelectedProvince(e.target.value);
                  setSelectedCity('');
                  setSelectedDistrict('');
                }}
              >
                {locations.provinces.map((province) => (
                  <option key={province} value={province}>
                    {province}
                  </option>
                ))}
              </Select>
            </FormControl>
          </GridItem>

          <GridItem>
            <FormControl isDisabled={!selectedProvince || isLoading}>
              <FormLabel>시/군/구</FormLabel>
              <Select
                placeholder={isLoading ? '로드 중...' : '시/군/구 선택'}
                value={selectedCity}
                onChange={(e) => {
                  setSelectedCity(e.target.value);
                  setSelectedDistrict('');
                }}
                isDisabled={isLoading || !selectedProvince}
              >
                {isLoading ? (
                  <option disabled>로드 중...</option>
                ) : Array.isArray(locations.cities) && locations.cities.length > 0 ? (
                  locations.cities.map((city: string) => (
                    <option key={city} value={city}>
                      {city}
                    </option>
                  ))
                ) : (
                  <option disabled>선택 가능한 시/군/구가 없습니다</option>
                )}
              </Select>
            </FormControl>
          </GridItem>

          <GridItem>
            <FormControl isDisabled={!selectedCity || isLoading}>
              <FormLabel>읍/면/동</FormLabel>
              <Select
                placeholder={isLoading ? '로드 중...' : '읍/면/동 선택'}
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                isDisabled={isLoading || !selectedCity}
              >
                {isLoading ? (
                  <option disabled>로드 중...</option>
                ) : selectedProvince && selectedCity && locations.districts[selectedProvince]?.[selectedCity]?.length > 0 ? (
                  locations.districts[selectedProvince][selectedCity].map((district: string) => (
                    <option key={district} value={district}>
                      {district}
                    </option>
                  ))
                ) : (
                  <option disabled>선택 가능한 읍/면/동이 없습니다</option>
                )}
              </Select>
            </FormControl>
          </GridItem>
        </Grid>

        {isLoading && (
          <Center py={10}>
            <Spinner
              thickness="4px"
              speed="0.65s"
              emptyColor="gray.200"
              color="blue.500"
              size="xl"
            />
          </Center>
        )}

        {populationData && !isLoading && (
          <Stack spacing={5}>
            <Card>
              <CardBody>
                <Heading size="md" mb={4}>연령별 성별 인구 분포</Heading>
                <Box height="400px">
                  <ResponsiveContainer>
                    <BarChart
                      data={populationData?.age_groups || []}
                      margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="ageGroup" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="male" name="남성" fill="#2B6CB0" />
                      <Bar dataKey="female" name="여성" fill="#D53F8C" />
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
              </CardBody>
            </Card>

            <Grid templateColumns="repeat(3, 1fr)" gap={4}>
              <GridItem>
                <Card>
                  <CardBody>
                    <Stat>
                      <StatLabel>총 인구</StatLabel>
                      <StatNumber>{(populationData?.total?.total || 0).toLocaleString()}명</StatNumber>
                    </Stat>
                  </CardBody>
                </Card>
              </GridItem>

              <GridItem>
                <Card>
                  <CardBody>
                    <Stat>
                      <StatLabel>남성 인구</StatLabel>
                      <StatNumber color="blue.600">
                        {(populationData?.total?.male || 0).toLocaleString()}명
                      </StatNumber>
                    </Stat>
                  </CardBody>
                </Card>
              </GridItem>

              <GridItem>
                <Card>
                  <CardBody>
                    <Stat>
                      <StatLabel>여성 인구</StatLabel>
                      <StatNumber color="pink.600">
                        {(populationData?.total?.female || 0).toLocaleString()}명
                      </StatNumber>
                    </Stat>
                  </CardBody>
                </Card>
              </GridItem>
            </Grid>
          </Stack>
        )}
      </Stack>
    </Box>
  );
};

export default PopulationDashboardPage;

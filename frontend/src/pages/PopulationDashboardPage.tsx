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
  cities: string[] | null;
  districts: string[] | null;
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
  const [locations, setLocations] = useState<Location>({ provinces: [], cities: null, districts: null });
  const [selectedProvince, setSelectedProvince] = useState<string>('');
  const [selectedCity, setSelectedCity] = useState<string>('');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [populationData, setPopulationData] = useState<PopulationData | null>(null);
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
        setLocations(response.data);
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
        setIsLoading(true);
        setError(null);
        try {
          const response = await axios.get(`/api/v1/population/locations?province=${selectedProvince}`);
          setLocations(prev => ({ ...prev, cities: response.data.cities }));
        } catch (error) {
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
          setLocations(prev => ({ ...prev, districts: response.data.districts }));
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
          setPopulationData(response.data);
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
                placeholder="시/군/구 선택"
                value={selectedCity}
                onChange={(e) => {
                  setSelectedCity(e.target.value);
                  setSelectedDistrict('');
                }}
              >
                {locations.cities?.map((city) => (
                  <option key={city} value={city}>
                    {city}
                  </option>
                ))}
              </Select>
            </FormControl>
          </GridItem>

          <GridItem>
            <FormControl isDisabled={!selectedCity || isLoading}>
              <FormLabel>읍/면/동</FormLabel>
              <Select
                placeholder="읍/면/동 선택"
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
              >
                {locations.districts?.map((district) => (
                  <option key={district} value={district}>
                    {district}
                  </option>
                ))}
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
                      data={populationData.age_groups}
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
                      <StatNumber>{populationData.total.total.toLocaleString()}명</StatNumber>
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
                        {populationData.total.male.toLocaleString()}명
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
                        {populationData.total.female.toLocaleString()}명
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

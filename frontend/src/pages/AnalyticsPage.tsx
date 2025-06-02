import React, { useState } from "react";
import {
  Box,
  Text,
  VStack,
  HStack,
  Card,
  CardBody,
  CardHeader,
  Button,
  ButtonGroup,
  Grid,
  Select,
  Badge,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Divider,
  SimpleGrid,
  Progress,
  useColorModeValue,
  Heading
} from "@chakra-ui/react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
} from "recharts";
import {
  FaChartLine,
  FaUsers,
  FaEye,
  FaHeart,
  FaArrowUp,
  FaArrowDown,
  FaCalendarAlt,
} from "react-icons/fa";


const AnalyticsPage: React.FC = () => {
  const [timeRange, setTimeRange] = useState("7d");
  const [selectedTab, setSelectedTab] = useState(0);
  const cardBg = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.700");
  const [viewMode, setViewMode] = useState<'gender' | 'age'>('gender');

  // 목업 데이터
  const performanceData = [
    { date: "1일전", views: 1200, likes: 85, shares: 23, clicks: 156 },
    { date: "2일전", views: 980, likes: 67, shares: 18, clicks: 134 },
    { date: "3일전", views: 1450, likes: 102, shares: 31, clicks: 198 },
    { date: "4일전", views: 1100, likes: 78, shares: 22, clicks: 167 },
    { date: "5일전", views: 1350, likes: 95, shares: 28, clicks: 189 },
    { date: "6일전", views: 890, likes: 59, shares: 15, clicks: 123 },
    { date: "7일전", views: 1280, likes: 89, shares: 25, clicks: 178 },
  ];

  const audienceData = [
    { age: "20-29", percentage: 35, count: 2450 },
    { age: "30-39", percentage: 28, count: 1960 },
    { age: "40-49", percentage: 22, count: 1540 },
    { age: "50-59", percentage: 12, count: 840 },
    { age: "60+", percentage: 3, count: 210 },
  ];

  const platformData = [
    { name: "네이버 블로그", value: 45, color: "#00C851" },
    { name: "인스타그램", value: 30, color: "#E91E63" },
    { name: "유튜브", value: 20, color: "#FF3737" },
    { name: "기타", value: 5, color: "#6C757D" },
  ];

  const competitorData = [
    { metric: "콘텐츠 품질", 우리: 85, 경쟁사1: 78, 경쟁사2: 82 },
    { metric: "참여도", 우리: 92, 경쟁사1: 85, 경쟁사2: 88 },
    { metric: "도달률", 우리: 78, 경쟁사1: 82, 경쟁사2: 75 },
    { metric: "브랜드 인지도", 우리: 88, 경쟁사1: 90, 경쟁사2: 85 },
    { metric: "고객 만족도", 우리: 95, 경쟁사1: 88, 경쟁사2: 90 },
  ];

  const trendingKeywords = [
    { keyword: "친환경", trend: "+25%", searches: 12500 },
    { keyword: "할인이벤트", trend: "+18%", searches: 8900 },
    { keyword: "신제품", trend: "+15%", searches: 7800 },
    { keyword: "무료배송", trend: "+12%", searches: 6700 },
    { keyword: "리뷰", trend: "-5%", searches: 5600 },
  ];

  // 시간대별 소비/유동인구 (00시~23시까지)
  const timeBasedData = Array.from({ length: 24 }, (_, i) => ({
    시간대: `${String(i).padStart(2, '0')}:00`,
    소비금액: Math.floor(Math.random() * 300000),
    유동인구: Math.floor(Math.random() * 500),
  }));

  // 연령대x성별 전체 연령대
  const targetAudienceData = [
    { age: "10대", 남성: 5, 여성: 4 },
    { age: "20대", 남성: 15, 여성: 18 },
    { age: "30대", 남성: 25, 여성: 22 },
    { age: "40대", 남성: 10, 여성: 12 },
    { age: "50대", 남성: 8, 여성: 9 },
    { age: "60대", 남성: 6, 여성: 5 },
    { age: "70대+", 남성: 3, 여성: 4 },
  ];

  const StatCard = ({ title, value, change, icon, color }: any) => (
    <Card bg={cardBg} borderColor={borderColor}>
      <CardBody>
        <Stat>
          <StatLabel display="flex" alignItems="center" gap={2}>
            <Box as={icon} color={color} />
            {title}
          </StatLabel>
          <StatNumber fontSize="2xl" fontWeight="bold">
            {value}
          </StatNumber>
          <StatHelpText>
            <StatArrow type={change > 0 ? "increase" : "decrease"} />
            {Math.abs(change)}% vs 지난주
          </StatHelpText>
        </Stat>
      </CardBody>
    </Card>
  );

  const ChartCard = ({ title, children }: any) => (
    <Card bg={cardBg} borderColor={borderColor}>
      <CardHeader>
        <Text fontSize="lg" fontWeight="bold">
          {title}
        </Text>
      </CardHeader>
      <CardBody>{children}</CardBody>
    </Card>
  );

  return (
    <Box>
      <HStack justify="space-between" mb={6}>
        <Text fontSize="2xl" fontWeight="bold">
          분석 & 인사이트
        </Text>
        <HStack>
          <Select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            w="150px"
          >
            <option value="7d">최근 7일</option>
            <option value="30d">최근 30일</option>
            <option value="90d">최근 3개월</option>
          </Select>
          <Button leftIcon={<FaCalendarAlt />} variant="outline">
            사용자 정의
          </Button>
        </HStack>
      </HStack>

      {/* KPI Cards */}
      <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6} mb={8}>
        <StatCard
          title="총 조회수"
          value="8.7K"
          change={15.3}
          icon={FaEye}
          color="blue.500"
        />
        <StatCard
          title="참여율"
          value="7.2%"
          change={8.1}
          icon={FaHeart}
          color="pink.500"
        />
        <StatCard
          title="도달 사용자"
          value="5.1K"
          change={12.7}
          icon={FaUsers}
          color="green.500"
        />
        <StatCard
          title="전환율"
          value="3.4%"
          change={-2.1}
          icon={FaChartLine}
          color="purple.500"
        />
      </SimpleGrid>

      <Tabs index={selectedTab} onChange={setSelectedTab}>
        <TabList>
          <Tab>성과 분석</Tab>
          <Tab>고객 분석</Tab>
          <Tab>경쟁사 분석</Tab>
          <Tab>트렌드 분석</Tab>
        </TabList>

        <TabPanels>
          {/* 성과 분석 */}
          <TabPanel p={0} pt={6}>
            <VStack align="stretch" spacing={6}>
              <ChartCard title="SNS 채널별 조회수 추이 (최근 4주)">
                <Box display="flex" alignItems="center" justifyContent="center" h={250}>
                  <Text color="gray.400">SNS 데이터 연동 시 조회수 트렌드를 표시합니다.</Text>
                </Box>
              </ChartCard>
              <ChartCard title="월별 매출/방문자 수 추이">
                <Box display="flex" alignItems="center" justifyContent="center" h={250}>
                  <Text color="gray.400">POS 또는 수기 입력 기반 매출/방문자 데이터를 표시합니다.</Text>
                </Box>
              </ChartCard>
              <ChartCard title="게시물별 조회수/좋아요 TOP5">
                <Box display="flex" alignItems="center" justifyContent="center" h={250}>
                  <Text color="gray.400">SNS 연동 시 인기 게시물 정보를 표로 제공합니다.</Text>
                </Box>
              </ChartCard>
            </VStack>
          </TabPanel>

          {/* 고객 분석 */}
          <TabPanel p={0} pt={6}>
            <VStack align="stretch" spacing={4}>
              <Heading size="md" mb={2}>타겟 고객 분석</Heading>
              {/* 성별별 시간대별 소비 & 유동인구 추이 */}
              <ChartCard title="시간대별 소비 & 유동인구 추이">
                <VStack align="start" spacing={4}>
                  <ButtonGroup size="sm" isAttached>
                    <Button onClick={() => setViewMode('gender')} isActive={viewMode === 'gender'}>
                      성별 기준
                    </Button>
                    <Button onClick={() => setViewMode('age')} isActive={viewMode === 'age'}>
                      연령대 기준
                    </Button>
                  </ButtonGroup>

                  <ResponsiveContainer width="100%" height={250}>
                    {viewMode === 'gender' ? (
                      <LineChart
                        data={[
                          { 시간: '00시', 남성_소비: 15000, 여성_소비: 12000, 남성_유동: 350, 여성_유동: 300 },
                          { 시간: '06시', 남성_소비: 17000, 여성_소비: 16000, 남성_유동: 700, 여성_유동: 680 },
                          { 시간: '08시', 남성_소비: 25000, 여성_소비: 27000, 남성_유동: 1200, 여성_유동: 1300 },
                          { 시간: '12시', 남성_소비: 35000, 여성_소비: 37000, 남성_유동: 2000, 여성_유동: 2200 },
                          { 시간: '14시', 남성_소비: 42000, 여성_소비: 46000, 남성_유동: 2300, 여성_유동: 2500 },
                          { 시간: '18시', 남성_소비: 44000, 여성_소비: 50000, 남성_유동: 2700, 여성_유동: 2900 },
                          { 시간: '22시', 남성_소비: 41000, 여성_소비: 48000, 남성_유동: 2600, 여성_유동: 2800 },
                        ]}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="시간" />
                        <YAxis
                          yAxisId="left"
                          tickFormatter={(v) => `${v / 1000}K`}
                          label={{ value: '소비금액 (원)', angle: -90, position: 'insideLeft', offset: 10 }}
                        />
                        <YAxis
                          yAxisId="right"
                          orientation="right"
                          label={{ value: '유동인구 (명)', angle: -90, position: 'insideLeft', offset: 50 }}
                        />
                        <Tooltip />
                        <Legend
                          verticalAlign="top"
                          align="right"
                          wrapperStyle={{
                            paddingBottom: 5,
                            marginTop: -5,
                            textAlign: 'center',
                          }}
                        />
                        <Line yAxisId="left" type="monotone" dataKey="남성_소비" stroke="#2B6CB0" strokeWidth={2} />
                        <Line yAxisId="left" type="monotone" dataKey="여성_소비" stroke="#C53030" strokeWidth={2} />
                        <Line yAxisId="right" type="monotone" dataKey="남성_유동" stroke="#3182CE" strokeDasharray="4 4" strokeWidth={1.5} />
                        <Line yAxisId="right" type="monotone" dataKey="여성_유동" stroke="#DD6B20" strokeDasharray="4 4" strokeWidth={1.5} />
                      </LineChart>
                    ) : (
                      <LineChart
                        data={[
                          { 시간: '00시', '20대': 14000, '30대': 16000, '40대': 10000, '50대': 8000, '20대_유동': 300, '30대_유동': 350, '40대_유동': 280, '50대_유동': 260 },
                          { 시간: '06시', '20대': 18000, '30대': 20000, '40대': 14000, '50대': 11000, '20대_유동': 700, '30대_유동': 750, '40대_유동': 680, '50대_유동': 620 },
                          { 시간: '08시', '20대': 25000, '30대': 27000, '40대': 18000, '50대': 15000, '20대_유동': 1200, '30대_유동': 1300, '40대_유동': 1100, '50대_유동': 900 },
                          { 시간: '12시', '20대': 32000, '30대': 36000, '40대': 24000, '50대': 20000, '20대_유동': 1900, '30대_유동': 2100, '40대_유동': 1700, '50대_유동': 1500 },
                          { 시간: '14시', '20대': 37000, '30대': 41000, '40대': 28000, '50대': 23000, '20대_유동': 2400, '30대_유동': 2600, '40대_유동': 2100, '50대_유동': 1800 },
                          { 시간: '18시', '20대': 39000, '30대': 43000, '40대': 31000, '50대': 26000, '20대_유동': 2800, '30대_유동': 3000, '40대_유동': 2500, '50대_유동': 2200 },
                          { 시간: '22시', '20대': 35000, '30대': 40000, '40대': 29000, '50대': 24000, '20대_유동': 2700, '30대_유동': 2900, '40대_유동': 2300, '50대_유동': 2100 },
                        ]}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="시간" />
                        <YAxis
                          yAxisId="left"
                          tickFormatter={(v) => `${v / 1000}K`}
                          label={{ value: '소비금액 (원)', angle: -90, position: 'insideLeft', offset: 10 }}
                        />
                        <YAxis
                          yAxisId="right"
                          orientation="right"
                          label={{ value: '유동인구 (명)', angle: -90, position: 'insideLeft', offset: 50 }}
                        />
                        <Tooltip />
                        <Legend
                          verticalAlign="top"
                          align="right"
                          wrapperStyle={{
                            paddingBottom: 5,
                            marginTop: -5,
                            textAlign: 'center',
                          }}
                        />
                        <Legend verticalAlign="top" align="right" />
                        <Line yAxisId="left" type="monotone" dataKey="20대" stroke="#4299E1" strokeWidth={2} />
                        <Line yAxisId="left" type="monotone" dataKey="30대" stroke="#9F7AEA" strokeWidth={2} />
                        <Line yAxisId="left" type="monotone" dataKey="40대" stroke="#48BB78" strokeWidth={2} />
                        <Line yAxisId="left" type="monotone" dataKey="50대" stroke="#ED8936" strokeWidth={2} />
                        <Line yAxisId="right" type="monotone" dataKey="20대_유동" stroke="#4299E1" strokeDasharray="4 4" strokeWidth={1.5} />
                        <Line yAxisId="right" type="monotone" dataKey="30대_유동" stroke="#9F7AEA" strokeDasharray="4 4" strokeWidth={1.5} />
                        <Line yAxisId="right" type="monotone" dataKey="40대_유동" stroke="#48BB78" strokeDasharray="4 4" strokeWidth={1.5} />
                        <Line yAxisId="right" type="monotone" dataKey="50대_유동" stroke="#ED8936" strokeDasharray="4 4" strokeWidth={1.5} />
                      </LineChart>
                    )}
                  </ResponsiveContainer>
                </VStack>
              </ChartCard>

              {/* 추가: 네 개의 새로운 차트 카드 */}
              <VStack align="stretch" spacing={4} mt={4}>
                {/* 1. 요일별 유동인구 추이 */}
                <ChartCard title="요일별 유동인구 추이">
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart
                      data={[
                        { 요일: '월', 유동인구: 1200 },
                        { 요일: '화', 유동인구: 1500 },
                        { 요일: '수', 유동인구: 1700 },
                        { 요일: '목', 유동인구: 1400 },
                        { 요일: '금', 유동인구: 1900 },
                        { 요일: '토', 유동인구: 2400 },
                        { 요일: '일', 유동인구: 2200 },
                      ]}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="요일" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="유동인구" stroke="#38A169" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </ChartCard>

                {/* 2. 업종별 소비 비중 */}
                <ChartCard title="업종별 소비 비중">
                  <Box>
                    <ResponsiveContainer width="100%" height={250}>
                      <BarChart
                        layout="vertical"
                        data={[
                          { 업종: '카페·음료', 소비금액: 1400000 },
                          { 업종: '한식', 소비금액: 800000 },
                          { 업종: '편의점', 소비금액: 600000 },
                          { 업종: '제과·디저트', 소비금액: 500000 },
                        ]}
                        margin={{ left: 30 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" tickFormatter={(v) => `${v / 1000}K`} />
                        <YAxis type="category" dataKey="업종" />
                        <Tooltip formatter={(v) => `${(v as number).toLocaleString()} 원`} />
                        <Bar dataKey="소비금액" fill="#805AD5" />
                      </BarChart>
                    </ResponsiveContainer>
                    <Text fontSize="sm" color="gray.500" mt={2}>
                      ※ 이 그래프는 선택된 타겟 고객 기준(예: <b>30대 남성</b>)으로 계산된 결과입니다.
                    </Text>
                  </Box>
                </ChartCard>

                {/* 3. 타겟 지역 vs 전체 지역 소비 비교 */}
                <ChartCard title="타겟 지역 vs 전체 지역 소비 비교">
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart
                      data={[
                        { 연령대: '20대', 타겟: 28, 전체: 20 },
                        { 연령대: '30대', 타겟: 32, 전체: 27 },
                        { 연령대: '40대', 타겟: 18, 전체: 22 },
                        { 연령대: '50대', 타겟: 10, 전체: 18 },
                      ]}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="연령대" />
                      <YAxis unit="%" />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="타겟" fill="#3182CE" />
                      <Bar dataKey="전체" fill="#CBD5E0" />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartCard>
              </VStack>
            </VStack>
          </TabPanel>

          {/* 경쟁사 분석 */}
          <TabPanel p={0} pt={6}>
            <ChartCard title="경쟁사 대비 성과 비교">
              {" "}
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart
                  data={competitorData}
                  margin={{ top: 20, right: 30, left: 30, bottom: 20 }}
                >
                  <PolarGrid />
                  <PolarAngleAxis
                    dataKey="metric"
                    tick={{ fill: "gray.600" }}
                  />
                  <Radar
                    name="우리"
                    dataKey="우리"
                    stroke="#3182CE"
                    fill="#3182CE"
                    fillOpacity={0.3}
                  />
                  <Radar
                    name="경쟁사1"
                    dataKey="경쟁사1"
                    stroke="#E53E3E"
                    fill="#E53E3E"
                    fillOpacity={0.2}
                  />
                  <Radar
                    name="경쟁사2"
                    dataKey="경쟁사2"
                    stroke="#38A169"
                    fill="#38A169"
                    fillOpacity={0.2}
                  />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </ChartCard>
          </TabPanel>

          {/* 트렌드 분석 */}
          <TabPanel p={0} pt={6}>
            <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} gap={6}>
              <Card bg={cardBg} borderColor={borderColor}>
                <CardHeader>
                  <Text fontSize="lg" fontWeight="bold">
                    인기 키워드 트렌드
                  </Text>
                </CardHeader>
                <CardBody>
                  <VStack spacing={4} align="stretch">
                    {trendingKeywords.map((item, index) => (
                      <Box key={index}>
                        <HStack justify="space-between">
                          <Text fontWeight="medium">#{item.keyword}</Text>
                          <HStack>
                            <Badge
                              colorScheme={
                                item.trend.includes("+") ? "green" : "red"
                              }
                              display="flex"
                              alignItems="center"
                              gap={1}
                            >
                              {item.trend.includes("+") ? (
                                <FaArrowUp />
                              ) : (
                                <FaArrowDown />
                              )}
                              {item.trend}
                            </Badge>
                          </HStack>
                        </HStack>
                        <Text fontSize="sm" color="gray.600">
                          월간 검색량: {item.searches.toLocaleString()}회
                        </Text>
                        <Divider mt={3} />
                      </Box>
                    ))}
                  </VStack>
                </CardBody>
              </Card>

              <Card bg={cardBg} borderColor={borderColor}>
                <CardHeader>
                  <Text fontSize="lg" fontWeight="bold">
                    AI 추천 인사이트
                  </Text>
                </CardHeader>
                <CardBody>
                  <VStack spacing={4} align="stretch">
                    <Box
                      p={4}
                      bg="blue.50"
                      borderRadius="md"
                      borderLeft="4px solid"
                      borderColor="blue.400"
                    >
                      <Text fontWeight="bold" color="blue.700" mb={2}>
                        📈 성과 향상 기회
                      </Text>
                      <Text fontSize="sm">
                        인스타그램 참여율이 20% 증가했습니다. 비슷한 콘텐츠를 더
                        자주 게시해보세요.
                      </Text>
                    </Box>

                    <Box
                      p={4}
                      bg="green.50"
                      borderRadius="md"
                      borderLeft="4px solid"
                      borderColor="green.400"
                    >
                      <Text fontWeight="bold" color="green.700" mb={2}>
                        🎯 타겟팅 최적화
                      </Text>
                      <Text fontSize="sm">
                        30-39세 고객층의 반응이 좋습니다. 이 연령대를 대상으로
                        한 콘텐츠를 늘려보세요.
                      </Text>
                    </Box>

                    <Box
                      p={4}
                      bg="orange.50"
                      borderRadius="md"
                      borderLeft="4px solid"
                      borderColor="orange.400"
                    >
                      <Text fontWeight="bold" color="orange.700" mb={2}>
                        ⚠️ 주의사항
                      </Text>
                      <Text fontSize="sm">
                        '리뷰' 키워드 트렌드가 하락 중입니다. 대체 키워드를
                        고려해보세요.
                      </Text>
                    </Box>

                    <Box
                      p={4}
                      bg="purple.50"
                      borderRadius="md"
                      borderLeft="4px solid"
                      borderColor="purple.400"
                    >
                      <Text fontWeight="bold" color="purple.700" mb={2}>
                        💡 콘텐츠 제안
                      </Text>
                      <Text fontSize="sm">
                        '친환경' 키워드가 급상승 중입니다. 관련 콘텐츠 제작을
                        고려해보세요.
                      </Text>
                    </Box>
                  </VStack>
                </CardBody>
              </Card>
            </Grid>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default AnalyticsPage;

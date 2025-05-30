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
            <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={6}>
              <ChartCard title="일별 성과 추이">
                {" "}
                <ResponsiveContainer width="100%" height={300}>
                  {" "}
                  <LineChart
                    data={performanceData}
                    margin={{ top: 5, right: 30, left: 20, bottom: 35 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="date"
                      label={{ value: "날짜", position: "bottom", offset: 20 }}
                    />
                    <YAxis
                      label={{
                        value: "수치",
                        angle: -90,
                        position: "insideLeft",
                        offset: 0,
                      }}
                    />
                    <Tooltip />
                    <Line
                      name="조회수"
                      type="monotone"
                      dataKey="views"
                      stroke="#3182CE"
                      strokeWidth={2}
                    />
                    <Line
                      name="좋아요"
                      type="monotone"
                      dataKey="likes"
                      stroke="#E53E3E"
                      strokeWidth={2}
                    />
                    <Line
                      name="클릭수"
                      type="monotone"
                      dataKey="clicks"
                      stroke="#38A169"
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </ChartCard>

              <ChartCard title="플랫폼별 성과">
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={platformData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {platformData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </ChartCard>
            </Grid>
          </TabPanel>

          {/* 고객 분석 */}
          <TabPanel p={0} pt={6}>
            <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} gap={6}>
              <ChartCard title="연령대별 고객 분포">
                {" "}
                <ResponsiveContainer width="100%" height={300}>
                  {" "}
                  <BarChart
                    data={audienceData}
                    margin={{ top: 5, right: 30, left: 20, bottom: 35 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="age"
                      label={{
                        value: "연령대",
                        position: "bottom",
                        offset: 20,
                      }}
                    />
                    <YAxis
                      label={{
                        value: "비율 (%)",
                        angle: -90,
                        position: "insideLeft",
                        offset: 0,
                      }}
                    />
                    <Tooltip />
                    <Bar name="고객 비율" dataKey="percentage" fill="#3182CE" />
                  </BarChart>
                </ResponsiveContainer>
              </ChartCard>

              <Card bg={cardBg} borderColor={borderColor}>
                <CardHeader>
                  <Text fontSize="lg" fontWeight="bold">
                    고객 세그먼트 상세
                  </Text>
                </CardHeader>
                <CardBody>
                  <VStack spacing={4} align="stretch">
                    {audienceData.map((item, index) => (
                      <Box key={index}>
                        <HStack justify="space-between" mb={2}>
                          <Text fontWeight="medium">{item.age}세</Text>
                          <Badge colorScheme="blue">{item.percentage}%</Badge>
                        </HStack>
                        <Progress value={item.percentage} colorScheme="blue" />
                        <Text fontSize="sm" color="gray.600" mt={1}>
                          {item.count.toLocaleString()}명
                        </Text>
                        <Divider mt={3} />
                      </Box>
                    ))}
                  </VStack>
                </CardBody>
              </Card>
            </Grid>
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

import React from "react";
import {
  Box,
  Grid,
  GridItem,
  Card,
  CardBody,
  Heading,
  Text,
  VStack,
  HStack,
  Badge,
  Progress,
  SimpleGrid,
  Icon,
  Button,
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
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  Legend,
} from "recharts";
import {
  FiTrendingUp,
  FiUsers,
  FiTarget,
  FiDollarSign,
  FiArrowUp,
  FiArrowDown,
  FiClock,
} from "react-icons/fi";

// 샘플 데이터
const performanceData = [
  { 시간대: "10~12시", 소비금액: 150000, 유동인구: 230 },
  { 시간대: "12~14시", 소비금액: 220000, 유동인구: 310 },
  { 시간대: "14~16시", 소비금액: 300000, 유동인구: 420 },
  { 시간대: "16~18시", 소비금액: 280000, 유동인구: 390 },
  { 시간대: "18~20시", 소비금액: 350000, 유동인구: 450 },
];

const audienceData = [
  { name: "20대", value: 35, color: "#8884d8" },
  { name: "30대", value: 30, color: "#82ca9d" },
  { name: "40대", value: 20, color: "#ffc658" },
  { name: "50대+", value: 15, color: "#ff7c7c" },
];

const contentPerformance = [
  { type: "블로그", 조회수: 12000, 참여율: 4.2 },
  { type: "인스타그램", 조회수: 8500, 참여율: 6.8 },
  { type: "유튜브", 조회수: 15000, 참여율: 3.9 },
  { type: "전단지", 조회수: 3200, 참여율: 2.1 },
];

const targetAudienceData = [
  { age: "20대", 남성: 15, 여성: 18 },
  { age: "30대", 남성: 25, 여성: 22 },
  { age: "40대", 남성: 10, 여성: 12 },
];

const DashboardPage: React.FC = () => {
  const cardBg = useColorModeValue("white", "gray.800");

  const StatCard = ({
    title,
    value,
    change,
    icon,
    isIncrease,
  }: {
    title: string;
    value: string;
    change: string;
    icon: any;
    isIncrease: boolean;
  }) => (
    <Card bg={cardBg} shadow="md">
      <CardBody>
        <HStack justify="space-between" mb={2}>
          <Icon as={icon} fontSize="24px" color="brand.500" />
          <Badge
            colorScheme={isIncrease ? "green" : "red"}
            variant="subtle"
            display="flex"
            alignItems="center"
            gap={1}
          >
            <Icon as={isIncrease ? FiArrowUp : FiArrowDown} fontSize="xs" />
            {change}
          </Badge>
        </HStack>
        <VStack align="start" spacing={1}>
          <Text fontSize="2xl" fontWeight="bold">
            {value}
          </Text>
          <Text fontSize="sm" color="gray.500">
            {title}
          </Text>
        </VStack>
      </CardBody>
    </Card>
  );

  return (
    <Box>
      <VStack align="stretch" spacing={6}>
        {/* 주요 지표 카드 */}
        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
          <StatCard
            title="주요 소비 타겟"
            value="30대 남성"
            change="▲"
            icon={FiTarget}
            isIncrease={true}
          />
          <StatCard
            title="소비 집중 시간대"
            value="14~16시"
            change="▲"
            icon={FiClock}
            isIncrease={true}
          />
          <StatCard
            title="타겟 지역"
            value="수지구 신봉동"
            change="NEW"
            icon={FiUsers}
            isIncrease={true}
          />
          <StatCard
            title="타겟 업종"
            value="카페·음료"
            change="↑ 12%"
            icon={FiDollarSign}
            isIncrease={true}
          />
        </SimpleGrid>
        <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} gap={6}>
          {/* 추천 액션 */}
          <GridItem>
            <Card bg={cardBg} shadow="md">
              <CardBody>
                <VStack align="stretch" spacing={4}>
                  <Heading size="md">추천 액션</Heading>
                  <VStack align="stretch" spacing={3}>
                    <Box
                      p={3}
                      bg="blue.50"
                      borderRadius="md"
                      borderLeft="4px"
                      borderColor="blue.400"
                    >
                      <Text fontSize="sm" fontWeight="500" color="blue.800">
                        📍 경기도 수지구 신봉동
                      </Text>
                      <Text fontSize="xs" color="blue.600" mt={1}>
                        30대 남성 고객이 가장 높은 소비량을 보였습니다. 이 타겟을 중심으로 마케팅을 기획하세요.
                      </Text>
                    </Box>
                    <Box
                      p={3}
                      bg="green.50"
                      borderRadius="md"
                      borderLeft="4px"
                      borderColor="green.400"
                    >
                      <Text fontSize="sm" fontWeight="500" color="green.800">
                        🕑 2~3시에 유동인구 급증
                      </Text>
                      <Text fontSize="xs" color="green.600" mt={1}>
                        해당 시간대에 이벤트 또는 프로모션을 집중적으로 진행해보세요.
                      </Text>
                    </Box>
                    <Box
                      p={3}
                      bg="orange.50"
                      borderRadius="md"
                      borderLeft="4px"
                      borderColor="orange.400"
                    >
                      <Text fontSize="sm" fontWeight="500" color="orange.800">
                        ⚠️ 경쟁 지역 내 신규 매장 증가
                      </Text>
                      <Text fontSize="xs" color="orange.600" mt={1}>
                        차별화된 서비스와 고객 혜택 전략을 수립해야 합니다.
                      </Text>
                    </Box>
                  </VStack>
                </VStack>
              </CardBody>
            </Card>
          </GridItem>

          {/* 목표 달성률 */}
          <GridItem>
            <Card bg={cardBg} shadow="md">
              <CardBody>
                <VStack align="stretch" spacing={4}>
                  <Heading size="md">이달의 목표</Heading>
                  <VStack align="stretch" spacing={4}>
                    <Box>
                      <HStack justify="space-between" mb={2}>
                        <Text fontSize="sm">방문자 수</Text>
                        <Text fontSize="sm" fontWeight="bold">
                          24,387 / 30,000
                        </Text>
                      </HStack>
                      <Progress
                        value={81}
                        colorScheme="blue"
                        borderRadius="md"
                      />
                    </Box>
                    <Box>
                      <HStack justify="space-between" mb={2}>
                        <Text fontSize="sm">전환율</Text>
                        <Text fontSize="sm" fontWeight="bold">
                          5.2% / 6.0%
                        </Text>
                      </HStack>
                      <Progress
                        value={87}
                        colorScheme="green"
                        borderRadius="md"
                      />
                    </Box>
                    <Box>
                      <HStack justify="space-between" mb={2}>
                        <Text fontSize="sm">콘텐츠 생성</Text>
                        <Text fontSize="sm" fontWeight="bold">
                          23 / 25
                        </Text>
                      </HStack>
                      <Progress
                        value={92}
                        colorScheme="purple"
                        borderRadius="md"
                      />
                    </Box>
                    <Box>
                      <HStack justify="space-between" mb={2}>
                        <Text fontSize="sm">수익 목표</Text>
                        <Text fontSize="sm" fontWeight="bold">
                          ₩1,234,567 / ₩2,000,000
                        </Text>
                      </HStack>
                      <Progress
                        value={62}
                        colorScheme="orange"
                        borderRadius="md"
                      />
                    </Box>
                  </VStack>
                </VStack>
              </CardBody>
            </Card>
          </GridItem>
        </Grid>
        {/* 차트 영역 */}
        <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={6}>
          {/* 성과 트렌드 */}
          <GridItem>
            <Card bg={cardBg} shadow="md">
              <CardBody>
                <VStack align="stretch" spacing={4}>
                  <Heading size="md">시간대별 소비 & 유동인구</Heading>
                  <Box h="300px">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart
                        data={performanceData}
                        margin={{ top: 5, right: 30, left: 20, bottom: 35 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                          dataKey="시간대"
                          label={{ value: "시간대", position: "bottom", offset: 20 }}
                        />
                        <YAxis
                          yAxisId="left"
                          label={{
                            value: "소비금액(천원)",
                            angle: -90,
                            position: "insideLeft",
                            offset: 5
                          }}
                          tickFormatter={(value) => (value / 1000).toLocaleString()}
                        />
                        <YAxis
                          yAxisId="right"
                          orientation="right"
                          label={{ value: "유동인구(명)", angle: 90, position: "insideRight" }}
                        />
                        <Tooltip />
                        <Line
                          yAxisId="left"
                          type="monotone"
                          dataKey="소비금액"
                          stroke="#3182ce"
                          strokeWidth={3}
                          dot={{ fill: "#3182ce", r: 4 }}
                        />
                        <Line
                          yAxisId="right"
                          type="monotone"
                          dataKey="유동인구"
                          stroke="#38a169"
                          strokeWidth={3}
                          dot={{ fill: "#38a169", r: 4 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </VStack>
              </CardBody>
            </Card>
          </GridItem>

          {/* 타겟 고객층 */}
          <GridItem>
            <Card bg={cardBg} shadow="md">
              <CardBody>
                <VStack align="stretch" spacing={4}>
                  <Heading size="md">타겟 고객 비율 (연령대 x 성별)</Heading>
                  <Text fontSize="xs" color="gray.500" mt={-2}>
                    ※ 상위 3개 연령대 기준
                  </Text>
                  <Box h="300px">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={targetAudienceData} margin={{ top: 20, right: 30, left: 20, bottom: 30 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="age" label={{ value: "연령대", position: "bottom", offset: 10 }} />
                        <YAxis label={{ value: "비율 (%)", angle: -90, position: "insideLeft" }} />
                        <Tooltip />
                        <Legend verticalAlign="top" align="right" />
                        <Bar dataKey="남성" stackId="a" fill="#3182CE" />
                        <Bar dataKey="여성" stackId="a" fill="#E53E3E" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </VStack>
              </CardBody>
            </Card>
          </GridItem>
        </Grid>

        {/* 콘텐츠 성과 */}
        <Card bg={cardBg} shadow="md">
          <CardBody>
            <VStack align="stretch" spacing={4}>
              <HStack justify="space-between">
                <Heading size="md">콘텐츠 성과</Heading>
                <Button size="sm" variant="outline" colorScheme="brand">
                  상세 보기
                </Button>
              </HStack>
              <Box h="250px">
                <ResponsiveContainer width="100%" height="100%">
                  {" "}
                  <BarChart
                    data={contentPerformance}
                    margin={{ top: 5, right: 30, left: 20, bottom: 35 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="type"
                      label={{
                        value: "콘텐츠 유형",
                        position: "bottom",
                        offset: 20,
                      }}
                    />
                    <YAxis
                      yAxisId="left"
                      label={{
                        value: "조회수",
                        angle: -90,
                        position: "insideLeft",
                        offset: -5,
                      }}
                    />
                    <YAxis
                      yAxisId="right"
                      orientation="right"
                      label={{
                        value: "참여율 (%)",
                        angle: 90,
                        position: "insideRight",
                        offset: 10,
                      }}
                    />
                    <Tooltip />
                    <Bar
                      yAxisId="left"
                      dataKey="조회수"
                      fill="#3182ce"
                      radius={[4, 4, 0, 0]}
                    />
                    <Bar
                      yAxisId="right"
                      dataKey="참여율"
                      fill="#38a169"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </VStack>
          </CardBody>
        </Card>

        {/* 최근 인사이트 */}
      </VStack>
    </Box>
  );
};

export default DashboardPage;

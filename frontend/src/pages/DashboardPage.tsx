import React from 'react'
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
} from '@chakra-ui/react'
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
} from 'recharts'
import {
  FiTrendingUp,
  FiUsers,
  FiTarget,
  FiDollarSign,
  FiArrowUp,
  FiArrowDown,
} from 'react-icons/fi'

// 샘플 데이터
const performanceData = [
  { month: '1월', 방문자: 2400, 전환율: 4.2 },
  { month: '2월', 방문자: 1398, 전환율: 3.8 },
  { month: '3월', 방문자: 9800, 전환율: 5.1 },
  { month: '4월', 방문자: 3908, 전환율: 4.7 },
  { month: '5월', 방문자: 4800, 전환율: 6.2 },
  { month: '6월', 방문자: 3800, 전환율: 5.9 },
]

const audienceData = [
  { name: '20대', value: 35, color: '#8884d8' },
  { name: '30대', value: 30, color: '#82ca9d' },
  { name: '40대', value: 20, color: '#ffc658' },
  { name: '50대+', value: 15, color: '#ff7c7c' },
]

const contentPerformance = [
  { type: '블로그', 조회수: 12000, 참여율: 4.2 },
  { type: '인스타그램', 조회수: 8500, 참여율: 6.8 },
  { type: '유튜브', 조회수: 15000, 참여율: 3.9 },
  { type: '전단지', 조회수: 3200, 참여율: 2.1 },
]

const DashboardPage: React.FC = () => {
  const cardBg = useColorModeValue('white', 'gray.800')

  const StatCard = ({ 
    title, 
    value, 
    change, 
    icon, 
    isIncrease 
  }: {
    title: string
    value: string
    change: string
    icon: any
    isIncrease: boolean
  }) => (
    <Card bg={cardBg} shadow="md">
      <CardBody>
        <HStack justify="space-between" mb={2}>
          <Icon as={icon} fontSize="24px" color="brand.500" />
          <Badge
            colorScheme={isIncrease ? 'green' : 'red'}
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
  )

  return (
    <Box>
      <VStack align="stretch" spacing={6}>
        {/* 주요 지표 카드 */}
        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
          <StatCard
            title="총 방문자"
            value="24,387"
            change="12.5%"
            icon={FiUsers}
            isIncrease={true}
          />
          <StatCard
            title="전환율"
            value="5.2%"
            change="8.1%"
            icon={FiTarget}
            isIncrease={true}
          />
          <StatCard
            title="수익"
            value="₩1,234,567"
            change="15.3%"
            icon={FiDollarSign}
            isIncrease={true}
          />
          <StatCard
            title="참여율"
            value="4.8%"
            change="2.4%"
            icon={FiTrendingUp}
            isIncrease={false}
          />
        </SimpleGrid>

        {/* 차트 영역 */}
        <Grid templateColumns={{ base: '1fr', lg: '2fr 1fr' }} gap={6}>
          {/* 성과 트렌드 */}
          <GridItem>
            <Card bg={cardBg} shadow="md">
              <CardBody>
                <VStack align="stretch" spacing={4}>
                  <Heading size="md">성과 트렌드</Heading>
                  <Box h="300px">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={performanceData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis yAxisId="left" />
                        <YAxis yAxisId="right" orientation="right" />
                        <Tooltip />
                        <Line
                          yAxisId="left"
                          type="monotone"
                          dataKey="방문자"
                          stroke="#3182ce"
                          strokeWidth={3}
                          dot={{ fill: '#3182ce', strokeWidth: 2, r: 4 }}
                        />
                        <Line
                          yAxisId="right"
                          type="monotone"
                          dataKey="전환율"
                          stroke="#38a169"
                          strokeWidth={3}
                          dot={{ fill: '#38a169', strokeWidth: 2, r: 4 }}
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
                  <Heading size="md">타겟 고객층</Heading>
                  <Box h="300px">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={audienceData}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={100}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {audienceData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                  <VStack align="stretch" spacing={2}>
                    {audienceData.map((item, index) => (
                      <HStack key={index} justify="space-between">
                        <HStack>
                          <Box
                            w={3}
                            h={3}
                            bg={item.color}
                            borderRadius="full"
                          />
                          <Text fontSize="sm">{item.name}</Text>
                        </HStack>
                        <Text fontSize="sm" fontWeight="bold">
                          {item.value}%
                        </Text>
                      </HStack>
                    ))}
                  </VStack>
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
                  <BarChart data={contentPerformance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="type" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
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
        <Grid templateColumns={{ base: '1fr', lg: '1fr 1fr' }} gap={6}>
          {/* 추천 액션 */}
          <GridItem>
            <Card bg={cardBg} shadow="md">
              <CardBody>
                <VStack align="stretch" spacing={4}>
                  <Heading size="md">추천 액션</Heading>
                  <VStack align="stretch" spacing={3}>
                    <Box p={3} bg="blue.50" borderRadius="md" borderLeft="4px" borderColor="blue.400">
                      <Text fontSize="sm" fontWeight="500" color="blue.800">
                        20대 여성 고객층 증가 감지
                      </Text>
                      <Text fontSize="xs" color="blue.600" mt={1}>
                        인스타그램 마케팅을 강화하여 이 트렌드를 활용하세요.
                      </Text>
                    </Box>
                    <Box p={3} bg="green.50" borderRadius="md" borderLeft="4px" borderColor="green.400">
                      <Text fontSize="sm" fontWeight="500" color="green.800">
                        점심시간대 방문자 급증
                      </Text>
                      <Text fontSize="xs" color="green.600" mt={1}>
                        점심 메뉴 관련 콘텐츠를 더 많이 생성해보세요.
                      </Text>
                    </Box>
                    <Box p={3} bg="orange.50" borderRadius="md" borderLeft="4px" borderColor="orange.400">
                      <Text fontSize="sm" fontWeight="500" color="orange.800">
                        경쟁사 신규 진입
                      </Text>
                      <Text fontSize="xs" color="orange.600" mt={1}>
                        차별화 전략 수립이 필요합니다.
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
                      <Progress value={81} colorScheme="blue" borderRadius="md" />
                    </Box>
                    <Box>
                      <HStack justify="space-between" mb={2}>
                        <Text fontSize="sm">전환율</Text>
                        <Text fontSize="sm" fontWeight="bold">
                          5.2% / 6.0%
                        </Text>
                      </HStack>
                      <Progress value={87} colorScheme="green" borderRadius="md" />
                    </Box>
                    <Box>
                      <HStack justify="space-between" mb={2}>
                        <Text fontSize="sm">콘텐츠 생성</Text>
                        <Text fontSize="sm" fontWeight="bold">
                          23 / 25
                        </Text>
                      </HStack>
                      <Progress value={92} colorScheme="purple" borderRadius="md" />
                    </Box>
                    <Box>
                      <HStack justify="space-between" mb={2}>
                        <Text fontSize="sm">수익 목표</Text>
                        <Text fontSize="sm" fontWeight="bold">
                          ₩1,234,567 / ₩2,000,000
                        </Text>
                      </HStack>
                      <Progress value={62} colorScheme="orange" borderRadius="md" />
                    </Box>
                  </VStack>
                </VStack>
              </CardBody>
            </Card>
          </GridItem>
        </Grid>
      </VStack>
    </Box>
  )
}

export default DashboardPage

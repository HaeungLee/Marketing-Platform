import React from 'react'
import { Box, VStack, Link, Icon, Text, useColorModeValue } from '@chakra-ui/react'
import { Link as RouterLink, useLocation } from 'react-router-dom'
import { 
  FiHome, 
  FiBarChart3, 
  FiEdit3, 
  FiSettings, 
  FiTarget,
  FiTrendingUp 
} from 'react-icons/fi'

const menuItems = [
  { path: '/app', icon: FiHome, label: '대시보드' },
  { path: '/app/business/setup', icon: FiTarget, label: '비즈니스 설정' },
  { path: '/app/content', icon: FiEdit3, label: '콘텐츠 생성' },
  { path: '/app/analytics', icon: FiBarChart3, label: '분석 & 인사이트' },
  { path: '/app/settings', icon: FiSettings, label: '설정' },
]

const Sidebar: React.FC = () => {
  const location = useLocation()
  const bg = useColorModeValue('white', 'gray.800')
  const borderColor = useColorModeValue('gray.200', 'gray.700')

  return (
    <Box
      w="280px"
      h="100vh"
      bg={bg}
      borderRight="1px"
      borderColor={borderColor}
      boxShadow="sm"
    >
      {/* 로고 영역 */}
      <Box p={6} borderBottom="1px" borderColor={borderColor}>
        <Text fontSize="xl" fontWeight="bold" color="brand.500">
          🚀 AI 마케팅 플랫폼
        </Text>
        <Text fontSize="sm" color="gray.500" mt={1}>
          스마트 마케팅 솔루션
        </Text>
      </Box>

      {/* 메뉴 아이템들 */}
      <VStack align="stretch" p={4} spacing={2}>
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path
          
          return (
            <Link
              key={item.path}
              as={RouterLink}
              to={item.path}
              display="flex"
              alignItems="center"
              p={3}
              borderRadius="lg"
              bg={isActive ? 'brand.50' : 'transparent'}
              color={isActive ? 'brand.600' : 'gray.600'}
              fontWeight={isActive ? '600' : '400'}
              _hover={{
                bg: isActive ? 'brand.100' : 'gray.100',
                color: isActive ? 'brand.700' : 'gray.800',
                transform: 'translateX(4px)',
              }}
              transition="all 0.2s"
              textDecoration="none"
            >
              <Icon as={item.icon} mr={3} fontSize="lg" />
              <Text fontSize="sm">{item.label}</Text>
            </Link>
          )
        })}
      </VStack>

      {/* 하단 정보 */}
      <Box position="absolute" bottom={4} left={4} right={4}>
        <Box p={3} bg="gray.50" borderRadius="lg">
          <Text fontSize="xs" color="gray.500" textAlign="center">
            버전 1.0.0 | 데모 모드
          </Text>
          <Text fontSize="xs" color="gray.400" textAlign="center" mt={1}>
            공모전용 프로토타입
          </Text>
        </Box>
      </Box>
    </Box>
  )
}

export default Sidebar

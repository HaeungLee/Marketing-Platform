import React from 'react'
import { Outlet } from 'react-router-dom'
import { Box, Flex } from '@chakra-ui/react'
import Sidebar from './Sidebar'
import Header from './Header'

const Layout: React.FC = () => {
  return (
    <Flex h="100vh">
      {/* 사이드바 */}
      <Sidebar />
      
      {/* 메인 콘텐츠 영역 */}
      <Box flex="1" bg="gray.50">
        <Header />
        <Box p={6} overflow="auto" h="calc(100vh - 80px)">
          <Outlet />
        </Box>
      </Box>
    </Flex>
  )
}

export default Layout

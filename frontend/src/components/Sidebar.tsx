import React, { useState } from "react";
import {
  Box,
  VStack,
  Link,
  Icon,
  Text,
  useColorModeValue,
  IconButton,
  Tooltip,
  Flex,
} from "@chakra-ui/react";
import { Link as RouterLink, useLocation } from "react-router-dom";
import {
  FiHome,
  FiBarChart,
  FiEdit3,
  FiSettings,
  FiTarget,
  FiTrendingUp,
  FiChevronLeft,
  FiChevronRight,
  FiFileText,
} from "react-icons/fi";

const menuItems = [
  { path: "/app", icon: FiHome, label: "대시보드" },
  { path: "/app/business/setup", icon: FiTarget, label: "비즈니스 설정" },
  { path: "/app/content", icon: FiEdit3, label: "콘텐츠 생성" },
  { path: "/app/flyer", icon: FiFileText, label: "전단지 생성" },
  { path: "/app/population", icon: FiTrendingUp, label: "인구 통계" },
  { path: "/app/analytics", icon: FiBarChart, label: "분석 & 인사이트" },
  { path: "/app/settings", icon: FiSettings, label: "설정" },
];

const Sidebar: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const location = useLocation();
  const bg = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.700");
  const buttonBg = useColorModeValue("white", "gray.700");
  const buttonHoverBg = useColorModeValue("gray.50", "gray.600");

  return (
    <Box position="relative">
      <Box
        w={isCollapsed ? "80px" : "280px"}
        h="100vh"
        bg={bg}
        borderRight="1px"
        borderColor={borderColor}
        boxShadow={isCollapsed ? "sm" : "lg"}
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
        overflow="hidden"
      >
        {/* 로고 영역 */}
        <Box
          p={isCollapsed ? 4 : 6}
          borderBottom="1px"
          borderColor={borderColor}
          textAlign={isCollapsed ? "center" : "left"}
          transition="all 0.3s"
        >
          <Link as={RouterLink} to="/" _hover={{ textDecoration: "none" }}>
            <Text
              fontSize={isCollapsed ? "2xl" : "xl"}
              fontWeight="bold"
              color="brand.500"
              cursor="pointer"
              transition="all 0.3s"
            >
              {isCollapsed ? "🚀" : "🚀 AI 마케팅 플랫폼"}
            </Text>
          </Link>
        </Box>

        {/* 메뉴 아이템들 */}
        <VStack align="stretch" p={4} spacing={2}>
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path;

            return (
              <Tooltip
                key={item.path}
                label={isCollapsed ? item.label : ""}
                placement="right"
                hasArrow
                bg="brand.500"
                openDelay={200}
              >
                <Link
                  as={RouterLink}
                  to={item.path}
                  display="flex"
                  alignItems="center"
                  p={3}
                  borderRadius="xl"
                  bg={isActive ? "brand.50" : "transparent"}
                  color={isActive ? "brand.500" : "gray.600"}
                  fontWeight={isActive ? "600" : "400"}
                  _hover={{
                    bg: isActive ? "brand.100" : "gray.100",
                    color: isActive ? "brand.600" : "gray.800",
                    transform: "translateX(4px)",
                  }}
                  transition="all 0.2s ease"
                  textDecoration="none"
                >
                  <Icon
                    as={item.icon}
                    fontSize={isCollapsed ? "xl" : "lg"}
                    transition="all 0.2s"
                  />
                  {!isCollapsed && (
                    <Text
                      fontSize="sm"
                      ml={3}
                      opacity="1"
                      transition="all 0.2s"
                    >
                      {item.label}
                    </Text>
                  )}
                </Link>
              </Tooltip>
            );
          })}
        </VStack>

        {/* 하단 정보 */}
        <Box
          position="absolute"
          bottom={4}
          left={4}
          right={4}
          opacity={isCollapsed ? 0 : 1}
          transform={isCollapsed ? "translateX(-20px)" : "translateX(0)"}
          transition="all 0.3s"
        >
          <Box p={3} bg="gray.50" borderRadius="xl" boxShadow="sm">
            <Text fontSize="xs" color="gray.500" textAlign="center">
              버전 1.0.0 | 데모 모드
            </Text>
            <Text fontSize="xs" color="gray.400" textAlign="center" mt={1}>
              공모전용 프로토타입
            </Text>
          </Box>
        </Box>
      </Box>

      {/* 토글 버튼 */}
      <IconButton
        aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        icon={isCollapsed ? <FiChevronRight /> : <FiChevronLeft />}
        position="absolute"
        top="40%"
        right={isCollapsed ? "-12px" : "-16px"}
        transform="translateY(-50%)"
        borderRadius="full"
        bg={buttonBg}
        color="brand.500"
        size="sm"
        boxShadow="lg"
        border="2px solid"
        borderColor="brand.100"
        _hover={{
          bg: buttonHoverBg,
          transform: "translateY(-50%) scale(1.1)",
        }}
        _active={{
          bg: buttonHoverBg,
          transform: "translateY(-50%) scale(0.95)",
        }}
        onClick={() => setIsCollapsed(!isCollapsed)}
        zIndex="1"
        transition="all 0.2s"
      />
    </Box>
  );
};

export default Sidebar;

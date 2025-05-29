import React from "react";
import {
  Box,
  Flex,
  Text,
  Button,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  Badge,
  useColorModeValue,
} from "@chakra-ui/react";
import { FiBell, FiChevronDown, FiUser, FiLogOut } from "react-icons/fi";

const Header: React.FC = () => {
  const bg = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.700");

  return (
    <Box
      h="80px"
      bg={bg}
      borderBottom="1px"
      borderColor={borderColor}
      px={6}
      py={4}
    >
      <Flex justify="space-between" align="center" h="100%">
        {/* 페이지 타이틀 */}
        <Box>
          <Text fontSize="2xl" fontWeight="bold" color="gray.800">
            대시 보드
          </Text>
          <Text fontSize="sm" color="gray.500">
            비즈니스 성과와 인사이트를 한눈에 확인하세요
          </Text>
        </Box>

        {/* 우측 액션 영역 */}
        <Flex align="center" gap={4}>
          {/* 알림 버튼 */}
          <Box position="relative">
            <Button
              variant="ghost"
              size="sm"
              leftIcon={<FiBell />}
              colorScheme="gray"
            >
              알림
            </Button>
            <Badge
              position="absolute"
              top="-1"
              right="-1"
              colorScheme="red"
              borderRadius="full"
              px={2}
              fontSize="xs"
            >
              3
            </Badge>
          </Box>

          {/* 사용자 메뉴 */}
          <Menu>
            <MenuButton
              as={Button}
              variant="ghost"
              rightIcon={<FiChevronDown />}
              size="sm"
            >
              <Flex align="center" gap={3}>
                <Avatar size="sm" name="데모 사용자" />
                <Box textAlign="left">
                  <Text fontSize="sm" fontWeight="500">
                    데모 사용자
                  </Text>
                  <Text fontSize="xs" color="gray.500">
                    demo@example.com
                  </Text>
                </Box>
              </Flex>
            </MenuButton>
            <MenuList>
              <MenuItem icon={<FiUser />}>프로필 설정</MenuItem>
              <MenuDivider />
              <MenuItem icon={<FiLogOut />} color="red.500">
                로그아웃
              </MenuItem>
            </MenuList>
          </Menu>
        </Flex>
      </Flex>
    </Box>
  );
};

export default Header;

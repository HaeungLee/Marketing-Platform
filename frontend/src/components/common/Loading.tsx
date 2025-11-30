import React from 'react';
import {
  Spinner,
  Center,
  VStack,
  Text,
  Box,
  useColorModeValue,
} from '@chakra-ui/react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  text?: string;
  fullScreen?: boolean;
}

/**
 * 로딩 스피너 컴포넌트
 */
export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'lg',
  text = '로딩 중...',
  fullScreen = false,
}) => {
  const content = (
    <VStack spacing={4}>
      <Spinner
        thickness="4px"
        speed="0.65s"
        emptyColor="gray.200"
        color="blue.500"
        size={size}
      />
      {text && <Text color="gray.500">{text}</Text>}
    </VStack>
  );

  if (fullScreen) {
    return (
      <Center h="100vh" w="100vw" position="fixed" top={0} left={0} bg="white" zIndex={9999}>
        {content}
      </Center>
    );
  }

  return <Center py={10}>{content}</Center>;
};

interface PageLoadingProps {
  text?: string;
}

/**
 * 페이지 로딩 컴포넌트
 */
export const PageLoading: React.FC<PageLoadingProps> = ({ text = '페이지를 불러오는 중...' }) => {
  return (
    <Center h="calc(100vh - 200px)">
      <LoadingSpinner size="xl" text={text} />
    </Center>
  );
};

interface SkeletonCardProps {
  count?: number;
}

/**
 * 스켈레톤 카드 컴포넌트
 */
export const SkeletonCard: React.FC<SkeletonCardProps> = ({ count = 1 }) => {
  const bgColor = useColorModeValue('gray.100', 'gray.700');
  
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <Box
          key={index}
          bg={bgColor}
          borderRadius="lg"
          p={6}
          animation="pulse 2s infinite"
        >
          <Box h="20px" bg="gray.200" borderRadius="md" mb={4} w="60%" />
          <Box h="32px" bg="gray.200" borderRadius="md" mb={2} w="40%" />
          <Box h="16px" bg="gray.200" borderRadius="md" w="80%" />
        </Box>
      ))}
    </>
  );
};

export default { LoadingSpinner, PageLoading, SkeletonCard };

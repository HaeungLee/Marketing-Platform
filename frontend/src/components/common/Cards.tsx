import React from 'react';
import {
  Card,
  CardBody,
  CardHeader,
  Heading,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Box,
  Flex,
  Icon,
  useColorModeValue,
} from '@chakra-ui/react';
import { IconType } from 'react-icons';

interface StatCardProps {
  label: string;
  value: string | number;
  helpText?: string;
  icon?: IconType;
  trend?: 'increase' | 'decrease';
  trendValue?: string;
  colorScheme?: string;
}

/**
 * 통계 카드 컴포넌트
 * 대시보드에서 KPI나 주요 지표를 표시할 때 사용
 */
export const StatCard: React.FC<StatCardProps> = ({
  label,
  value,
  helpText,
  icon,
  trend,
  trendValue,
  colorScheme = 'blue',
}) => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const iconBgColor = useColorModeValue(`${colorScheme}.50`, `${colorScheme}.900`);
  const iconColor = useColorModeValue(`${colorScheme}.500`, `${colorScheme}.200`);

  return (
    <Card bg={bgColor} borderWidth="1px" borderColor={borderColor} shadow="sm">
      <CardBody>
        <Flex justify="space-between" align="flex-start">
          <Stat>
            <StatLabel color="gray.500" fontSize="sm">
              {label}
            </StatLabel>
            <StatNumber fontSize="2xl" fontWeight="bold">
              {typeof value === 'number' ? value.toLocaleString() : value}
            </StatNumber>
            {(helpText || trend) && (
              <StatHelpText mb={0}>
                {trend && <StatArrow type={trend} />}
                {trendValue || helpText}
              </StatHelpText>
            )}
          </Stat>
          {icon && (
            <Box
              p={3}
              bg={iconBgColor}
              borderRadius="lg"
            >
              <Icon as={icon} boxSize={6} color={iconColor} />
            </Box>
          )}
        </Flex>
      </CardBody>
    </Card>
  );
};

interface DataCardProps {
  title: string;
  children: React.ReactNode;
  headerAction?: React.ReactNode;
  isLoading?: boolean;
  minHeight?: string;
}

/**
 * 데이터 카드 컴포넌트
 * 차트나 테이블 등 데이터를 감싸는 컨테이너로 사용
 */
export const DataCard: React.FC<DataCardProps> = ({
  title,
  children,
  headerAction,
  isLoading = false,
  minHeight,
}) => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  return (
    <Card bg={bgColor} borderWidth="1px" borderColor={borderColor} shadow="sm" minH={minHeight}>
      <CardHeader pb={2}>
        <Flex justify="space-between" align="center">
          <Heading size="md">{title}</Heading>
          {headerAction}
        </Flex>
      </CardHeader>
      <CardBody pt={2}>
        {isLoading ? (
          <Flex justify="center" align="center" minH="200px">
            <Box>로딩 중...</Box>
          </Flex>
        ) : (
          children
        )}
      </CardBody>
    </Card>
  );
};

interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: IconType;
  action?: React.ReactNode;
}

/**
 * 빈 상태 컴포넌트
 * 데이터가 없을 때 표시
 */
export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  icon,
  action,
}) => {
  const textColor = useColorModeValue('gray.500', 'gray.400');

  return (
    <Flex
      direction="column"
      align="center"
      justify="center"
      py={10}
      px={6}
      textAlign="center"
    >
      {icon && (
        <Icon as={icon} boxSize={12} color={textColor} mb={4} />
      )}
      <Heading size="md" mb={2}>
        {title}
      </Heading>
      {description && (
        <Box color={textColor} mb={4}>
          {description}
        </Box>
      )}
      {action}
    </Flex>
  );
};

export default { StatCard, DataCard, EmptyState };

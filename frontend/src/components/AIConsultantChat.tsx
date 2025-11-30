import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Button,
  VStack,
  HStack,
  Text,
  Input,
  useColorModeValue,
  Avatar,
  Badge,
  useToast,
  Spinner,
  IconButton,
  Collapse,
  useDisclosure,
  Card,
  CardBody,
  Flex,
  Wrap,
  WrapItem,
} from '@chakra-ui/react';
import {
  FiSend,
  FiX,
  FiMaximize2,
  FiPlus,
  FiMessageSquare,
  FiMinimize2,
} from 'react-icons/fi';

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

interface ConsultationContext {
  businessType?: string;
  region?: string;
  budget?: string;
}

// 빠른 질문 목록
const QUICK_QUESTIONS = [
  { label: '🏪 상권 분석', question: '우리 동네 상권 분석 방법을 알려주세요' },
  { label: '🚀 창업 준비', question: '카페 창업 준비는 어떻게 해야 하나요?' },
  { label: '📢 마케팅', question: '소상공인 마케팅 방법을 추천해주세요' },
  { label: '💰 지원사업', question: '소상공인 정부 지원사업에는 무엇이 있나요?' },
];

const AIConsultantChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      type: 'ai',
      content: `안녕하세요! 👋 소상공인 AI 상담사입니다.

**빠른 도움:**
• 상권 분석 • 창업 전략 
• 마케팅 방안 • 정부 지원

무엇을 도와드릴까요?`,
      timestamp: new Date()
    }
  ]);
  
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [context, setContext] = useState<ConsultationContext>({});
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  
  const { isOpen, onOpen, onClose } = useDisclosure();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatRef = useRef<HTMLDivElement>(null);
  const toast = useToast();

  const bg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const messageBg = useColorModeValue('gray.50', 'gray.700');
  const userMessageBg = useColorModeValue('blue.500', 'blue.600');
  const headerBg = useColorModeValue('blue.50', 'blue.900');

  // 메시지 스크롤 자동 이동
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 외부 클릭 시 닫기
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (chatRef.current && !chatRef.current.contains(event.target as Node)) {
        if (isOpen && !isFullscreen) {
          onClose();
        }
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen, onClose, isFullscreen]);

  // 채팅창이 열려있지 않을 때 새 메시지가 오면 읽지 않은 메시지 카운트 증가
  useEffect(() => {
    if (!isOpen && messages.length > 1) { // 환영 메시지 제외
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.type === 'ai') {
        setUnreadCount(prev => prev + 1);
      }
    } else if (isOpen) {
      setUnreadCount(0);
    }
  }, [messages, isOpen]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || loading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      // AI 상담 API 호출
      const response = await fetch('/api/v1/consultation/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: inputMessage,
          business_type: context.businessType,
          region: context.region,
          budget: context.budget
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        type: 'ai',
        content: data.answer,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);

    } catch (error) {
      console.error('상담 요청 실패:', error);
      
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        type: 'ai',
        content: '죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      
      toast({
        title: '상담 요청 실패',
        description: '네트워크 연결을 확인하고 다시 시도해 주세요.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  };

  const startNewConversation = () => {
    setMessages([
      {
        id: 'welcome',
        type: 'ai',
        content: `안녕하세요! 👋 소상공인 AI 상담사입니다.

**빠른 도움:**
• 상권 분석 • 창업 전략 
• 마케팅 방안 • 정부 지원

무엇을 도와드릴까요?`,
        timestamp: new Date()
      }
    ]);
    setContext({});
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('ko-KR', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // 간단한 마크다운 렌더링 (볼드, 불릿 등)
  const renderFormattedText = (text: string) => {
    // **텍스트** → 볼드
    // • 또는 - 로 시작하는 줄 → 불릿 포인트
    const lines = text.split('\n');
    
    return lines.map((line, idx) => {
      // 볼드 처리
      const parts = line.split(/(\*\*[^*]+\*\*)/g);
      const formattedParts = parts.map((part, partIdx) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return (
            <Text as="strong" key={partIdx} fontWeight="bold">
              {part.slice(2, -2)}
            </Text>
          );
        }
        return part;
      });

      // 불릿 포인트 스타일
      const isBullet = line.trim().startsWith('•') || line.trim().startsWith('-');
      
      return (
        <Text 
          key={idx} 
          fontSize="sm"
          pl={isBullet ? 2 : 0}
          mb={0.5}
        >
          {formattedParts}
        </Text>
      );
    });
  };

  return (
    <>
      {/* AI 상담 버튼 */}
      <Box position="relative">
        <Button
          variant="ghost"
          size="sm"
          leftIcon={<FiMessageSquare />}
          colorScheme="blue"
          onClick={onOpen}
        >
          AI 상담
        </Button>
        {unreadCount > 0 && (
          <Badge
            position="absolute"
            top="-1"
            right="-1"
            colorScheme="red"
            borderRadius="full"
            px={2}
            fontSize="xs"
          >
            {unreadCount > 9 ? '9+' : unreadCount}
          </Badge>
        )}
      </Box>

      {/* 채팅창 */}
      {isOpen && (
        <Box
          ref={chatRef}
          position="fixed"
          bottom={isFullscreen ? 0 : 4}
          right={isFullscreen ? 0 : 4}
          width={isFullscreen ? '100vw' : '400px'}
          height={isFullscreen ? '100vh' : '600px'}
          bg={bg}
          borderRadius={isFullscreen ? 0 : 'xl'}
          boxShadow="2xl"
          border="1px"
          borderColor={borderColor}
          zIndex={1000}
          display="flex"
          flexDirection="column"
        >
          {/* 헤더 */}
          <Flex
            p={4}
            borderBottom="1px"
            borderColor={borderColor}
            borderTopRadius={isFullscreen ? 0 : 'xl'}
            align="center"
            justify="space-between"
            bg={headerBg}
          >
            <HStack>
              <Avatar size="sm" name="AI 상담사" bg="blue.500" />
              <VStack align="start" spacing={0}>
                <Text fontWeight="semibold" fontSize="sm">
                  AI 상담사
                </Text>
                <Text fontSize="xs" color="gray.500">
                  온라인
                </Text>
              </VStack>
            </HStack>
            
            <HStack spacing={1}>
              <IconButton
                aria-label="새 대화"
                icon={<FiPlus />}
                size="sm"
                variant="ghost"
                onClick={startNewConversation}
                title="새 대화 시작"
              />
              <IconButton
                aria-label={isFullscreen ? "창 모드" : "전체화면"}
                icon={isFullscreen ? <FiMinimize2 /> : <FiMaximize2 />}
                size="sm"
                variant="ghost"
                onClick={toggleFullscreen}
                title={isFullscreen ? "창 모드로 전환" : "전체화면으로 전환"}
              />
              <IconButton
                aria-label="닫기"
                icon={<FiX />}
                size="sm"
                variant="ghost"
                onClick={onClose}
                title="채팅창 닫기"
              />
            </HStack>
          </Flex>

          {/* 메시지 영역 */}
          <Box
            flex="1"
            overflowY="auto"
            p={4}
            css={{
              '&::-webkit-scrollbar': {
                width: '4px',
              },
              '&::-webkit-scrollbar-track': {
                backgroundColor: 'transparent',
              },
              '&::-webkit-scrollbar-thumb': {
                backgroundColor: 'rgba(0,0,0,0.1)',
                borderRadius: '4px',
              },
            }}
          >
            <VStack spacing={3} align="stretch">
              {messages.map((message) => (
                <Box key={message.id}>
                  <Flex
                    justify={message.type === 'user' ? 'flex-end' : 'flex-start'}
                    mb={1}
                  >
                    <Box
                      maxW="85%"
                      bg={message.type === 'user' ? userMessageBg : messageBg}
                      color={message.type === 'user' ? 'white' : 'inherit'}
                      p={3}
                      borderRadius="lg"
                      borderBottomRightRadius={message.type === 'user' ? 'sm' : 'lg'}
                      borderBottomLeftRadius={message.type === 'ai' ? 'sm' : 'lg'}
                    >
                      {message.type === 'ai' ? (
                        <Box>{renderFormattedText(message.content)}</Box>
                      ) : (
                        <Text fontSize="sm" whiteSpace="pre-wrap">
                          {message.content}
                        </Text>
                      )}
                    </Box>
                  </Flex>
                  <Text
                    fontSize="xs"
                    color="gray.500"
                    textAlign={message.type === 'user' ? 'right' : 'left'}
                  >
                    {formatTime(message.timestamp)}
                  </Text>
                </Box>
              ))}
              
              {loading && (
                <Flex justify="flex-start" mb={1}>
                  <Box bg={messageBg} p={3} borderRadius="lg" borderBottomLeftRadius="sm">
                    <HStack>
                      <Spinner size="sm" />
                      <Text fontSize="sm">상담사가 답변을 준비하고 있습니다...</Text>
                    </HStack>
                  </Box>
                </Flex>
              )}
              
              <div ref={messagesEndRef} />
            </VStack>
          </Box>

          {/* 입력 영역 */}
          <Box
            p={4}
            borderTop="1px"
            borderColor={borderColor}
            borderBottomRadius={isFullscreen ? 0 : 'xl'}
          >
            {/* 빠른 질문 버튼 - 메시지가 환영 메시지만 있을 때 표시 */}
            {messages.length === 1 && (
              <Wrap spacing={2} mb={3}>
                {QUICK_QUESTIONS.map((q, idx) => (
                  <WrapItem key={idx}>
                    <Button
                      size="xs"
                      variant="outline"
                      colorScheme="blue"
                      onClick={() => {
                        setInputMessage(q.question);
                      }}
                      isDisabled={loading}
                    >
                      {q.label}
                    </Button>
                  </WrapItem>
                ))}
              </Wrap>
            )}
            
            <HStack spacing={2}>
              <Input
                value={inputMessage}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInputMessage(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="궁금한 것을 물어보세요..."
                disabled={loading}
              />
              <IconButton
                aria-label="전송"
                icon={<FiSend />}
                colorScheme="blue"
                onClick={sendMessage}
                isLoading={loading}
                disabled={!inputMessage.trim() || loading}
              />
            </HStack>
            
            <Text fontSize="xs" color="gray.500" mt={2} textAlign="center">
              Enter로 전송
            </Text>
          </Box>
        </Box>
      )}
    </>
  );
};

export default AIConsultantChat;

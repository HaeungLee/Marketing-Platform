# 📅 Today Plan - AI 상담사 + Konva 편집기 + 대안 데이터 구현

## 🎯 오늘의 목표
**빠른 시각적 개선으로 플랫폼 완성도 향상**

### 우선순위
1. **24/7 AI 상담사 + UI** (Google API gemma3:27b 활용)
2. **Konva.js 기반 전단지 편집기** (Fabric.js 대체)
3. **소상공인 데이터 대안 소스** 정리

---

## 🤖 24/7 AI 상담사 구현

### 1.1 Google API 기반 gemma3:27b 연동
```python
# backend/src/services/ai_consultant_service.py
import google.generativeai as genai
from typing import Dict, Any
import os

class GoogleGemmaConsultant:
    """Google API 기반 소상공인 상담 AI"""
    
    def __init__(self):
        # Google API 키 설정
        genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
        
        # gemma3:27b 모델 초기화
        self.model = genai.GenerativeModel(
            model_name="models/gemma-1.5-pro-latest",  # 또는 gemma3:27b 해당 모델명
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=2048,
            )
        )
        
        # 소상공인 특화 시스템 프롬프트
        self.system_prompt = """
        당신은 한국의 소상공인 전문 경영 컨설턴트입니다.
        
        **전문 분야:**
        - 상권 분석 및 입지 선정
        - 업종별 창업 전략 수립
        - 마케팅 및 홍보 방안
        - 정부 지원사업 및 제도 안내
        - 경영 개선 및 수익성 향상
        
        **답변 원칙:**
        1. 구체적이고 실행 가능한 조언 제공
        2. 한국 시장 상황에 맞는 현실적 제안
        3. 단계별 실행 계획 포함
        4. 비용과 효과를 고려한 우선순위 제시
        5. 따뜻하고 친근한 톤으로 상담
        
        모든 답변은 3-5가지 핵심 포인트로 정리해 주세요.
        """
    
    async def provide_consultation(self, user_question: str, context: Dict[str, Any] = None) -> str:
        """AI 상담 제공"""
        try:
            # 컨텍스트 정보 추가 (지역, 업종 등)
            enhanced_prompt = self._build_consultation_prompt(user_question, context)
            
            # Google AI API 호출
            response = await self.model.generate_content_async(enhanced_prompt)
            
            return self._format_consultation_response(response.text)
            
        except Exception as e:
            logger.error(f"AI 상담 생성 실패: {e}")
            return self._get_fallback_response(user_question)
    
    def _build_consultation_prompt(self, question: str, context: Dict[str, Any]) -> str:
        """상담 프롬프트 구성"""
        context_info = ""
        if context:
            if context.get('business_type'):
                context_info += f"- 업종: {context['business_type']}\n"
            if context.get('region'):
                context_info += f"- 지역: {context['region']}\n"
            if context.get('budget'):
                context_info += f"- 예산: {context['budget']}원\n"
        
        full_prompt = f"""
        {self.system_prompt}
        
        **상담 요청 정보:**
        {context_info}
        
        **사용자 질문:**
        {question}
        
        위 정보를 바탕으로 전문적이고 실용적인 상담을 제공해주세요.
        """
        
        return full_prompt
    
    def _format_consultation_response(self, response: str) -> str:
        """응답 형식 정리"""
        # 응답 정리 및 포맷팅
        formatted = response.strip()
        
        # 구조화된 형식으로 변환
        if not formatted.startswith("💡"):
            formatted = f"💡 **전문 상담 결과**\n\n{formatted}"
        
        return formatted
    
    def _get_fallback_response(self, question: str) -> str:
        """API 실패 시 기본 응답"""
        return """
        💡 **상담 요청을 받았습니다**
        
        죄송합니다. 현재 AI 상담 시스템에 일시적인 문제가 발생했습니다.
        
        **일반적인 소상공인 조언:**
        1. **시장 조사**: 해당 지역의 경쟁업체와 타겟 고객 분석
        2. **차별화 전략**: 독특한 서비스나 제품으로 경쟁력 확보  
        3. **디지털 마케팅**: SNS와 온라인 플랫폼 적극 활용
        4. **고객 관리**: 단골 고객 확보를 위한 서비스 품질 향상
        5. **정부 지원**: 소상공인 대상 정책자금 및 교육 프로그램 활용
        
        구체적인 상담이 필요하시면 잠시 후 다시 시도해 주세요.
        """

# API 엔드포인트
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/consultation", tags=["AI Consultation"])

class ConsultationRequest(BaseModel):
    question: str
    business_type: str = None
    region: str = None
    budget: int = None

@router.post("/ask")
async def ask_consultant(request: ConsultationRequest):
    """AI 상담사에게 질문"""
    try:
        consultant = GoogleGemmaConsultant()
        
        context = {
            "business_type": request.business_type,
            "region": request.region,
            "budget": request.budget
        }
        
        answer = await consultant.provide_consultation(
            request.question, 
            context
        )
        
        return {
            "success": True,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상담 처리 실패: {str(e)}")
```

### 1.2 오른쪽 상단 AI 메뉴 + 드롭다운 채팅창 구현
```typescript
// frontend/src/components/AIConsultantDropdown.tsx
import React, { useState, useRef, useEffect } from 'react';
import {
  Box, VStack, HStack, Text, Input, Button, Avatar,
  useToast, Spinner, IconButton, useDisclosure,
  Collapse, Select, Tooltip, Divider, Badge
} from '@chakra-ui/react';
import { 
  FiSend, FiUser, FiMessageCircle, FiX, FiMaximize2, 
  FiPlus, FiChevronDown, FiChevronUp, FiBot
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
  budget?: number;
}

const AIConsultantDropdown: React.FC = () => {
  const { isOpen, onToggle, onClose } = useDisclosure();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
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
  const [isContextVisible, setIsContextVisible] = useState(false);
  const [fullscreen, setFullscreen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const toast = useToast();

  // 메시지 스크롤 자동 이동
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 외부 클릭 시 닫기
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen, onClose]);

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
      // gemini_service.py 참고한 API 호출
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
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const startNewConversation = () => {
    setMessages([
      {
        id: '1',
        type: 'ai',
        content: `새로운 상담을 시작합니다! 👋

**도움이 필요한 분야를 선택해주세요:**
• 상권분석 • 창업전략 
• 마케팅방안 • 자금조달

어떤 주제로 시작할까요?`,
        timestamp: new Date()
      }
    ]);
    setContext({});
    setIsContextVisible(false);
  };

  const openFullscreen = () => {
    setFullscreen(true);
    onClose();
  };

  return (
    <>
      {/* 오른쪽 상단 AI 메뉴 아이콘 */}
      <Box
        position="fixed"
        top="20px"
        right="20px"
        zIndex={1000}
        ref={dropdownRef}
      >
        <Tooltip label="AI 상담사" placement="left">
          <Button
            onClick={onToggle}
            size="md"
            colorScheme="blue"
            variant={isOpen ? "solid" : "outline"}
            leftIcon={<FiBot />}
            rightIcon={isOpen ? <FiChevronUp /> : <FiChevronDown />}
            shadow="md"
            _hover={{ shadow: "lg", transform: "translateY(-1px)" }}
            transition="all 0.2s"
          >
            AI 상담
            {messages.length > 1 && (
              <Badge ml={2} colorScheme="red" borderRadius="full">
                {messages.length - 1}
              </Badge>
            )}
          </Button>
        </Tooltip>

        {/* 드롭다운 채팅창 */}
        <Collapse in={isOpen} animateOpacity>
          <Box
            mt={2}
            width="400px"
            height="500px"
            bg="white"
            borderRadius="lg"
            shadow="xl"
            border="1px solid"
            borderColor="gray.200"
            display="flex"
            flexDirection="column"
            position="relative"
          >
            {/* 채팅창 헤더 */}
            <HStack 
              p={3} 
              bg="blue.500" 
              color="white" 
              borderTopRadius="lg"
              justify="space-between"
            >
              <HStack spacing={2}>
                <Avatar size="xs" name="AI" bg="blue.600" />
                <Text fontSize="sm" fontWeight="bold">소상공인 AI 상담사</Text>
              </HStack>
              
              <HStack spacing={1}>
                <Tooltip label="새 대화">
                  <IconButton
                    aria-label="새 대화"
                    icon={<FiPlus />}
                    size="xs"
                    variant="ghost"
                    color="white"
                    onClick={startNewConversation}
                  />
                </Tooltip>
                <Tooltip label="전체 화면">
                  <IconButton
                    aria-label="전체화면"
                    icon={<FiMaximize2 />}
                    size="xs"
                    variant="ghost"
                    color="white"
                    onClick={openFullscreen}
                  />
                </Tooltip>
                <Tooltip label="닫기">
                  <IconButton
                    aria-label="닫기"
                    icon={<FiX />}
                    size="xs"
                    variant="ghost"
                    color="white"
                    onClick={onClose}
                  />
                </Tooltip>
              </HStack>
            </HStack>

            {/* 컨텍스트 설정 (접을 수 있음) */}
            <Box>
              <Button
                size="xs"
                variant="ghost"
                width="100%"
                onClick={() => setIsContextVisible(!isContextVisible)}
                rightIcon={isContextVisible ? <FiChevronUp /> : <FiChevronDown />}
                borderRadius={0}
                fontSize="xs"
              >
                상세 설정 {context.businessType && `(${context.businessType})`}
              </Button>
              
              <Collapse in={isContextVisible}>
                <Box p={3} bg="gray.50" borderBottom="1px solid" borderColor="gray.200">
                  <VStack spacing={2}>
                    <HStack spacing={2} width="100%">
                      <Select 
                        placeholder="업종" 
                        size="xs"
                        value={context.businessType || ''}
                        onChange={(e) => setContext(prev => ({ ...prev, businessType: e.target.value }))}
                      >
                        <option value="카페">☕ 카페</option>
                        <option value="음식점">🍽️ 음식점</option>
                        <option value="편의점">🏪 편의점</option>
                        <option value="미용실">💇 미용실</option>
                      </Select>
                      
                      <Select 
                        placeholder="지역" 
                        size="xs"
                        value={context.region || ''}
                        onChange={(e) => setContext(prev => ({ ...prev, region: e.target.value }))}
                      >
                        <option value="강남구">강남구</option>
                        <option value="마포구">마포구</option>
                        <option value="홍대">홍대</option>
                      </Select>
                    </HStack>
                    
                    <Input 
                      placeholder="예산 (만원)" 
                      size="xs"
                      type="number"
                      value={context.budget || ''}
                      onChange={(e) => setContext(prev => ({ ...prev, budget: parseInt(e.target.value) || undefined }))}
                    />
                  </VStack>
                </Box>
              </Collapse>
            </Box>

            {/* 메시지 영역 */}
            <Box 
              flex="1" 
              overflowY="auto" 
              p={3}
              bg="gray.50"
            >
              <VStack spacing={3} align="stretch">
                {messages.map((message) => (
                  <HStack
                    key={message.id}
                    justify={message.type === 'user' ? 'flex-end' : 'flex-start'}
                    align="flex-start"
                    spacing={2}
                  >
                    {message.type === 'ai' && (
                      <Avatar size="xs" name="AI" bg="blue.500" color="white" />
                    )}
                    
                    <Box
                      maxWidth="80%"
                      bg={message.type === 'user' ? 'blue.500' : 'white'}
                      color={message.type === 'user' ? 'white' : 'gray.800'}
                      p={2}
                      borderRadius="md"
                      fontSize="xs"
                      border={message.type === 'ai' ? '1px solid' : 'none'}
                      borderColor="gray.200"
                      shadow={message.type === 'ai' ? 'sm' : 'none'}
                    >
                      <Text whiteSpace="pre-wrap">{message.content}</Text>
                      <Text 
                        fontSize="10px" 
                        opacity={0.7} 
                        mt={1}
                        textAlign={message.type === 'user' ? 'right' : 'left'}
                      >
                        {message.timestamp.toLocaleTimeString()}
                      </Text>
                    </Box>
                    
                    {message.type === 'user' && (
                      <Avatar size="xs" name="User" bg="gray.500" />
                    )}
                  </HStack>
                ))}
                
                {loading && (
                  <HStack justify="flex-start" spacing={2}>
                    <Avatar size="xs" name="AI" bg="blue.500" />
                    <Box bg="white" p={2} borderRadius="md" border="1px solid" borderColor="gray.200">
                      <HStack spacing={1}>
                        <Spinner size="xs" />
                        <Text fontSize="xs" color="gray.600">답변 준비중...</Text>
                      </HStack>
                    </Box>
                  </HStack>
                )}
                
                <div ref={messagesEndRef} />
              </VStack>
            </Box>

            {/* 입력 영역 */}
            <Box p={2} borderTop="1px solid" borderColor="gray.200" bg="white" borderBottomRadius="lg">
              <HStack spacing={2}>
                <Input
                  placeholder="질문을 입력하세요..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  disabled={loading}
                  size="sm"
                  fontSize="xs"
                />
                <IconButton
                  aria-label="전송"
                  icon={<FiSend />}
                  size="sm"
                  colorScheme="blue"
                  onClick={sendMessage}
                  disabled={loading || !inputMessage.trim()}
                />
              </HStack>
            </Box>
          </Box>
        </Collapse>
      </Box>

      {/* 전체화면 모달 */}
      {fullscreen && (
        <Box
          position="fixed"
          top={0}
          left={0}
          width="100vw"
          height="100vh"
          bg="rgba(0, 0, 0, 0.5)"
          zIndex={1500}
          display="flex"
          alignItems="center"
          justifyContent="center"
          onClick={() => setFullscreen(false)}
        >
          <Box
            width="90%"
            height="90%"
            maxWidth="1000px"
            maxHeight="800px"
            bg="white"
            borderRadius="lg"
            shadow="2xl"
            display="flex"
            flexDirection="column"
            onClick={(e) => e.stopPropagation()}
          >
            {/* 전체화면 헤더 */}
            <HStack 
              p={4} 
              bg="blue.500" 
              color="white" 
              borderTopRadius="lg"
              justify="space-between"
            >
              <HStack spacing={3}>
                <Avatar size="sm" name="AI 상담사" bg="blue.600" />
                <VStack align="start" spacing={0}>
                  <Text fontWeight="bold">소상공인 AI 상담사</Text>
                  <Text fontSize="sm" opacity={0.9}>24시간 언제든지 상담 가능</Text>
                </VStack>
              </HStack>
              
              <HStack spacing={2}>
                <Button
                  size="sm"
                  variant="ghost"
                  color="white"
                  leftIcon={<FiPlus />}
                  onClick={startNewConversation}
                >
                  새 대화
                </Button>
                <IconButton
                  aria-label="닫기"
                  icon={<FiX />}
                  size="sm"
                  variant="ghost"
                  color="white"
                  onClick={() => setFullscreen(false)}
                />
              </HStack>
            </HStack>

            {/* 전체화면 컨텍스트 설정 */}
            <Box p={3} bg="gray.50" borderBottom="1px solid" borderColor="gray.200">
              <HStack spacing={4}>
                <Select 
                  placeholder="업종 선택" 
                  size="sm" 
                  maxWidth="180px"
                  value={context.businessType || ''}
                  onChange={(e) => setContext(prev => ({ ...prev, businessType: e.target.value }))}
                >
                  <option value="카페">☕ 카페</option>
                  <option value="음식점">🍽️ 음식점</option>
                  <option value="편의점">🏪 편의점</option>
                  <option value="미용실">💇 미용실</option>
                  <option value="서비스업">🔧 서비스업</option>
                </Select>
                
                <Select 
                  placeholder="지역 선택" 
                  size="sm" 
                  maxWidth="180px"
                  value={context.region || ''}
                  onChange={(e) => setContext(prev => ({ ...prev, region: e.target.value }))}
                >
                  <option value="강남구">📍 강남구</option>
                  <option value="마포구">📍 마포구</option>
                  <option value="종로구">📍 종로구</option>
                  <option value="홍대">📍 홍대</option>
                  <option value="신촌">📍 신촌</option>
                </Select>
                
                <Input 
                  placeholder="예산 (만원)" 
                  size="sm" 
                  maxWidth="150px"
                  type="number"
                  value={context.budget || ''}
                  onChange={(e) => setContext(prev => ({ ...prev, budget: parseInt(e.target.value) || undefined }))}
                />
              </HStack>
            </Box>

            {/* 전체화면 메시지 영역 */}
            <Box 
              flex="1" 
              overflowY="auto" 
              p={4}
              bg="gray.50"
            >
              <VStack spacing={4} align="stretch">
                {messages.map((message) => (
                  <HStack
                    key={message.id}
                    justify={message.type === 'user' ? 'flex-end' : 'flex-start'}
                    align="flex-start"
                    spacing={3}
                  >
                    {message.type === 'ai' && (
                      <Avatar size="sm" name="AI" bg="blue.500" color="white" />
                    )}
                    
                    <Box
                      maxWidth="70%"
                      bg={message.type === 'user' ? 'blue.500' : 'white'}
                      color={message.type === 'user' ? 'white' : 'gray.800'}
                      p={4}
                      borderRadius="lg"
                      border={message.type === 'ai' ? '1px solid' : 'none'}
                      borderColor="gray.200"
                      shadow={message.type === 'ai' ? 'sm' : 'none'}
                    >
                      <Text fontSize="sm" whiteSpace="pre-wrap">
                        {message.content}
                      </Text>
                      <Text 
                        fontSize="xs" 
                        opacity={0.7} 
                        mt={2}
                        textAlign={message.type === 'user' ? 'right' : 'left'}
                      >
                        {message.timestamp.toLocaleTimeString()}
                      </Text>
                    </Box>
                    
                    {message.type === 'user' && (
                      <Avatar size="sm" name="User" bg="gray.500" icon={<FiUser />} />
                    )}
                  </HStack>
                ))}
                
                {loading && (
                  <HStack justify="flex-start" align="center" spacing={3}>
                    <Avatar size="sm" name="AI" bg="blue.500" color="white" />
                    <Box bg="white" p={3} borderRadius="lg" border="1px solid" borderColor="gray.200">
                      <HStack spacing={2}>
                        <Spinner size="sm" />
                        <Text fontSize="sm" color="gray.600">상담사가 답변을 준비중입니다...</Text>
                      </HStack>
                    </Box>
                  </HStack>
                )}
                
                <div ref={messagesEndRef} />
              </VStack>
            </Box>

            {/* 전체화면 입력 영역 */}
            <Box p={4} borderTop="1px solid" borderColor="gray.200" bg="white" borderBottomRadius="lg">
              <HStack spacing={3}>
                <Input
                  placeholder="궁금한 것을 질문해 주세요... (예: 강남역 근처에서 카페 창업하려는데 어떤 점을 고려해야 할까요?)"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  disabled={loading}
                />
                <Button
                  colorScheme="blue"
                  onClick={sendMessage}
                  disabled={loading || !inputMessage.trim()}
                  leftIcon={<FiSend />}
                >
                  전송
                </Button>
              </HStack>
            </Box>
          </Box>
        </Box>
      )}
    </>
  );
};

export default AIConsultantDropdown;
```

### 1.3 메인 애플리케이션에 AI 드롭다운 상담봇 통합
```typescript
// frontend/src/App.tsx 또는 layout 컴포넌트에 추가
import AIConsultantDropdown from './components/AIConsultantDropdown';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <BrowserRouter>
        {/* 기존 애플리케이션 라우터 */}
        <Routes>
          {/* 모든 라우트들... */}
        </Routes>
        
        {/* AI 드롭다운 상담봇 - 오른쪽 상단 고정 */}
        <AIConsultantDropdown />
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
```

### 1.4 백엔드 상담 API 구현 (gemini_service.py 활용)
```python
# backend/src/application/services/ai_consultant_service.py
from infrastructure.ai.gemini_service import GeminiService
from typing import Dict, Any
import os

class AIConsultantService:
    """소상공인 전문 AI 상담 서비스"""
    
    def __init__(self):
        self.gemini_service = GeminiService(
            api_key=os.getenv("GOOGLE_AI_API_KEY")
        )
        
        # 소상공인 상담 특화 시스템 프롬프트
        self.consultant_system_prompt = """
        당신은 한국의 소상공인 전문 경영 컨설턴트입니다.
        
        **전문 분야:**
        - 상권 분석 및 입지 선정
        - 업종별 창업 전략 수립
        - 마케팅 및 홍보 방안
        - 정부 지원사업 및 제도 안내
        - 경영 개선 및 수익성 향상
        
        **답변 원칙:**
        1. 구체적이고 실행 가능한 조언 제공
        2. 한국 시장 상황에 맞는 현실적 제안
        3. 단계별 실행 계획 포함
        4. 비용과 효과를 고려한 우선순위 제시
        5. 따뜻하고 친근한 톤으로 상담
        
        모든 답변은 3-5가지 핵심 포인트로 정리해 주세요.
        """
    
    async def provide_consultation(self, 
                                 question: str, 
                                 business_type: str = None,
                                 region: str = None, 
                                 budget: int = None) -> Dict[str, Any]:
        """AI 상담 제공"""
        try:
            # 컨텍스트 정보로 프롬프트 강화
            context_info = self._build_context_info(business_type, region, budget)
            
            # gemini_service의 generate_content 메소드를 상담용으로 활용
            consultation_prompt = f"""
            {self.consultant_system_prompt}
            
            **상담 요청 정보:**
            {context_info}
            
            **사용자 질문:**
            {question}
            
            위 정보를 바탕으로 전문적이고 실용적인 상담을 제공해주세요.
            """
            
            # GeminiService의 기존 인프라 활용
            business_info = {
                "name": business_type or "소상공인",
                "category": business_type or "",
                "product": {"name": "상담 서비스", "description": ""},
                "tone": "전문적이고 친근한",
                "keywords": [business_type, region] if business_type and region else []
            }
            
            # generate_content 메소드 재활용하되 프롬프트 오버라이드
            original_method = self.gemini_service._create_text_prompt
            self.gemini_service._create_text_prompt = lambda *args: consultation_prompt
            
            result = await self.gemini_service.generate_content(
                business_info=business_info,
                content_type="consultation"
            )
            
            # 원래 메소드 복원
            self.gemini_service._create_text_prompt = original_method
            
            return {
                "success": True,
                "answer": result["content"],
                "context": {
                    "business_type": business_type,
                    "region": region,
                    "budget": budget
                },
                "timestamp": result.get("performance_metrics", {}).get("generation_time", 0)
            }
            
        except Exception as e:
            print(f"AI 상담 생성 오류: {e}")
            return self._get_fallback_consultation(question, business_type)
    
    def _build_context_info(self, business_type: str, region: str, budget: int) -> str:
        """상담 컨텍스트 정보 구성"""
        context_parts = []
        
        if business_type:
            context_parts.append(f"- 업종: {business_type}")
        if region:
            context_parts.append(f"- 지역: {region}")
        if budget:
            context_parts.append(f"- 예산: {budget:,}만원")
        
        return "\n".join(context_parts) if context_parts else "- 일반 상담"
    
    def _get_fallback_consultation(self, question: str, business_type: str) -> Dict[str, Any]:
        """폴백 상담 응답"""
        return {
            "success": False,
            "answer": f"""
💡 **상담 요청을 받았습니다**

죄송합니다. 현재 AI 상담 시스템에 일시적인 문제가 발생했습니다.

**{business_type or '소상공인'} 관련 일반적인 조언:**

1. **시장 조사**: 해당 지역의 경쟁업체와 타겟 고객 분석
2. **차별화 전략**: 독특한 서비스나 제품으로 경쟁력 확보  
3. **디지털 마케팅**: SNS와 온라인 플랫폼 적극 활용
4. **고객 관리**: 단골 고객 확보를 위한 서비스 품질 향상
5. **정부 지원**: 소상공인 대상 정책자금 및 교육 프로그램 활용

구체적인 상담이 필요하시면 잠시 후 다시 시도해 주세요.
            """,
            "context": {"business_type": business_type},
            "timestamp": 0.1
        }

# API 라우터 (FastAPI)
# backend/src/presentation/api/v1/consultation.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from application.services.ai_consultant_service import AIConsultantService
from datetime import datetime

router = APIRouter(prefix="/api/v1/consultation", tags=["AI Consultation"])

class ConsultationRequest(BaseModel):
    question: str
    business_type: str = None
    region: str = None
    budget: int = None

@router.post("/ask")
async def ask_consultant(request: ConsultationRequest):
    """AI 상담사에게 질문 - gemini_service.py 기반"""
    try:
        consultant_service = AIConsultantService()
        
        result = await consultant_service.provide_consultation(
            question=request.question,
            business_type=request.business_type,
            region=request.region,
            budget=request.budget
        )
        
        return {
            **result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"상담 처리 실패: {str(e)}"
        )

@router.get("/health")
async def consultation_health():
    """상담 시스템 상태 확인"""
    try:
        consultant_service = AIConsultantService()
        # 간단한 테스트 질문으로 시스템 상태 확인
        test_result = await consultant_service.provide_consultation(
            question="안녕하세요",
            business_type="테스트"
        )
        
        return {
            "status": "healthy" if test_result["success"] else "degraded",
            "timestamp": datetime.now().isoformat(),
            "gemini_service": "connected"
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

---

## 🎨 Konva.js 기반 전단지 편집기

### 2.1 React-Konva 설치 및 설정
```bash
# 패키지 설치
npm install konva react-konva
npm install @types/konva --save-dev

# 폰트 및 아이콘 패키지
npm install @fontsource/noto-sans-kr lucide-react
```

### 2.2 Konva 편집기 메인 컴포넌트
```typescript
// frontend/src/components/KonvaFlyerEditor.tsx
import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Stage, Layer, Text, Image, Transformer, Rect } from 'react-konva';
import { 
  Box, VStack, HStack, Button, Input, Select, 
  ColorPicker, Slider, Divider, useToast, IconButton,
  ButtonGroup, Tooltip
} from '@chakra-ui/react';
import { 
  FiType, FiImage, FiSquare, FiCircle, FiDownload, 
  FiTrash2, FiCopy, FiRotateCw, FiZoomIn, FiZoomOut 
} from 'react-icons/fi';
import Konva from 'konva';

interface EditorElement {
  id: string;
  type: 'text' | 'image' | 'shape';
  x: number;
  y: number;
  width?: number;
  height?: number;
  // 텍스트 속성
  text?: string;
  fontSize?: number;
  fill?: string;
  fontFamily?: string;
  // 이미지 속성
  src?: string;
  // 도형 속성
  shapeType?: 'rect' | 'circle';
  stroke?: string;
  strokeWidth?: number;
}

interface KonvaFlyerEditorProps {
  width?: number;
  height?: number;
  onSave?: (imageData: string) => void;
}

const KonvaFlyerEditor: React.FC<KonvaFlyerEditorProps> = ({ 
  width = 600, 
  height = 800, 
  onSave 
}) => {
  const [elements, setElements] = useState<EditorElement[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [stageScale, setStageScale] = useState(1);
  const [stagePos, setStagePos] = useState({ x: 0, y: 0 });
  
  const stageRef = useRef<Konva.Stage>(null);
  const transformerRef = useRef<Konva.Transformer>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const toast = useToast();

  // 선택된 요소 변환기 연결
  useEffect(() => {
    if (selectedId && transformerRef.current) {
      const stage = stageRef.current;
      if (stage) {
        const selectedNode = stage.findOne(`#${selectedId}`);
        if (selectedNode) {
          transformerRef.current.nodes([selectedNode]);
          transformerRef.current.getLayer()?.batchDraw();
        }
      }
    }
  }, [selectedId]);

  // 텍스트 추가
  const addText = useCallback(() => {
    const newText: EditorElement = {
      id: `text-${Date.now()}`,
      type: 'text',
      x: 50,
      y: 50,
      text: '텍스트를 입력하세요',
      fontSize: 24,
      fill: '#000000',
      fontFamily: 'Noto Sans KR'
    };
    setElements(prev => [...prev, newText]);
    setSelectedId(newText.id);
  }, []);

  // 이미지 추가
  const addImage = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleImageUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const imageSrc = e.target?.result as string;
      
      const newImage: EditorElement = {
        id: `image-${Date.now()}`,
        type: 'image',
        x: 100,
        y: 100,
        width: 200,
        height: 150,
        src: imageSrc
      };
      
      setElements(prev => [...prev, newImage]);
      setSelectedId(newImage.id);
    };
    reader.readAsDataURL(file);
  }, []);

  // 도형 추가
  const addShape = useCallback((shapeType: 'rect' | 'circle') => {
    const newShape: EditorElement = {
      id: `shape-${Date.now()}`,
      type: 'shape',
      x: 150,
      y: 150,
      width: 100,
      height: 100,
      shapeType,
      fill: '#3182CE',
      stroke: '#2C5282',
      strokeWidth: 2
    };
    setElements(prev => [...prev, newShape]);
    setSelectedId(newShape.id);
  }, []);

  // 요소 삭제
  const deleteSelected = useCallback(() => {
    if (selectedId) {
      setElements(prev => prev.filter(el => el.id !== selectedId));
      setSelectedId(null);
    }
  }, [selectedId]);

  // 요소 복사
  const duplicateSelected = useCallback(() => {
    if (selectedId) {
      const element = elements.find(el => el.id === selectedId);
      if (element) {
        const newElement: EditorElement = {
          ...element,
          id: `${element.type}-${Date.now()}`,
          x: element.x + 20,
          y: element.y + 20
        };
        setElements(prev => [...prev, newElement]);
        setSelectedId(newElement.id);
      }
    }
  }, [selectedId, elements]);

  // 선택 해제
  const handleStageClick = useCallback((e: any) => {
    if (e.target === e.target.getStage()) {
      setSelectedId(null);
      transformerRef.current?.nodes([]);
    }
  }, []);

  // 요소 속성 업데이트
  const updateElement = useCallback((id: string, updates: Partial<EditorElement>) => {
    setElements(prev => 
      prev.map(el => el.id === id ? { ...el, ...updates } : el)
    );
  }, []);

  // 저장/내보내기
  const handleSave = useCallback(() => {
    if (stageRef.current) {
      const dataURL = stageRef.current.toDataURL({
        mimeType: 'image/png',
        quality: 1,
        pixelRatio: 2
      });
      
      if (onSave) {
        onSave(dataURL);
      } else {
        // 다운로드
        const link = document.createElement('a');
        link.download = `flyer-${Date.now()}.png`;
        link.href = dataURL;
        link.click();
      }
      
      toast({
        title: '전단지 저장 완료',
        status: 'success',
        duration: 2000,
      });
    }
  }, [onSave, toast]);

  // 줌 인/아웃
  const handleZoom = useCallback((direction: 'in' | 'out') => {
    const scaleBy = 1.2;
    const stage = stageRef.current;
    if (!stage) return;

    const oldScale = stageScale;
    const newScale = direction === 'in' ? oldScale * scaleBy : oldScale / scaleBy;
    
    const clampedScale = Math.max(0.1, Math.min(3, newScale));
    setStageScale(clampedScale);
  }, [stageScale]);

  const selectedElement = selectedId ? elements.find(el => el.id === selectedId) : null;

  return (
    <Box width="100%" display="flex" gap={4}>
      {/* 도구 패널 */}
      <VStack 
        width="250px" 
        bg="white" 
        p={4} 
        borderRadius="md" 
        border="1px solid" 
        borderColor="gray.200"
        align="stretch"
        spacing={4}
      >
        <Text fontWeight="bold" fontSize="lg">편집 도구</Text>
        
        {/* 요소 추가 버튼들 */}
        <VStack spacing={2} align="stretch">
          <Button leftIcon={<FiType />} onClick={addText} size="sm">
            텍스트 추가
          </Button>
          <Button leftIcon={<FiImage />} onClick={addImage} size="sm">
            이미지 추가
          </Button>
          <HStack>
            <Button 
              leftIcon={<FiSquare />} 
              onClick={() => addShape('rect')} 
              size="sm" 
              flex={1}
            >
              사각형
            </Button>
            <Button 
              leftIcon={<FiCircle />} 
              onClick={() => addShape('circle')} 
              size="sm" 
              flex={1}
            >
              원형
            </Button>
          </HStack>
        </VStack>

        <Divider />

        {/* 선택된 요소 속성 */}
        {selectedElement && (
          <VStack spacing={3} align="stretch">
            <Text fontWeight="semibold">선택된 요소 설정</Text>
            
            {selectedElement.type === 'text' && (
              <>
                <Box>
                  <Text fontSize="sm" mb={1}>텍스트</Text>
                  <Input
                    value={selectedElement.text || ''}
                    onChange={(e) => updateElement(selectedId!, { text: e.target.value })}
                    size="sm"
                  />
                </Box>
                
                <Box>
                  <Text fontSize="sm" mb={1}>글자 크기: {selectedElement.fontSize}</Text>
                  <Slider
                    value={selectedElement.fontSize || 24}
                    min={12}
                    max={72}
                    onChange={(value) => updateElement(selectedId!, { fontSize: value })}
                  />
                </Box>
                
                <Box>
                  <Text fontSize="sm" mb={1}>글자 색상</Text>
                  <Input
                    type="color"
                    value={selectedElement.fill || '#000000'}
                    onChange={(e) => updateElement(selectedId!, { fill: e.target.value })}
                    size="sm"
                  />
                </Box>
              </>
            )}

            {(selectedElement.type === 'shape' || selectedElement.type === 'image') && (
              <Box>
                <Text fontSize="sm" mb={1}>배경 색상</Text>
                <Input
                  type="color"
                  value={selectedElement.fill || '#3182CE'}
                  onChange={(e) => updateElement(selectedId!, { fill: e.target.value })}
                  size="sm"
                />
              </Box>
            )}
          </VStack>
        )}

        <Divider />

        {/* 편집 액션 */}
        <VStack spacing={2} align="stretch">
          <ButtonGroup size="sm" variant="outline" width="100%">
            <Tooltip label="복사">
              <IconButton 
                aria-label="복사" 
                icon={<FiCopy />} 
                onClick={duplicateSelected}
                disabled={!selectedId}
                flex={1}
              />
            </Tooltip>
            <Tooltip label="삭제">
              <IconButton 
                aria-label="삭제" 
                icon={<FiTrash2 />} 
                onClick={deleteSelected}
                disabled={!selectedId}
                colorScheme="red"
                flex={1}
              />
            </Tooltip>
          </ButtonGroup>
          
          <HStack>
            <Tooltip label="확대">
              <IconButton 
                aria-label="확대" 
                icon={<FiZoomIn />} 
                onClick={() => handleZoom('in')}
                size="sm"
              />
            </Tooltip>
            <Tooltip label="축소">
              <IconButton 
                aria-label="축소" 
                icon={<FiZoomOut />} 
                onClick={() => handleZoom('out')}
                size="sm"
              />
            </Tooltip>
            <Text fontSize="sm">{Math.round(stageScale * 100)}%</Text>
          </HStack>
          
          <Button 
            leftIcon={<FiDownload />} 
            onClick={handleSave}
            colorScheme="blue"
            size="sm"
          >
            저장/다운로드
          </Button>
        </VStack>
      </VStack>

      {/* 캔버스 영역 */}
      <Box 
        flex="1" 
        bg="gray.100" 
        borderRadius="md" 
        p={4}
        display="flex"
        justifyContent="center"
        alignItems="center"
        overflow="hidden"
      >
        <Box
          border="2px solid"
          borderColor="gray.300"
          borderRadius="md"
          bg="white"
          shadow="lg"
        >
          <Stage
            width={width}
            height={height}
            ref={stageRef}
            scaleX={stageScale}
            scaleY={stageScale}
            x={stagePos.x}
            y={stagePos.y}
            onMouseDown={handleStageClick}
            draggable
            onDragEnd={(e) => setStagePos({ x: e.target.x(), y: e.target.y() })}
          >
            <Layer>
              {/* 배경 */}
              <Rect width={width} height={height} fill="white" />
              
              {/* 요소들 렌더링 */}
              {elements.map((element) => {
                if (element.type === 'text') {
                  return (
                    <Text
                      key={element.id}
                      id={element.id}
                      x={element.x}
                      y={element.y}
                      text={element.text}
                      fontSize={element.fontSize}
                      fill={element.fill}
                      fontFamily={element.fontFamily}
                      draggable
                      onClick={() => setSelectedId(element.id)}
                      onDragEnd={(e) => {
                        updateElement(element.id, {
                          x: e.target.x(),
                          y: e.target.y()
                        });
                      }}
                    />
                  );
                }
                
                if (element.type === 'image' && element.src) {
                  const imageObj = new window.Image();
                  imageObj.src = element.src;
                  
                  return (
                    <Image
                      key={element.id}
                      id={element.id}
                      x={element.x}
                      y={element.y}
                      width={element.width}
                      height={element.height}
                      image={imageObj}
                      draggable
                      onClick={() => setSelectedId(element.id)}
                      onDragEnd={(e) => {
                        updateElement(element.id, {
                          x: e.target.x(),
                          y: e.target.y()
                        });
                      }}
                    />
                  );
                }
                
                if (element.type === 'shape') {
                  return (
                    <Rect
                      key={element.id}
                      id={element.id}
                      x={element.x}
                      y={element.y}
                      width={element.width}
                      height={element.height}
                      fill={element.fill}
                      stroke={element.stroke}
                      strokeWidth={element.strokeWidth}
                      cornerRadius={element.shapeType === 'circle' ? (element.width || 0) / 2 : 0}
                      draggable
                      onClick={() => setSelectedId(element.id)}
                      onDragEnd={(e) => {
                        updateElement(element.id, {
                          x: e.target.x(),
                          y: e.target.y()
                        });
                      }}
                    />
                  );
                }
                
                return null;
              })}
              
              {/* 변환기 */}
              {selectedId && (
                <Transformer
                  ref={transformerRef}
                  boundBoxFunc={(oldBox, newBox) => {
                    // 최소 크기 제한
                    if (newBox.width < 10 || newBox.height < 10) {
                      return oldBox;
                    }
                    return newBox;
                  }}
                  onTransformEnd={(e) => {
                    const node = e.target;
                    const selectedEl = elements.find(el => el.id === selectedId);
                    
                    if (selectedEl) {
                      updateElement(selectedId, {
                        x: node.x(),
                        y: node.y(),
                        width: node.width() * node.scaleX(),
                        height: node.height() * node.scaleY(),
                        ...(selectedEl.type === 'text' && {
                          fontSize: (selectedEl.fontSize || 24) * node.scaleY()
                        })
                      });
                      
                      // 스케일 리셋
                      node.scaleX(1);
                      node.scaleY(1);
                    }
                  }}
                />
              )}
            </Layer>
          </Stage>
        </Box>
      </Box>

      {/* 숨겨진 파일 입력 */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleImageUpload}
        accept="image/*"
        style={{ display: 'none' }}
      />
    </Box>
  );
};

export default KonvaFlyerEditor;
```

---

## 📊 소상공인 데이터 대안 소스

### 3.1 현재 문제 상황
```markdown
**소상공인365 API 제한사항:**
- iframe 형식으로만 제공
- JSON 데이터 직접 접근 불가
- API 키 발급 제한적
- 서버 로그인 문제 발생 중
```

### 3.2 대안 데이터 소스
```python
# backend/src/services/alternative_data_service.py
class AlternativeDataSources:
    """소상공인 데이터 대안 소스들"""
    
    def __init__(self):
        self.data_sources = {
            # 1. 공공데이터포털 (우선순위 1)
            "public_data": {
                "name": "공공데이터포털",
                "url": "https://www.data.go.kr/",
                "apis": {
                    "상가업소정보": "https://apis.data.go.kr/B553077/api/open/storeListInRadius",
                    "지역별인구통계": "https://apis.data.go.kr/1741000/admmSexdAgePpltn",
                    "소상공인시장진흥공단": "https://apis.data.go.kr/B553077/"
                },
                "장점": ["안정적", "무료", "정부 공인"],
                "단점": ["API 키 발급 필요", "호출 제한"]
            },
            
            # 2. 서울열린데이터 (서울 지역 특화)
            "seoul_open": {
                "name": "서울열린데이터광장",
                "url": "https://data.seoul.go.kr/",
                "apis": {
                    "상권분석정보": "http://openapi.seoul.go.kr:8088/.../CommercialDistrictAnalysisService/",
                    "인구밀도정보": "http://openapi.seoul.go.kr:8088/.../PopulationDensityService/",
                    "지하철역정보": "http://openapi.seoul.go.kr:8088/.../SubwayStationInfo/"
                },
                "장점": ["서울 데이터 풍부", "실시간 업데이트"],
                "단점": ["서울 지역 한정"]
            },
            
            # 3. 국가통계포털 (신뢰도 높음)
            "kosis": {
                "name": "국가통계포털(KOSIS)",
                "url": "https://kosis.kr/",
                "apis": {
                    "지역통계": "https://kosis.kr/openapi/",
                    "업종별통계": "https://kosis.kr/openapi/statisticsList.do"
                },
                "장점": ["정확한 통계", "장기 데이터"],
                "단점": ["API 복잡", "실시간성 부족"]
            },
            
            # 4. 경기데이터드림 (경기도 특화)
            "gyeonggi_data": {
                "name": "경기데이터드림",
                "url": "https://data.gg.go.kr/",
                "apis": {
                    "소상공인현황": "https://data.gg.go.kr/portal/data/service/",
                    "상권정보": "https://data.gg.go.kr/portal/data/service/"
                },
                "장점": ["경기도 상세 데이터"],
                "단점": ["경기도 한정"]
            }
        }
    
    async def collect_alternative_data(self):
        """대안 소스들에서 데이터 수집"""
        collected_data = {
            "business_stores": [],
            "population_stats": [],
            "commercial_areas": []
        }
        
        # 1. 공공데이터포털에서 상가 정보 수집
        try:
            stores_data = await self._fetch_public_stores()
            collected_data["business_stores"].extend(stores_data)
        except Exception as e:
            logger.warning(f"공공데이터포털 수집 실패: {e}")
        
        # 2. 서울열린데이터에서 상권 분석 수집
        try:
            commercial_data = await self._fetch_seoul_commercial()
            collected_data["commercial_areas"].extend(commercial_data)
        except Exception as e:
            logger.warning(f"서울열린데이터 수집 실패: {e}")
        
        # 3. KOSIS에서 인구통계 수집
        try:
            population_data = await self._fetch_kosis_population()
            collected_data["population_stats"].extend(population_data)
        except Exception as e:
            logger.warning(f"KOSIS 수집 실패: {e}")
        
        return collected_data
    
    async def _fetch_public_stores(self):
        """공공데이터포털 상가업소 정보 수집"""
        api_key = os.getenv("PUBLIC_DATA_API_KEY")
        base_url = "https://apis.data.go.kr/B553077/api/open/storeListInRadius"
        
        # 주요 지역별로 데이터 수집
        major_locations = [
            {"name": "강남역", "lat": 37.4979, "lng": 127.0276},
            {"name": "홍대입구", "lat": 37.5571, "lng": 126.9245},
            {"name": "명동", "lat": 37.5636, "lng": 126.9838},
            {"name": "신촌", "lat": 37.5549, "lng": 126.9356}
        ]
        
        all_stores = []
        for location in major_locations:
            try:
                params = {
                    "serviceKey": api_key,
                    "type": "json",
                    "radius": "1000",
                    "cx": str(location["lng"]),
                    "cy": str(location["lat"]),
                    "numOfRows": "100"
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(base_url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get("response", {}).get("body", {}).get("items"):
                                items = data["response"]["body"]["items"]["item"]
                                if isinstance(items, list):
                                    all_stores.extend(items)
                                else:
                                    all_stores.append(items)
                                    
            except Exception as e:
                logger.error(f"{location['name']} 데이터 수집 실패: {e}")
                continue
        
        return all_stores
    
    async def _fetch_seoul_commercial(self):
        """서울열린데이터 상권분석 정보 수집"""
        api_key = os.getenv("SEOUL_API_KEY")
        base_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/VwsmSignguStorW/1/100/"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("VwsmSignguStorW", {}).get("row", [])
        except Exception as e:
            logger.error(f"서울 상권분석 수집 실패: {e}")
        
        return []
    
    async def _fetch_kosis_population(self):
        """KOSIS 인구통계 수집"""  
        # KOSIS API는 복잡하므로 CSV 다운로드 후 처리하는 방식도 고려
        api_key = os.getenv("KOSIS_API_KEY")
        base_url = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
        
        params = {
            "method": "getList",
            "apiKey": api_key,
            "itmId": "13103_ATAG_13102",  # 인구통계 항목ID
            "objL1": "ALL",  # 시도
            "objL2": "ALL",  # 시군구
            "format": "json",
            "jsonVD": "Y"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
        except Exception as e:
            logger.error(f"KOSIS 인구통계 수집 실패: {e}")
        
        return []

# 정적 트렌드 데이터 (pytrends 대체)
class StaticTrendProvider:
    """정적 트렌드 분석 데이터 제공"""
    
    BUSINESS_TRENDS = {
        "카페": {
            "seasonal_patterns": {
                "spring": {"score": 85, "note": "야외 테라스 수요 증가"},
                "summer": {"score": 75, "note": "아이스 음료 매출 증가"},
                "fall": {"score": 90, "note": "실내 공간 선호도 증가"},
                "winter": {"score": 95, "note": "따뜻한 음료 성수기"}
            },
            "peak_hours": ["08:00-10:00", "14:00-16:00", "19:00-21:00"],
            "target_demographics": ["20-30대 직장인", "대학생", "프리랜서"],
            "marketing_keywords": ["원두", "디저트", "와이파이", "스터디카페"]
        },
        
        "음식점": {
            "seasonal_patterns": {
                "spring": {"score": 80, "note": "야외 식사 수요 증가"},
                "summer": {"score": 70, "note": "시원한 음식 선호"},
                "fall": {"score": 85, "note": "보양식 수요 증가"},
                "winter": {"score": 90, "note": "따뜻한 국물 요리 인기"}
            },
            "peak_hours": ["12:00-14:00", "18:00-20:00"],
            "target_demographics": ["전 연령대", "직장인", "가족단위"],
            "marketing_keywords": ["맛집", "배달", "포장", "테이크아웃"]
        },
        
        "편의점": {
            "seasonal_patterns": {
                "spring": {"score": 75, "note": "일정한 수요"},
                "summer": {"score": 80, "note": "음료수, 아이스크림 증가"},
                "fall": {"score": 75, "note": "일정한 수요"},
                "winter": {"score": 85, "note": "따뜻한 음료, 군것질 증가"}
            },
            "peak_hours": ["07:00-09:00", "12:00-13:00", "18:00-22:00"],
            "target_demographics": ["전 연령대", "직장인", "학생"],
            "marketing_keywords": ["편의성", "24시간", "택배", "ATM"]
        }
    }
    
    def get_trend_analysis(self, business_type: str, region: str = None) -> Dict:
        """업종별 트렌드 분석 제공"""
        trend_data = self.BUSINESS_TRENDS.get(business_type, {})
        
        return {
            "business_type": business_type,
            "region": region or "전국",
            "analysis_date": datetime.now().isoformat(),
            "seasonal_trends": trend_data.get("seasonal_patterns", {}),
            "optimal_hours": trend_data.get("peak_hours", []),
            "target_customers": trend_data.get("target_demographics", []),
            "marketing_tips": trend_data.get("marketing_keywords", []),
            "trend_score": self._calculate_current_trend_score(business_type)
        }
    
    def _calculate_current_trend_score(self, business_type: str) -> int:
        """현재 시기 기준 트렌드 점수 계산"""
        current_month = datetime.now().month
        
        # 계절별 점수 (간단한 로직)
        if current_month in [3, 4, 5]:  # 봄
            season = "spring"
        elif current_month in [6, 7, 8]:  # 여름
            season = "summer"
        elif current_month in [9, 10, 11]:  # 가을
            season = "fall"
        else:  # 겨울
            season = "winter"
        
        trend_data = self.BUSINESS_TRENDS.get(business_type, {})
        seasonal_data = trend_data.get("seasonal_patterns", {})
        
        return seasonal_data.get(season, {}).get("score", 75)
```

---

## 🚀 오늘의 실행 계획

### 즉시 시작 (오전)
1. **Google API 키 설정** - gemma3:27b 연동
2. **AI 상담사 백엔드** 구현 (gemini_service.py 활용) (1-2시간)
3. **오른쪽 상단 AI 드롭다운** 구현 (Copilot 스타일) (2시간)

### 오후 작업
1. **React-Konva 패키지 설치**
2. **기본 편집기 구조** 구현
3. **텍스트/이미지 추가** 기능

### 저녁 마무리
1. **대안 데이터 소스** 연동 테스트
2. **정적 트렌드 데이터** 적용
3. **통합 테스트** 및 디버깅

## 📋 체크리스트

- [ ] Google AI API 키 발급 및 설정
- [ ] **오른쪽 상단 AI 메뉴** - 봇 아이콘 + 드롭다운 버튼
- [ ] **Copilot 스타일 드롭다운** - 400x500 채팅창
- [ ] **헤더 3버튼** - 새대화, 전체창, 닫기
- [ ] **외부 클릭 시 자동 닫기** 기능
- [ ] **전체화면 모달** - 90% 화면 차지
- [ ] AI 상담사 백엔드 서비스 구현 (gemini_service.py 재활용)
- [ ] React-Konva 설치 및 기본 설정
- [ ] 전단지 편집기 핵심 기능 구현
- [ ] 공공데이터포털 API 연동 테스트
- [ ] 정적 트렌드 시스템 적용
- [ ] UI/UX 개선 및 최종 테스트

## 🎯 AI 드롭다운 상담봇 핵심 기능
- **위치**: 오른쪽 상단 고정 (top: 20px, right: 20px)
- **아이콘**: 봇 아이콘 + "AI 상담" 텍스트 + 화살표
- **드롭다운**: 클릭 시 아래로 400x500 채팅창 펼침
- **헤더 버튼**: ➕새대화 🔍전체창 ❌닫기
- **Badge**: 메시지 개수 표시 (대화 진행 시)
- **외부 클릭**: 자동 닫기 (useEffect + addEventListener)

이 계획으로 오늘 하루 만에 눈에 띄는 개선을 만들 수 있을 것 같습니다! 🚀

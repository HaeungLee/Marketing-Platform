import React, { useState, useRef, useCallback } from 'react';
import {
  Box,
  VStack,
  HStack,
  Input,
  Button,
  Text,
  useToast,
  Container,
  Heading,
  ButtonGroup,
  IconButton,
  Spacer,
  Image,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react';
import { DownloadIcon, RepeatIcon } from '@chakra-ui/icons';

const FlyerGenerator: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [imageError, setImageError] = useState<string | null>(null);
  const toast = useToast();

  // Base64 이미지 검증 함수
  const validateBase64Image = useCallback((base64Data: string): boolean => {
    try {
      // Base64 문자 검증
      const base64Regex = /^[A-Za-z0-9+/]*={0,2}$/;
      if (!base64Regex.test(base64Data)) {
        console.error('❌ Invalid base64 characters');
        return false;
      }
      
      // 길이 검증 (4의 배수여야 함)
      if (base64Data.length % 4 !== 0) {
        console.error('❌ Base64 length is not multiple of 4:', base64Data.length);
        return false;
      }
      
      // PNG 시그니처 확인
      if (base64Data.startsWith('iVBOR')) {
        console.log('✅ Valid PNG signature detected');
        return true;
      }
      
      // JPEG 시그니처 확인  
      if (base64Data.startsWith('/9j/')) {
        console.log('✅ Valid JPEG signature detected');
        return true;
      }
      
      console.warn('⚠️ Unknown image format, but proceeding');
      return true;
    } catch (error) {
      console.error('❌ Base64 validation error:', error);
      return false;
    }
  }, []);  const generateImage = async () => {
    if (!prompt) {
      toast({
        title: '프롬프트를 입력해주세요.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    setImageError(null);
    setGeneratedImage(null);

    try {
      console.log('🚀 Sending request to:', 'http://localhost:8000/api/images/generate');
      console.log('📝 Request body:', { prompt });
      
      const response = await fetch('http://localhost:8000/api/images/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt,
        }),
      });

      console.log('📊 Response status:', response.status);
      console.log('📋 Response ok:', response.ok);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Response error text:', errorText);
        let error;
        try {
          error = JSON.parse(errorText);
        } catch {
          error = { detail: errorText };
        }
        throw new Error(error.detail || '이미지 생성에 실패했습니다.');
      }

      const data = await response.json();
      console.log('✅ Response data keys:', Object.keys(data));
      console.log('🖼️ Has image_data:', !!data.image_data);
      console.log('📏 Image data length:', data.image_data?.length);
      console.log('🔍 Image data preview (first 100 chars):', data.image_data?.substring(0, 100));
        if (!data.image_data) {
        throw new Error('이미지 데이터를 받지 못했습니다.');
      }      // Base64 데이터 검증 및 정리
      let cleanBase64 = data.image_data;
      
      // Base64 데이터에서 불필요한 문자 제거
      cleanBase64 = cleanBase64.replace(/\s/g, ''); // 공백 제거
      cleanBase64 = cleanBase64.replace(/\n/g, ''); // 줄바꿈 제거
      
      console.log('🧹 Cleaned base64 length:', cleanBase64.length);
      console.log('🔍 Cleaned base64 preview (first 100 chars):', cleanBase64.substring(0, 100));
      console.log('🔍 Cleaned base64 preview (last 50 chars):', cleanBase64.substring(cleanBase64.length - 50));
      
      // Base64 검증
      if (!validateBase64Image(cleanBase64)) {
        throw new Error('잘못된 Base64 이미지 데이터입니다.');
      }
      
      console.log('🧹 Cleaned base64 length:', cleanBase64.length);
      console.log('🔍 Cleaned base64 preview (first 100 chars):', cleanBase64.substring(0, 100));
      console.log('🔍 Cleaned base64 preview (last 50 chars):', cleanBase64.substring(cleanBase64.length - 50));
      
      // MIME 타입 감지 개선
      let mimeType = 'image/png';
      if (cleanBase64.startsWith('iVBOR')) {
        mimeType = 'image/png';
      } else if (cleanBase64.startsWith('/9j/')) {
        mimeType = 'image/jpeg';
      } else if (cleanBase64.startsWith('R0lGOD')) {
        mimeType = 'image/gif';
      }
      
      console.log('🎨 Detected MIME type:', mimeType);
      
      // Data URL 생성
      const imageUrl = `data:${mimeType};base64,${cleanBase64}`;
      console.log('🔗 Generated data URL length:', imageUrl.length);
      console.log('🔗 Data URL preview:', imageUrl.substring(0, 200));
      
      setGeneratedImage(imageUrl);
      
      // 성공 알림
      toast({
        title: '이미지 생성 완료!',
        description: '프롬프트에 따라 이미지가 생성되었습니다.',
        status: 'success',
        duration: 4000,
        isClosable: true,
      });
      
    } catch (error) {
      console.error('Generation error:', error);
      const errorMessage = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.';
      setImageError(errorMessage);
      toast({
        title: '오류가 발생했습니다.',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };
  // 이미지 다운로드 함수
  const downloadImage = useCallback(() => {
    if (!generatedImage) {
      toast({
        title: '다운로드할 이미지가 없습니다.',
        status: 'warning',
        duration: 2000,
        isClosable: true,
      });
      return;
    }
    
    const link = document.createElement('a');
    link.download = 'generated-flyer.png';
    link.href = generatedImage;
    link.click();
  }, [generatedImage, toast]);

  // 새 이미지 생성 (이전 이미지 클리어)
  const generateNewImage = useCallback(() => {
    setGeneratedImage(null);
    setImageError(null);
  }, []);
  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={6}>
        <Heading>전단지 생성기</Heading>
        
        <Box w="100%">
          <Input
            placeholder="이미지 생성을 위한 프롬프트를 입력하세요 (예: 카페 전단지, 모던한 스타일)"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            mb={4}
            onKeyPress={(e) => e.key === 'Enter' && generateImage()}
          />
          <HStack spacing={4}>
            <Button
              colorScheme="blue"
              onClick={generateImage}
              isLoading={isLoading}
              flex="1"
            >
              이미지 생성
            </Button>
            {generatedImage && (
              <>
                <Button
                  variant="outline"
                  onClick={generateNewImage}
                  leftIcon={<RepeatIcon />}
                >
                  새로 생성
                </Button>
                <IconButton
                  aria-label="이미지 다운로드"
                  icon={<DownloadIcon />}
                  onClick={downloadImage}
                  colorScheme="green"
                />
              </>
            )}
          </HStack>
        </Box>

        {/* 에러 메시지 표시 */}
        {imageError && (
          <Alert status="error">
            <AlertIcon />
            <Box>
              <AlertTitle>이미지 생성 실패!</AlertTitle>
              <AlertDescription>{imageError}</AlertDescription>
            </Box>
          </Alert>
        )}        {/* 생성된 이미지 표시 */}
        {generatedImage && (
          <Box w="100%" p={4} border="1px" borderColor="gray.200" borderRadius="md" textAlign="center">
            <Text mb={4} fontSize="lg" fontWeight="medium">생성된 이미지</Text>
            <Image
              src={generatedImage}
              alt="Generated Image"
              maxW="100%"
              maxH="600px"
              mx="auto"
              border="1px solid #e2e8f0"
              borderRadius="md"
              onLoad={() => {
                console.log('✅ Image loaded successfully!');
                setImageError(null); // 성공 시 에러 클리어
              }}
              onError={(e) => {
                console.error('❌ 이미지 표시 실패:', e);
                console.error('❌ Image src:', generatedImage?.substring(0, 200));
                console.error('❌ Image src length:', generatedImage?.length);
                setImageError('이미지를 표시할 수 없습니다. Base64 형식을 확인해주세요.');
              }}
            />
            <Text mt={2} fontSize="sm" color="gray.500">
              이미지를 우클릭하여 저장하거나 위의 다운로드 버튼을 사용하세요.
            </Text>
            
            {/* 디버깅 정보 */}
            <Box mt={4} p={2} bg="gray.50" borderRadius="md" fontSize="xs" color="gray.600">
              <Text>데이터 URL 길이: {generatedImage?.length}</Text>
              <Text>MIME 타입: {generatedImage?.match(/data:([^;]+)/)?.[1] || 'unknown'}</Text>
              <Text>Base64 시작: {generatedImage?.substring(0, 100)}...</Text>
            </Box>
          </Box>
        )}

        {/* 로딩 상태이고 이미지가 없을 때 플레이스홀더 */}
        {isLoading && !generatedImage && (
          <Box w="100%" p={8} border="1px" borderColor="gray.200" borderRadius="md" textAlign="center">
            <Text fontSize="lg" color="gray.500">
              이미지 생성 중...
            </Text>
            <Text fontSize="sm" color="gray.400" mt={2}>
              프롬프트: "{prompt}"
            </Text>
          </Box>
        )}

        {/* 초기 상태 안내 */}
        {!generatedImage && !isLoading && !imageError && (
          <Box w="100%" p={8} border="1px" borderColor="gray.200" borderRadius="md" textAlign="center">
            <Text fontSize="lg" color="gray.500" mb={2}>
              프롬프트를 입력하고 이미지를 생성해보세요!
            </Text>
            <Text fontSize="sm" color="gray.400">
              예시: "귀여운 고양이", "산 풍경", "현대적인 카페 인테리어" 등
            </Text>
          </Box>
        )}
      </VStack>
    </Container>
  );
};

export default FlyerGenerator;
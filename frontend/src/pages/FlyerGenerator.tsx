import React, { useState, useRef, useCallback } from 'react';
import {
  Box,
  VStack,
  Input,
  Button,
  Image,
  Text,
  useToast,
  Container,
  Heading,
  Progress,
} from '@chakra-ui/react';
import 'fabric';
declare const fabric: any;

const FlyerGenerator: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fabricCanvasRef = useRef<any>(null);
  const toast = useToast();

  const generateImage = async () => {
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
    try {
      const response = await fetch('/api/images/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: prompt,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || '이미지 생성에 실패했습니다.');
      }
      
      const data = await response.json();
      if (!data.image_data) {
        throw new Error('이미지 데이터를 받지 못했습니다.');
      }

      const imageData = data.image_data;
      setImageUrl(`data:image/png;base64,${imageData}`);
      
      // 이미지를 Fabric 캔버스에 추가
      fabric.Image.fromURL(`data:image/png;base64,${imageData}`, (img: any) => {
        if (fabricCanvasRef.current) {
          fabricCanvasRef.current.clear();
          // 이미지 크기 조정
          const scale = Math.min(
            800 / (img.width || 512),
            600 / (img.height || 512)
          );
          img.scale(scale);
          fabricCanvasRef.current.add(img);
          fabricCanvasRef.current.centerObject(img);
          fabricCanvasRef.current.renderAll();
        }
      });
      
    } catch (error) {
      console.error('Generation error:', error);
      toast({
        title: '오류가 발생했습니다.',
        description: error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    // Canvas 초기화
    if (canvasRef.current && !fabricCanvasRef.current) {
      fabricCanvasRef.current = new fabric.Canvas(canvasRef.current, {
        width: 800,
        height: 600,
      });

      // 기본 배경색 설정
      fabricCanvasRef.current.setBackgroundColor('#ffffff', () => {
        fabricCanvasRef.current?.renderAll();
      });
    }

    return () => {
      // 컴포넌트 언마운트 시 캔버스 정리
      if (fabricCanvasRef.current) {
        fabricCanvasRef.current.dispose();
      }
    };
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
          />
          <Button
            colorScheme="blue"
            onClick={generateImage}
            isLoading={isLoading}
            w="100%"
            mb={4}
          >
            이미지 생성
          </Button>
        </Box>

        <Box w="100%" border="1px" borderColor="gray.200" borderRadius="md" p={4}>
          <canvas ref={canvasRef} style={{ border: '1px solid #ccc' }} />
        </Box>

        {imageUrl && (
          <Image
            src={imageUrl}
            alt="생성된 이미지"
            maxW="100%"
            borderRadius="md"
          />
        )}
      </VStack>
    </Container>
  );
};

export default FlyerGenerator; 
import React, { useState, useRef, useCallback, useEffect } from 'react';
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
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  IconButton,
  Spacer,
} from '@chakra-ui/react';
import { AddIcon, DeleteIcon, DownloadIcon, RepeatIcon } from '@chakra-ui/icons';
import { Canvas, Text as FabricText, Image as FabricImage, Rect, Circle, Triangle } from 'fabric';

const FlyerGenerator: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedTool, setSelectedTool] = useState<string>('select');
  const [textInput, setTextInput] = useState('');
  const [fontSize, setFontSize] = useState(24);
  const [textColor, setTextColor] = useState('#000000');
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fabricCanvasRef = useRef<any>(null);const toast = useToast();

  // 이미지를 캔버스에 추가하는 함수
  const addImageToCanvas = useCallback(async (imageData: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      if (!fabricCanvasRef.current) {
        reject(new Error('Canvas not initialized'));
        return;
      }

      try {
        const imgElement = document.createElement('img');
        
        imgElement.onload = async () => {
          try {            console.log('🖼️ Image loaded, creating Fabric image...');
            const fabricImg = await FabricImage.fromElement(imgElement);
            
            if (!fabricImg) {
              throw new Error('Failed to create Fabric image');
            }
            
            // 캔버스 클리어
            fabricCanvasRef.current.clear();
            
            // 이미지 크기 조정 (캔버스에 맞게)
            const canvasWidth = fabricCanvasRef.current.getWidth();
            const canvasHeight = fabricCanvasRef.current.getHeight();
            const scale = Math.min(
              canvasWidth / imgElement.naturalWidth,
              canvasHeight / imgElement.naturalHeight
            ) * 0.8; // 여백을 위해 0.8 배율 적용
            
            fabricImg.scale(scale);
              // 캔버스에 추가하고 중앙 정렬
            fabricCanvasRef.current.add(fabricImg);
            fabricCanvasRef.current.centerObject(fabricImg);
            fabricCanvasRef.current.renderAll();
              // 캔버스 상태 디버깅
            console.log('🎯 Canvas objects count:', fabricCanvasRef.current.getObjects().length);
            console.log('📐 Canvas dimensions:', fabricCanvasRef.current.getWidth(), 'x', fabricCanvasRef.current.getHeight());
            console.log('🖼️ Image dimensions:', fabricImg.width, 'x', fabricImg.height);
            console.log('🔍 Image position:', fabricImg.left, ',', fabricImg.top);
            console.log('📏 Image scale:', fabricImg.scaleX, 'x', fabricImg.scaleY);
            
            // Force a manual render to ensure visibility
            setTimeout(() => {
              fabricCanvasRef.current.renderAll();
              console.log('🔄 Forced re-render completed');
            }, 100);
            
            console.log('✅ Image successfully added to canvas');
            resolve();
          } catch (err) {
            console.error('❌ FabricImage.fromElement error:', err);
            reject(err);
          }
        };
        
        imgElement.onerror = (err) => {
          console.error('❌ Image load error:', err);
          reject(new Error('Failed to load image'));
        };
        
        imgElement.src = `data:image/png;base64,${imageData}`;
      } catch (error) {
        console.error('❌ Image creation error:', error);
        reject(error);
      }
    });
  }, []);

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
    try {      console.log('🚀 Sending request to:', '/api/images/generate');
      console.log('📝 Request body:', { prompt });
      
      const response = await fetch('/api/images/generate', {
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
      }const imageData = data.image_data;
        // 이미지를 Fabric 캔버스에 추가
      try {
        await addImageToCanvas(imageData);
        console.log('🎨 Image successfully added to canvas');
        
        // 성공 알림
        toast({
          title: '이미지 생성 완료!',
          description: '캔버스에 이미지가 추가되었습니다. 편집 도구를 사용해 텍스트와 도형을 추가하세요.',
          status: 'success',
          duration: 4000,
          isClosable: true,
        });
      } catch (imageError) {
        console.error('❌ Failed to add image to canvas:', imageError);
        toast({
          title: '캔버스에 이미지 추가 실패',
          description: '이미지는 생성되었지만 캔버스에 추가하는데 실패했습니다.',
          status: 'warning',
          duration: 3000,
          isClosable: true,
        });
      }
      
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

  // 텍스트 추가 함수
  const addText = useCallback(() => {
    if (!fabricCanvasRef.current || !textInput.trim()) {
      toast({
        title: '텍스트를 입력해주세요.',
        status: 'warning',
        duration: 2000,
        isClosable: true,
      });
      return;
    }    const text = new FabricText(textInput, {
      left: 100,
      top: 100,
      fontSize: fontSize,
      fill: textColor,
      fontFamily: 'Arial',
    });

    fabricCanvasRef.current.add(text);
    fabricCanvasRef.current.setActiveObject(text);
    fabricCanvasRef.current.renderAll();
    setTextInput('');
  }, [textInput, fontSize, textColor, toast]);

  // 도형 추가 함수
  const addShape = useCallback((shapeType: string) => {
    if (!fabricCanvasRef.current) return;

    let shape;
    const commonProps = {
      left: 150,
      top: 150,
      fill: 'rgba(0, 123, 255, 0.5)',
      stroke: '#007bff',
      strokeWidth: 2,
    };    switch (shapeType) {
      case 'rectangle':
        shape = new Rect({
          ...commonProps,
          width: 100,
          height: 80,
        });
        break;
      case 'circle':
        shape = new Circle({
          ...commonProps,
          radius: 50,
        });
        break;
      case 'triangle':
        shape = new Triangle({
          ...commonProps,
          width: 100,
          height: 100,
        });
        break;
      default:
        return;
    }

    fabricCanvasRef.current.add(shape);
    fabricCanvasRef.current.setActiveObject(shape);
    fabricCanvasRef.current.renderAll();
  }, []);

  // 선택된 객체 삭제
  const deleteSelected = useCallback(() => {
    if (!fabricCanvasRef.current) return;
    
    const activeObjects = fabricCanvasRef.current.getActiveObjects();
    if (activeObjects.length) {
      fabricCanvasRef.current.remove(...activeObjects);
      fabricCanvasRef.current.discardActiveObject();
      fabricCanvasRef.current.renderAll();
    }
  }, []);
  // 캔버스 지우기
  const clearCanvas = useCallback(() => {
    if (!fabricCanvasRef.current) return;
    fabricCanvasRef.current.clear();
    fabricCanvasRef.current.backgroundColor = '#ffffff';
    fabricCanvasRef.current.renderAll();
  }, []);

  // 이미지 다운로드
  const downloadImage = useCallback(() => {
    if (!fabricCanvasRef.current) return;
    
    const dataURL = fabricCanvasRef.current.toDataURL({
      format: 'png',
      quality: 1,
    });
    
    const link = document.createElement('a');
    link.download = 'flyer.png';
    link.href = dataURL;
    link.click();
  }, []);

  // 실행 취소/다시 실행 (간단한 구현)
  const undo = useCallback(() => {
    // 실제 구현에서는 상태 관리가 필요합니다
    toast({
      title: '실행 취소 기능은 향후 구현됩니다.',
      status: 'info',
      duration: 2000,
      isClosable: true,
    });
  }, [toast]);  useEffect(() => {
    // Canvas 초기화
    if (canvasRef.current && !fabricCanvasRef.current) {
      try {
        fabricCanvasRef.current = new Canvas(canvasRef.current);
        fabricCanvasRef.current.setDimensions({
          width: 800,
          height: 600
        });
        fabricCanvasRef.current.backgroundColor = '#ffffff';
        fabricCanvasRef.current.renderAll();
      } catch (error) {
        console.error('Canvas initialization error:', error);
      }
    }

    return () => {
      // 컴포넌트 언마운트 시 캔버스 정리
      if (fabricCanvasRef.current) {
        try {
          fabricCanvasRef.current.dispose();
          fabricCanvasRef.current = null;
        } catch (error) {
          console.error('Canvas disposal error:', error);
        }
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
        </Box>        <HStack spacing={4} w="100%">
          <ButtonGroup variant="outline" spacing="4">
            <Button
              onClick={() => setSelectedTool('text')}
              colorScheme={selectedTool === 'text' ? 'blue' : 'gray'}
              leftIcon={<AddIcon />}
            >
              텍스트 추가
            </Button>
            <Button
              onClick={() => addShape('rectangle')}
              colorScheme={selectedTool === 'rectangle' ? 'blue' : 'gray'}
              leftIcon={<AddIcon />}
            >
              사각형 추가
            </Button>
            <Button
              onClick={() => addShape('circle')}
              colorScheme={selectedTool === 'circle' ? 'blue' : 'gray'}
              leftIcon={<AddIcon />}
            >
              원 추가
            </Button>
            <Button
              onClick={() => addShape('triangle')}
              colorScheme={selectedTool === 'triangle' ? 'blue' : 'gray'}
              leftIcon={<AddIcon />}
            >
              삼각형 추가
            </Button>
          </ButtonGroup>

          <Spacer />          <ButtonGroup variant="outline" spacing="4">
            <IconButton
              aria-label="실행 취소"
              icon={<RepeatIcon />}
              onClick={undo}
            />
            <IconButton
              aria-label="다시 실행"
              icon={<RepeatIcon />}
              onClick={undo}
            />
            <IconButton
              aria-label="캔버스 지우기"
              icon={<DeleteIcon />}
              onClick={clearCanvas}
              colorScheme="red"
            />
            <IconButton
              aria-label="선택 삭제"
              icon={<DeleteIcon />}
              onClick={deleteSelected}
            />
            <IconButton
              aria-label="이미지 다운로드"
              icon={<DownloadIcon />}
              onClick={downloadImage}
            />
          </ButtonGroup>
        </HStack>

        <Box w="100%" border="1px" borderColor="gray.200" borderRadius="md" p={4}>
          <canvas ref={canvasRef} style={{ border: '1px solid #ccc' }} />
        </Box>

        {/* Text Controls */}
        {selectedTool === 'text' && (
          <Box w="100%" p={4} border="1px" borderColor="gray.200" borderRadius="md">
            <VStack spacing={4}>
              <HStack w="100%">
                <Input
                  placeholder="추가할 텍스트를 입력하세요"
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  flex="1"
                />
                <Button colorScheme="blue" onClick={addText}>
                  텍스트 추가
                </Button>
              </HStack>
              <HStack w="100%">
                <Text minW="60px">크기:</Text>
                <NumberInput
                  value={fontSize}
                  onChange={(value) => setFontSize(Number(value))}
                  min={8}
                  max={72}
                  w="100px"
                >
                  <NumberInputField />
                  <NumberInputStepper>
                    <NumberIncrementStepper />
                    <NumberDecrementStepper />
                  </NumberInputStepper>
                </NumberInput>
                <Text minW="60px">색상:</Text>
                <Input
                  type="color"
                  value={textColor}
                  onChange={(e) => setTextColor(e.target.value)}
                  w="60px"
                  h="40px"
                  p="1"
                />
              </HStack>
            </VStack>
          </Box>        )}
      </VStack>
    </Container>
  );
};

export default FlyerGenerator;
import React, { useState } from "react";
import {
  Box,
  Card,
  CardBody,
  Heading,
  Text,
  VStack,
  HStack,
  Button,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Select,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  useToast,
  Stepper,
  Step,
  StepIndicator,
  StepStatus,
  StepIcon,
  StepNumber,
  StepTitle,
  StepDescription,
  StepSeparator,
  useSteps,
} from "@chakra-ui/react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";

interface BusinessData {
  name: string;
  category: string;
  description: string;
  latitude: number;
  longitude: number;
  address: string;
  phone: string;
  website: string;
  targetRadius: number;
}

const steps = [
  { title: "기본 정보", description: "비즈니스 기본 정보 입력" },
  { title: "위치 설정", description: "비즈니스 위치 선택" },
  { title: "타겟 설정", description: "타겟 고객층 설정" },
  { title: "완료", description: "설정 완료 및 확인" },
];

const BusinessSetupPage: React.FC = () => {
  const toast = useToast();
  const { activeStep, setActiveStep } = useSteps({
    index: 0,
    count: steps.length,
  });

  const [businessData, setBusinessData] = useState<BusinessData>({
    name: "",
    category: "",
    description: "",
    latitude: 37.5665,
    longitude: 126.978,
    address: "",
    phone: "",
    website: "",
    targetRadius: 1.0,
  });

  const handleNext = () => {
    if (activeStep < steps.length - 1) {
      setActiveStep(activeStep + 1);
    }
  };

  const handlePrevious = () => {
    if (activeStep > 0) {
      setActiveStep(activeStep - 1);
    }
  };

  const handleSubmit = async () => {
    try {
      // API 호출 시뮬레이션
      await new Promise((resolve) => setTimeout(resolve, 1000));

      toast({
        title: "비즈니스 설정 완료",
        description: "성공적으로 비즈니스가 등록되었습니다.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "오류 발생",
        description: "설정 중 오류가 발생했습니다.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const LocationPicker = () => {
    const map = useMapEvents({
      click: (e) => {
        setBusinessData((prev) => ({
          ...prev,
          latitude: e.latlng.lat,
          longitude: e.latlng.lng,
        }));
      },
    });
    return null;
  };

  const renderStepContent = () => {
    switch (activeStep) {
      case 0:
        return (
          <VStack spacing={4} align="stretch">
            <FormControl isRequired>
              <FormLabel>비즈니스 이름</FormLabel>
              <Input
                value={businessData.name}
                onChange={(e) =>
                  setBusinessData((prev) => ({ ...prev, name: e.target.value }))
                }
                placeholder="예: 맛있는 커피숍"
              />
            </FormControl>

            <FormControl isRequired>
              <FormLabel>업종 카테고리</FormLabel>
              <Select
                value={businessData.category}
                onChange={(e) =>
                  setBusinessData((prev) => ({
                    ...prev,
                    category: e.target.value,
                  }))
                }
                placeholder="업종을 선택하세요"
              >
                <option value="cafe">카페</option>
                <option value="restaurant">일반음식점</option>
                <option value="fastfood">패스트푸드</option>
                <option value="bakery">베이커리</option>
                <option value="clothing">의류</option>
                <option value="beauty">미용실</option>
                <option value="fitness">헬스장</option>
              </Select>
            </FormControl>

            <FormControl isRequired>
              <FormLabel>비즈니스 설명</FormLabel>
              <Textarea
                value={businessData.description}
                onChange={(e) =>
                  setBusinessData((prev) => ({
                    ...prev,
                    description: e.target.value,
                  }))
                }
                placeholder="비즈니스에 대한 간단한 설명을 입력하세요"
                rows={4}
              />
            </FormControl>

            <HStack spacing={4}>
              <FormControl>
                <FormLabel>전화번호</FormLabel>
                <Input
                  value={businessData.phone}
                  onChange={(e) =>
                    setBusinessData((prev) => ({
                      ...prev,
                      phone: e.target.value,
                    }))
                  }
                  placeholder="010-1234-5678"
                />
              </FormControl>

              <FormControl>
                <FormLabel>웹사이트</FormLabel>
                <Input
                  value={businessData.website}
                  onChange={(e) =>
                    setBusinessData((prev) => ({
                      ...prev,
                      website: e.target.value,
                    }))
                  }
                  placeholder="https://example.com"
                />
              </FormControl>
            </HStack>
          </VStack>
        );

      case 1:
        return (
          <VStack spacing={4} align="stretch">
            <FormControl>
              <FormLabel>주소</FormLabel>
              <Input
                value={businessData.address}
                onChange={(e) =>
                  setBusinessData((prev) => ({
                    ...prev,
                    address: e.target.value,
                  }))
                }
                placeholder="주소를 입력하거나 지도에서 클릭하세요"
              />
            </FormControl>

            <Text fontSize="sm" color="gray.600">
              지도를 클릭하여 정확한 위치를 선택하세요
            </Text>

            <Box h="400px" borderRadius="md" overflow="hidden">
              <MapContainer
                center={[businessData.latitude, businessData.longitude]}
                zoom={15}
                style={{ height: "100%", width: "100%" }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution="&copy; OpenStreetMap contributors"
                />
                <Marker
                  position={[businessData.latitude, businessData.longitude]}
                />
                <LocationPicker />
              </MapContainer>
            </Box>

            <HStack>
              <Text fontSize="sm">선택된 좌표:</Text>
              <Text fontSize="sm" fontWeight="bold">
                {businessData.latitude.toFixed(6)},{" "}
                {businessData.longitude.toFixed(6)}
              </Text>
            </HStack>
          </VStack>
        );

      case 2:
        return (
          <VStack spacing={6} align="stretch">
            <FormControl>
              <FormLabel>타겟 반경 (km)</FormLabel>
              <NumberInput
                value={businessData.targetRadius}
                onChange={(value) =>
                  setBusinessData((prev) => ({
                    ...prev,
                    targetRadius: parseFloat(value) || 1.0,
                  }))
                }
                min={0.1}
                max={10}
                step={0.1}
              >
                <NumberInputField />
                <NumberInputStepper>
                  <NumberIncrementStepper />
                  <NumberDecrementStepper />
                </NumberInputStepper>
              </NumberInput>
              <Text fontSize="sm" color="gray.500" mt={1}>
                마케팅 타겟으로 할 반경을 설정하세요
              </Text>
            </FormControl>

            <Box p={4} bg="blue.50" borderRadius="md">
              <Text fontSize="sm" fontWeight="bold" mb={2}>
                예상 타겟 정보
              </Text>
              <VStack align="start" spacing={1}>
                <Text fontSize="sm">• 예상 인구: 약 15,000명</Text>
                <Text fontSize="sm">• 주요 연령층: 20-40대</Text>
                <Text fontSize="sm">• 유동인구: 평일 1,200명/일</Text>
                <Text fontSize="sm">
                  • 주요 시간대: 오전 9시, 점심 12시, 오후 6시
                </Text>
              </VStack>
            </Box>
          </VStack>
        );

      case 3:
        return (
          <VStack spacing={6} align="stretch">
            <Card>
              <CardBody>
                <VStack align="start" spacing={3}>
                  <Heading size="md">설정 완료</Heading>
                  <Text color="gray.600">
                    모든 설정이 완료되었습니다. 아래 정보를 확인하고 저장하세요.
                  </Text>

                  <Box w="100%">
                    <VStack align="stretch" spacing={2}>
                      <HStack justify="space-between">
                        <Text fontWeight="bold">비즈니스 이름:</Text>
                        <Text>{businessData.name}</Text>
                      </HStack>
                      <HStack justify="space-between">
                        <Text fontWeight="bold">업종:</Text>
                        <Text>{businessData.category}</Text>
                      </HStack>
                      <HStack justify="space-between">
                        <Text fontWeight="bold">위치:</Text>
                        <Text>{businessData.address || "지도에서 선택됨"}</Text>
                      </HStack>
                      <HStack justify="space-between">
                        <Text fontWeight="bold">타겟 반경:</Text>
                        <Text>{businessData.targetRadius}km</Text>
                      </HStack>
                    </VStack>
                  </Box>
                </VStack>
              </CardBody>
            </Card>
          </VStack>
        );

      default:
        return null;
    }
  };

  return (
    <Box maxW="800px" mx="auto">
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading mb={2}>비즈니스 설정</Heading>
          <Text color="gray.600">
            효과적인 마케팅을 위해 비즈니스 정보를 설정해주세요
          </Text>
        </Box>

        <Stepper index={activeStep} orientation="horizontal">
          {steps.map((step, index) => (
            <Step key={index}>
              <StepIndicator>
                <StepStatus
                  complete={<StepIcon />}
                  incomplete={<StepNumber />}
                  active={<StepNumber />}
                />
              </StepIndicator>

              <Box flexShrink="0">
                <StepTitle>{step.title}</StepTitle>
                <StepDescription>{step.description}</StepDescription>
              </Box>

              <StepSeparator />
            </Step>
          ))}
        </Stepper>

        <Card>
          <CardBody>
            {renderStepContent()}

            <HStack justify="space-between" mt={8}>
              <Button
                onClick={handlePrevious}
                disabled={activeStep === 0}
                variant="outline"
              >
                이전
              </Button>

              {activeStep === steps.length - 1 ? (
                <Button colorScheme="brand" onClick={handleSubmit}>
                  설정 저장
                </Button>
              ) : (
                <Button
                  colorScheme="brand"
                  onClick={handleNext}
                  disabled={
                    (activeStep === 0 &&
                      (!businessData.name ||
                        !businessData.category ||
                        !businessData.description)) ||
                    (activeStep === 1 &&
                      (!businessData.latitude || !businessData.longitude))
                  }
                >
                  다음
                </Button>
              )}
            </HStack>
          </CardBody>
        </Card>
      </VStack>
    </Box>
  );
};

export default BusinessSetupPage;

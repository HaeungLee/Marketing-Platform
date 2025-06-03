import React, { useState } from "react";
import {
  Box,
  Text,
  VStack,
  HStack,
  Button,
  Textarea,
  Input,
  useToast,
  Image,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  FormControl,
  FormLabel,
  Select,
} from "@chakra-ui/react";
import apiClient from "../services/api";
import { contentApi } from "../services/apiService";
import type { ImageGenerationResponse } from "../types/api";

const ContentGeneratorPage: React.FC = () => {
  // 텍스트 콘텐츠 생성 상태
  const [businessName, setBusinessName] = useState("");
  const [businessCategory, setBusinessCategory] = useState("");
  const [businessDescription, setBusinessDescription] = useState("");
  const [productName, setProductName] = useState("");
  const [productDescription, setProductDescription] = useState("");
  const [contentType, setContentType] = useState("blog");
  const [tone, setTone] = useState("친근한");
  const [response, setResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // 이미지 생성 상태
  const [imagePrompt, setImagePrompt] = useState("");
  const [imageStyle, setImageStyle] = useState("professional");
  const [generatedImage, setGeneratedImage] =
    useState<ImageGenerationResponse | null>(null);
  const [isImageLoading, setIsImageLoading] = useState(false);

  const toast = useToast();
  const handleGenerate = async () => {
    if (!businessName.trim() || !productName.trim()) {
      toast({
        title: "입력 오류",
        description: "비즈니스명과 상품명을 입력해주세요.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);

    try {
      const requestData = {
        business_id: `business-${Date.now()}`,
        business_name: businessName,
        business_category: businessCategory || "일반",
        business_description:
          businessDescription || "우수한 서비스를 제공하는 비즈니스",
        product_name: productName,
        product_description: productDescription || "고품질의 상품/서비스",
        content_type: contentType,
        tone: tone,
        keywords: [],
      };

      const response = await fetch(
        "http://localhost:8001/api/v1/content/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      setResponse(data.content);

      toast({
        title: "성공",
        description: "콘텐츠가 성공적으로 생성되었습니다!",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error: any) {
      console.error("콘텐츠 생성 오류:", error);
      toast({
        title: "오류 발생",
        description:
          error.response?.data?.detail || "콘텐츠 생성 중 오류가 발생했습니다.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleImageGenerate = async () => {
    if (!imagePrompt.trim()) {
      toast({
        title: "입력 오류",
        description: "이미지 프롬프트를 입력해주세요.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsImageLoading(true);

    try {
      const result = await contentApi.generateImage({
        prompt: imagePrompt,
        business_name: businessName || undefined,
        business_category: businessCategory || undefined,
        style: imageStyle,
      });

      if (result.success) {
        setGeneratedImage(result);
        toast({
          title: "성공",
          description: "이미지가 성공적으로 생성되었습니다!",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
      } else {
        toast({
          title: "생성 실패",
          description: result.error || "이미지 생성에 실패했습니다.",
          status: "error",
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error: any) {
      toast({
        title: "오류 발생",
        description:
          error.response?.data?.detail || "이미지 생성 중 오류가 발생했습니다.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsImageLoading(false);
    }
  };

  return (
    <Box p={6}>
      <Text fontSize="2xl" fontWeight="bold" mb={6}>
        AI 콘텐츠 생성
      </Text>

      <Tabs>
        <TabList>
          <Tab>텍스트 콘텐츠</Tab>
          <Tab>이미지 생성</Tab>
        </TabList>

        <TabPanels>
          {" "}
          {/* 텍스트 콘텐츠 생성 탭 */}
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <FormControl>
                <FormLabel>비즈니스명</FormLabel>
                <Input
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  placeholder="예: 맛있는 베이커리"
                />
              </FormControl>

              <FormControl>
                <FormLabel>업종/카테고리</FormLabel>
                <Input
                  value={businessCategory}
                  onChange={(e) => setBusinessCategory(e.target.value)}
                  placeholder="예: 베이커리, 카페, 온라인쇼핑몰"
                />
              </FormControl>

              <FormControl>
                <FormLabel>비즈니스 설명</FormLabel>
                <Textarea
                  value={businessDescription}
                  onChange={(e) => setBusinessDescription(e.target.value)}
                  placeholder="비즈니스에 대한 간단한 설명을 입력하세요..."
                  rows={2}
                />
              </FormControl>

              <FormControl>
                <FormLabel>상품/서비스명</FormLabel>
                <Input
                  value={productName}
                  onChange={(e) => setProductName(e.target.value)}
                  placeholder="예: 수제 크루아상, 프리미엄 원두"
                />
              </FormControl>

              <FormControl>
                <FormLabel>상품/서비스 설명</FormLabel>
                <Textarea
                  value={productDescription}
                  onChange={(e) => setProductDescription(e.target.value)}
                  placeholder="상품/서비스에 대한 자세한 설명을 입력하세요..."
                  rows={3}
                />
              </FormControl>

              <HStack spacing={4}>
                <FormControl>
                  <FormLabel>콘텐츠 타입</FormLabel>
                  <Select
                    value={contentType}
                    onChange={(e) => setContentType(e.target.value)}
                  >
                    <option value="blog">블로그 포스트</option>
                    <option value="instagram">인스타그램</option>
                    <option value="youtube">유튜브</option>
                    <option value="flyer">플라이어</option>
                  </Select>
                </FormControl>

                <FormControl>
                  <FormLabel>톤앤매너</FormLabel>
                  <Select
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                  >
                    <option value="친근한">친근한</option>
                    <option value="전문적인">전문적인</option>
                    <option value="캐주얼한">캐주얼한</option>
                    <option value="공식적인">공식적인</option>
                  </Select>
                </FormControl>
              </HStack>

              <Button
                colorScheme="blue"
                onClick={handleGenerate}
                isLoading={isLoading}
                loadingText="생성 중..."
                size="lg"
              >
                콘텐츠 생성
              </Button>

              {response && (
                <Box
                  p={4}
                  border="1px"
                  borderColor="gray.200"
                  borderRadius="md"
                  bg="gray.50"
                >
                  <Text fontWeight="bold" mb={2}>
                    생성된 콘텐츠:
                  </Text>
                  <Text whiteSpace="pre-wrap">{response}</Text>
                </Box>
              )}
            </VStack>
          </TabPanel>
          {/* 이미지 생성 탭 */}
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <HStack spacing={4}>
                <FormControl flex={1}>
                  <FormLabel>비즈니스명</FormLabel>
                  <Input
                    value={businessName}
                    onChange={(e) => setBusinessName(e.target.value)}
                    placeholder="예: 카페 모카"
                  />
                </FormControl>
                <FormControl flex={1}>
                  <FormLabel>비즈니스 카테고리</FormLabel>
                  <Input
                    value={businessCategory}
                    onChange={(e) => setBusinessCategory(e.target.value)}
                    placeholder="예: 카페/음료"
                  />
                </FormControl>
              </HStack>

              <FormControl>
                <FormLabel>이미지 스타일</FormLabel>
                <Select
                  value={imageStyle}
                  onChange={(e) => setImageStyle(e.target.value)}
                >
                  <option value="professional">전문적인</option>
                  <option value="casual">캐주얼</option>
                  <option value="modern">모던</option>
                  <option value="vintage">빈티지</option>
                  <option value="minimalist">미니멀</option>
                </Select>
              </FormControl>

              <FormControl>
                <FormLabel>이미지 프롬프트</FormLabel>
                <Textarea
                  value={imagePrompt}
                  onChange={(e) => setImagePrompt(e.target.value)}
                  placeholder="생성하고 싶은 이미지를 설명하세요... 예: 따뜻한 조명의 아늑한 카페 인테리어"
                  rows={4}
                />
              </FormControl>

              <Button
                colorScheme="green"
                onClick={handleImageGenerate}
                isLoading={isImageLoading}
                loadingText="이미지 생성 중..."
                size="lg"
              >
                이미지 생성
              </Button>

              {generatedImage && generatedImage.success && (
                <Box
                  p={4}
                  border="1px"
                  borderColor="gray.200"
                  borderRadius="md"
                  bg="gray.50"
                >
                  <Text fontWeight="bold" mb={4}>
                    생성된 이미지:
                  </Text>
                  <Image
                    src={`http://127.0.0.1:8001${generatedImage.image_url}`}
                    alt="Generated marketing image"
                    maxW="100%"
                    borderRadius="md"
                    boxShadow="md"
                  />
                  <Text fontSize="sm" color="gray.600" mt={2}>
                    파일명: {generatedImage.filename}
                  </Text>
                  <Text fontSize="sm" color="gray.500" mt={1}>
                    생성 시간:{" "}
                    {new Date(generatedImage.created_at).toLocaleString()}
                  </Text>
                </Box>
              )}
            </VStack>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default ContentGeneratorPage;

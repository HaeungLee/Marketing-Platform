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
  Badge,
  Heading,
} from "@chakra-ui/react";
import { DownloadIcon, RepeatIcon } from "@chakra-ui/icons";
import apiClient from "../services/api";
import { contentApi } from "../services/apiService";
import type { ImageGenerationResponse } from "../types/api";

const ContentGeneratorPage: React.FC = () => {
  // 단순화된 텍스트 콘텐츠 생성 상태
  const [prompt, setPrompt] = useState("");
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
    if (!prompt.trim()) {
      toast({
        title: "입력 오류",
        description: "프롬프트를 입력해주세요.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    console.log("콘텐츠 생성 요청 시작...");

    try {
      // 요청을 단순화: prompt만 포함
      const requestData = {
        prompt: prompt.trim(),
        // content_type과 tone은 백엔드에서 기본값 사용
      };

      console.log("단순화된 요청 데이터:", requestData);

      // CORS 디버깅을 위한 로깅
      console.log("API 요청 URL:", "http://localhost:8000/api/v1/content/generate/simple");

      const response = await fetch(
        "http://localhost:8000/api/v1/content/generate/simple",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": window.location.origin
          },
          body: JSON.stringify(requestData),
          credentials: "omit" // CORS 이슈 해결을 위해 credentials 제외
        }
      );

      console.log("응답 상태:", response.status);
      console.log("응답 헤더:", [...response.headers.entries()]);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("API 오류 응답:", errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      
      const data = await response.json();
      console.log("응답 데이터:", data);

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
          error.response?.data?.detail || error.message || "콘텐츠 생성 중 오류가 발생했습니다.",
        status: "error",
        duration: 5000,
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
      <VStack spacing={4} align="stretch" mb={6}>
        <Heading size="lg" color="gray.800">
          📝 콘텐츠 생성 & 전단지 제작
        </Heading>
        <Text color="gray.600">
          AI 기반 마케팅 콘텐츠와 전단지를 한 번에 생성하세요
        </Text>
      </VStack>

      <Tabs variant="enclosed" colorScheme="brand">
        <TabList>
          <Tab>📝 텍스트 콘텐츠</Tab>
          <Tab>🖼️ 이미지 생성</Tab>
          <Tab>📄 전단지 제작</Tab>
        </TabList>

        <TabPanels>
          {" "}
          {/* 텍스트 콘텐츠 생성 탭 */}
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <Box mb={4}>
                <Heading size="md" mb={3}>빠른 콘텐츠 생성기</Heading>
                <Text fontSize="sm" color="gray.600">
                  원하는 내용을 프롬프트로 입력하면 AI가 해당 내용에 맞는 콘텐츠를 생성합니다.
                  구체적인 프롬프트일수록 더 좋은 결과를 얻을 수 있습니다.
                </Text>
              </Box>

              <FormControl>
                <FormLabel>
                  프롬프트 입력
                  <Badge ml={2} colorScheme="green">AI 프롬프트</Badge>
                </FormLabel>
                <Textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="원하는 마케팅 콘텐츠에 대해 상세히 설명해주세요. 예: '저는 서울 강남에 위치한 프리미엄 베이커리를 운영하고 있습니다. 수제 크루아상의 장점과 특별한 재료를 강조하는 블로그 글을 작성해주세요.'"
                  rows={6}
                  size="md"
                /></FormControl>

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
              <Box mb={4}>
                <Heading size="md" mb={3}>AI 이미지 생성기</Heading>
                <Text fontSize="sm" color="gray.600">
                  원하는 이미지에 대한 설명을 입력하면 AI가 해당 이미지를 생성합니다.
                  구체적인 설명일수록 더 좋은 결과를 얻을 수 있습니다.
                </Text>
              </Box>

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
                  {generatedImage.image_data ? (
                    <Image
                      src={`data:image/png;base64,${generatedImage.image_data}`}
                      alt="Generated marketing image"
                      maxW="100%"
                      borderRadius="md"
                      boxShadow="md"
                    />
                  ) : generatedImage.image_url ? (
                    <Image
                      src={`http://localhost:8000${generatedImage.image_url}`}
                      alt="Generated marketing image"
                      maxW="100%"
                      borderRadius="md"
                      boxShadow="md"
                    />
                  ) : (
                    <Text color="red.500">이미지를 표시할 수 없습니다.</Text>
                  )}
                  <Text fontSize="sm" color="gray.600" mt={2}>
                    파일명: {generatedImage.filename}
                  </Text>
                  <Text fontSize="sm" color="gray.500" mt={1}>
                    생성 시간: {generatedImage.created_at ? new Date(generatedImage.created_at).toLocaleString() : "방금 전"}
                  </Text>
                </Box>
              )}
            </VStack>
          </TabPanel>

          {/* 전단지 제작 탭 */}
          <TabPanel>
            <VStack spacing={6} align="stretch">
              <Box mb={4}>
                <Heading size="md" mb={3}>🎨 AI 전단지 생성기</Heading>
                <Text fontSize="sm" color="gray.600">
                  원하는 전단지 스타일과 내용을 설명하면 AI가 전단지 이미지를 생성합니다.
                  구체적인 디자인 요소와 텍스트 내용을 포함하여 설명해주세요.
                </Text>
              </Box>

              <FormControl>
                <FormLabel>전단지 디자인 프롬프트</FormLabel>
                <Textarea
                  placeholder="예: 모던한 스타일의 카페 전단지, 빨간색과 흰색 테마, '신메뉴 출시' 텍스트 포함, 미니멀한 디자인"
                  value={imagePrompt}
                  onChange={(e) => setImagePrompt(e.target.value)}
                  rows={4}
                />
              </FormControl>

              <FormControl>
                <FormLabel>디자인 스타일</FormLabel>
                <Select
                  value={imageStyle}
                  onChange={(e) => setImageStyle(e.target.value)}
                >
                  <option value="professional">프로페셔널</option>
                  <option value="casual">캐주얼</option>
                  <option value="modern">모던</option>
                  <option value="vintage">빈티지</option>
                  <option value="minimalist">미니멀</option>
                </Select>
              </FormControl>

              <Button
                colorScheme="brand"
                size="lg"
                onClick={handleImageGenerate}
                isLoading={isImageLoading}
                loadingText="전단지 생성 중..."
              >
                🎨 전단지 생성하기
              </Button>

              {generatedImage && (
                <Box>
                  <Text fontWeight="bold" mb={3}>
                    생성된 전단지:
                  </Text>
                  <Box
                    border="2px"
                    borderColor="gray.200"
                    borderRadius="md"
                    overflow="hidden"
                    maxW="500px"
                    mx="auto"
                  >
                    {generatedImage.image_data ? (
                      <Image
                        src={`data:image/png;base64,${generatedImage.image_data}`}
                        alt="Generated Flyer"
                        width="100%"
                        height="auto"
                      />
                    ) : generatedImage.image_url ? (
                      <Image
                        src={`http://localhost:8000${generatedImage.image_url}`}
                        alt="Generated Flyer"
                        width="100%"
                        height="auto"
                      />
                    ) : (
                      <Text color="red.500">이미지를 표시할 수 없습니다.</Text>
                    )}
                   </Box>
                   <HStack justify="center" mt={4}>
                     <Button
                       leftIcon={<DownloadIcon />}
                       colorScheme="blue"
                       onClick={() => {
                         if (generatedImage?.image_data) {
                           const link = document.createElement('a');
                           link.download = 'generated-flyer.png';
                           link.href = `data:image/png;base64,${generatedImage.image_data}`;
                           link.click();
                         } else if (generatedImage?.image_url) {
                           const link = document.createElement('a');
                           link.download = 'generated-flyer.png';
                           link.href = `http://localhost:8000${generatedImage.image_url}`;
                           link.click();
                         }
                       }}
                    >
                      다운로드
                    </Button>
                    <Button
                      leftIcon={<RepeatIcon />}
                      variant="outline"
                      onClick={() => setGeneratedImage(null)}
                    >
                      새로 생성
                    </Button>
                  </HStack>
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

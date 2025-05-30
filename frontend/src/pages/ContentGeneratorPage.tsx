import React, { useState } from "react";
import {
  Box,
  Text,
  VStack,
  HStack,
  Card,
  CardBody,
  CardHeader,
  Button,
  Textarea,
  Select,
  Input,
  Badge,
  Grid,
  GridItem,
  useToast,
  Spinner,
  IconButton,
  Divider,
  FormControl,
  FormLabel,
} from "@chakra-ui/react";
import {
  FaInstagram,
  FaBlog,
  FaYoutube,
  FaFileAlt,
  FaCopy,
  FaSync,
  FaRobot,
} from "react-icons/fa";
import apiClient from "../services/api";

interface GeneratedContent {
  type: "blog" | "instagram" | "youtube" | "flyer";
  title: string;
  content: string;
  hashtags: string[];
}

const ContentGeneratorPage: React.FC = () => {
  const [selectedType, setSelectedType] = useState<
    "blog" | "instagram" | "youtube" | "flyer"
  >("blog");
  const [prompt, setPrompt] = useState("");
  const [product, setProduct] = useState("");
  const [tone, setTone] = useState("friendly");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] =
    useState<GeneratedContent | null>(null);
  const toast = useToast();

  const contentTypes = [
    { id: "blog", label: "네이버 블로그", icon: FaBlog, color: "green" },
    { id: "instagram", label: "인스타그램", icon: FaInstagram, color: "pink" },
    { id: "youtube", label: "유튜브 숏폼", icon: FaYoutube, color: "red" },
    { id: "flyer", label: "전단지", icon: FaFileAlt, color: "blue" },
  ];

  const toneOptions = [
    { value: "friendly", label: "친근한" },
    { value: "professional", label: "전문적인" },
    { value: "casual", label: "캐주얼한" },
    { value: "formal", label: "격식 있는" },
  ];

  const handleGenerate = async () => {
    if (!prompt.trim() || !product.trim()) {
      toast({
        title: "입력 오류",
        description: "상품 정보와 홍보 내용을 모두 입력해주세요.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsGenerating(true);

    try {
      const { data } = await apiClient.post("/content/generate", {
        business_id: "demo",
        business_name: "데모 비즈니스",
        business_category: "retail",
        business_description: "고품질 제품을 판매하는 리테일 비즈니스",
        product_name: product,
        product_description: prompt,
        content_type: selectedType,
        tone: tone,
        target_audience: {
          age_group: "20-50",
          interests: ["shopping", "quality", "value"],
        },
      });

      setGeneratedContent({
        type: selectedType,
        title: data.title || `${product} 마케팅`,
        content: data.content,
        hashtags: data.hashtags || [],
      });

      toast({
        title: "콘텐츠 생성 완료",
        description: "새로운 마케팅 콘텐츠가 생성되었습니다.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail ||
        error.message ||
        (error.code === "ECONNABORTED"
          ? "요청 시간이 초과되었습니다. 다시 시도해주세요."
          : "콘텐츠 생성 중 오류가 발생했습니다.");

      toast({
        title: "오류 발생",
        description: errorMessage,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "복사 완료",
      description: "클립보드에 복사되었습니다.",
      status: "success",
      duration: 2000,
      isClosable: true,
    });
  };

  return (
    <Box>
      <Text fontSize="2xl" fontWeight="bold" mb={6}>
        AI 콘텐츠 생성
      </Text>

      <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} gap={6}>
        <GridItem>
          <Card>
            <CardHeader>
              <HStack justify="space-between">
                <Text fontSize="lg" fontWeight="bold">
                  콘텐츠 생성 설정
                </Text>
                <Badge
                  colorScheme={
                    contentTypes.find((t) => t.id === selectedType)?.color ||
                    "gray"
                  }
                >
                  {contentTypes.find((t) => t.id === selectedType)?.label}
                </Badge>
              </HStack>
            </CardHeader>
            <CardBody>
              <VStack spacing={4} align="stretch">
                {/* Content Type Selection */}
                <Grid templateColumns="repeat(2, 1fr)" gap={3}>
                  {contentTypes.map((type) => (
                    <GridItem key={type.id}>
                      <Card
                        cursor="pointer"
                        bg={
                          selectedType === type.id
                            ? `${type.color}.50`
                            : "white"
                        }
                        borderColor={
                          selectedType === type.id
                            ? `${type.color}.200`
                            : "gray.200"
                        }
                        borderWidth="2px"
                        onClick={() => setSelectedType(type.id as any)}
                        _hover={{ transform: "translateY(-2px)", shadow: "md" }}
                        transition="all 0.2s"
                      >
                        <CardBody p={4} textAlign="center">
                          <VStack spacing={2}>
                            <Box
                              as={type.icon}
                              size="24px"
                              color={`${type.color}.500`}
                            />
                            <Text fontSize="sm" fontWeight="medium">
                              {type.label}
                            </Text>
                          </VStack>
                        </CardBody>
                      </Card>
                    </GridItem>
                  ))}
                </Grid>

                <Divider />

                {/* Product Input */}
                <FormControl>
                  <FormLabel>홍보할 상품/서비스</FormLabel>
                  <Input
                    placeholder="예: 수제 케이크, 헤어컷 서비스, 온라인 쇼핑몰"
                    value={product}
                    onChange={(e) => setProduct(e.target.value)}
                  />
                </FormControl>

                {/* Prompt Input */}
                <FormControl>
                  <FormLabel>홍보 내용 및 특징</FormLabel>
                  <Textarea
                    placeholder="상품의 특징, 장점, 할인 정보 등을 자세히 입력해주세요..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    rows={4}
                  />
                </FormControl>

                {/* Tone Selection */}
                <FormControl>
                  <FormLabel>톤앤매너</FormLabel>
                  <Select
                    value={tone}
                    onChange={(e) => setTone(e.target.value)}
                  >
                    {toneOptions.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </Select>
                </FormControl>

                <Button
                  leftIcon={<FaRobot />}
                  colorScheme="blue"
                  size="lg"
                  onClick={handleGenerate}
                  isLoading={isGenerating}
                  loadingText="AI가 콘텐츠를 생성 중..."
                >
                  콘텐츠 생성하기
                </Button>
              </VStack>
            </CardBody>
          </Card>
        </GridItem>

        <GridItem>
          {isGenerating ? (
            <Card>
              <CardBody textAlign="center" py={20}>
                <VStack spacing={4}>
                  <Spinner size="xl" color="blue.500" />
                  <Text>AI가 최적의 콘텐츠를 생성하고 있습니다...</Text>
                  <Text fontSize="sm" color="gray.600">
                    잠시만 기다려주세요. 보통 10-30초 정도 소요됩니다.
                  </Text>
                </VStack>
              </CardBody>
            </Card>
          ) : generatedContent ? (
            <Card>
              <CardHeader>
                <HStack justify="space-between">
                  <Text fontSize="lg" fontWeight="bold">
                    생성된 콘텐츠
                  </Text>
                  <HStack>
                    <IconButton
                      aria-label="Refresh"
                      icon={<FaSync />}
                      size="sm"
                      onClick={handleGenerate}
                    />
                    <IconButton
                      aria-label="Copy"
                      icon={<FaCopy />}
                      size="sm"
                      onClick={() => handleCopy(generatedContent.content)}
                    />
                  </HStack>
                </HStack>
              </CardHeader>
              <CardBody>
                <VStack spacing={4} align="stretch">
                  <Box>
                    <Text fontWeight="bold" mb={2}>
                      제목
                    </Text>
                    <Text bg="gray.50" p={3} borderRadius="md">
                      {generatedContent.title}
                    </Text>
                  </Box>

                  <Box>
                    <Text fontWeight="bold" mb={2}>
                      내용
                    </Text>
                    <Textarea
                      value={generatedContent.content}
                      readOnly
                      rows={8}
                      bg="gray.50"
                    />
                  </Box>

                  <Box>
                    <Text fontWeight="bold" mb={2}>
                      해시태그
                    </Text>
                    <HStack wrap="wrap">
                      {generatedContent.hashtags.map((tag, index) => (
                        <Badge
                          key={index}
                          colorScheme="blue"
                          cursor="pointer"
                          onClick={() => handleCopy(`#${tag}`)}
                        >
                          #{tag}
                        </Badge>
                      ))}
                    </HStack>
                  </Box>
                </VStack>
              </CardBody>
            </Card>
          ) : (
            <Card>
              <CardBody textAlign="center" py={20}>
                <VStack spacing={4}>
                  <Box as={FaRobot} size="48px" color="gray.400" />
                  <Text color="gray.600">
                    왼쪽에서 설정을 완료하고 "콘텐츠 생성하기" 버튼을
                    눌러주세요.
                  </Text>
                  <Text fontSize="sm" color="gray.500">
                    AI가 귀하의 비즈니스에 최적화된 마케팅 콘텐츠를
                    생성해드립니다.
                  </Text>
                </VStack>
              </CardBody>
            </Card>
          )}
        </GridItem>
      </Grid>
    </Box>
  );
};

export default ContentGeneratorPage;

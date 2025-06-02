import React, { useState } from "react";
import {
  Box,
  Text,
  VStack,
  Button,
  Textarea,
  useToast,
  Spinner,
} from "@chakra-ui/react";
import apiClient from "../services/api";

const ContentGeneratorPage: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);
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

    try {
      const { data } = await apiClient.post("/content/generate", {
        prompt: prompt
      });

      setResponse(data.content);
    } catch (error: any) {
      toast({
        title: "오류 발생",
        description: error.response?.data?.detail || "콘텐츠 생성 중 오류가 발생했습니다.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box p={6}>
      <Text fontSize="2xl" fontWeight="bold" mb={6}>
        AI 콘텐츠 생성
      </Text>

      <VStack spacing={4} align="stretch">
        <Textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="생성하고 싶은 내용을 입력하세요..."
          size="lg"
          rows={5}
        />

        <Button
          colorScheme="blue"
          onClick={handleGenerate}
          isLoading={isLoading}
          loadingText="생성 중..."
        >
          생성하기
        </Button>

        {response && (
          <Box
            mt={4}
            p={4}
            borderWidth={1}
            borderRadius="md"
            bg="gray.50"
          >
            <Text whiteSpace="pre-wrap">{response}</Text>
          </Box>
        )}
      </VStack>
    </Box>
  );
};

export default ContentGeneratorPage;

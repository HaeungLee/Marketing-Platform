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
  Input,
  Textarea,
  Switch,
  Select,
  Divider,
  FormControl,
  FormLabel,
  FormHelperText,
  Grid,
  Badge,
  Avatar,
  useToast,
  Alert,
  AlertIcon,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  useColorModeValue,
} from "@chakra-ui/react";
import {
  FaUser,
  FaBell,
  FaLock,
  FaCog,
  FaEdit,
  FaGoogle,
  FaBlog,
} from "react-icons/fa";

interface ConnectedAccount {
  platform: string;
  name: string;
  connected: boolean;
  email?: string;
  id?: string;
}

const SettingsPage: React.FC = () => {
  const [userInfo, setUserInfo] = useState({
    name: "홍길동",
    email: "hong@example.com",
    phone: "010-1234-5678",
    company: "홍길동 케이크샵",
    description: "수제 케이크 전문점을 운영하고 있습니다.",
  });

  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    sms: true,
    marketing: false,
  });

  const [aiSettings, setAiSettings] = useState({
    creativity: 70,
    tone: "friendly",
    language: "ko",
    autoGenerate: false,
  });

  const [connectedAccounts, setConnectedAccounts] = useState<
    ConnectedAccount[]
  >([
    {
      platform: "google",
      name: "Google",
      connected: true,
      email: "hong@gmail.com",
    },
    {
      platform: "naver",
      name: "네이버 블로그",
      connected: true,
      id: "hongcake",
    },
    { platform: "instagram", name: "Instagram", connected: false },
    { platform: "youtube", name: "YouTube", connected: false },
  ]);

  const toast = useToast();
  const cardBg = useColorModeValue("white", "gray.800");
  const borderColor = useColorModeValue("gray.200", "gray.700");

  const handleSaveProfile = () => {
    toast({
      title: "프로필 저장 완료",
      description: "프로필 정보가 성공적으로 업데이트되었습니다.",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  const handleSaveNotifications = () => {
    toast({
      title: "알림 설정 저장 완료",
      description: "알림 설정이 성공적으로 업데이트되었습니다.",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
  };

  const handleConnectAccount = (platform: string) => {
    toast({
      title: "계정 연동",
      description: `${platform} 계정 연동을 시작합니다...`,
      status: "info",
      duration: 3000,
      isClosable: true,
    });
  };

  const handleDisconnectAccount = (platform: string) => {
    setConnectedAccounts((prev) =>
      prev.map((acc) =>
        acc.platform === platform
          ? { ...acc, connected: false, email: undefined, id: undefined }
          : acc
      )
    );
    toast({
      title: "계정 연동 해제",
      description: `${platform} 계정 연동이 해제되었습니다.`,
      status: "warning",
      duration: 3000,
      isClosable: true,
    });
  };

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case "google":
        return FaGoogle;
      case "naver":
        return FaBlog;
      default:
        return FaCog;
    }
  };

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case "google":
        return "red";
      case "naver":
        return "green";
      default:
        return "gray";
    }
  };

  return (
    <Box>
      <Text fontSize="2xl" fontWeight="bold" mb={6}>
        설정
      </Text>

      <Tabs>
        <TabList>
          <Tab>
            <HStack>
              <FaUser />
              <Text>프로필</Text>
            </HStack>
          </Tab>
          <Tab>
            <HStack>
              <FaBell />
              <Text>알림</Text>
            </HStack>
          </Tab>
          <Tab>
            <HStack>
              <FaCog />
              <Text>AI 설정</Text>
            </HStack>
          </Tab>
          <Tab>
            <HStack>
              <FaLock />
              <Text>계정 연동</Text>
            </HStack>
          </Tab>
        </TabList>

        <TabPanels>
          {/* 프로필 설정 */}
          <TabPanel p={0} pt={6}>
            <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} gap={6}>
              <Card bg={cardBg} borderColor={borderColor}>
                <CardHeader>
                  <Text fontSize="lg" fontWeight="bold">
                    기본 정보
                  </Text>
                </CardHeader>
                <CardBody>
                  <VStack spacing={4} align="stretch">
                    <HStack spacing={4}>
                      <Avatar size="lg" name={userInfo.name} />
                      <VStack align="start">
                        <Button size="sm" leftIcon={<FaEdit />}>
                          프로필 사진 변경
                        </Button>
                        <Text fontSize="sm" color="gray.600">
                          JPG, PNG 파일만 가능
                        </Text>
                      </VStack>
                    </HStack>

                    <FormControl>
                      <FormLabel>이름</FormLabel>
                      <Input
                        value={userInfo.name}
                        onChange={(e) =>
                          setUserInfo((prev) => ({
                            ...prev,
                            name: e.target.value,
                          }))
                        }
                      />
                    </FormControl>

                    <FormControl>
                      <FormLabel>이메일</FormLabel>
                      <Input
                        type="email"
                        value={userInfo.email}
                        onChange={(e) =>
                          setUserInfo((prev) => ({
                            ...prev,
                            email: e.target.value,
                          }))
                        }
                      />
                    </FormControl>

                    <FormControl>
                      <FormLabel>연락처</FormLabel>
                      <Input
                        value={userInfo.phone}
                        onChange={(e) =>
                          setUserInfo((prev) => ({
                            ...prev,
                            phone: e.target.value,
                          }))
                        }
                      />
                    </FormControl>

                    <Button colorScheme="blue" onClick={handleSaveProfile}>
                      프로필 저장
                    </Button>
                  </VStack>
                </CardBody>
              </Card>

              <Card bg={cardBg} borderColor={borderColor}>
                <CardHeader>
                  <Text fontSize="lg" fontWeight="bold">
                    비즈니스 정보
                  </Text>
                </CardHeader>
                <CardBody>
                  <VStack spacing={4} align="stretch">
                    <FormControl>
                      <FormLabel>사업체명</FormLabel>
                      <Input
                        value={userInfo.company}
                        onChange={(e) =>
                          setUserInfo((prev) => ({
                            ...prev,
                            company: e.target.value,
                          }))
                        }
                      />
                    </FormControl>

                    <FormControl>
                      <FormLabel>사업 설명</FormLabel>
                      <Textarea
                        value={userInfo.description}
                        onChange={(e) =>
                          setUserInfo((prev) => ({
                            ...prev,
                            description: e.target.value,
                          }))
                        }
                        rows={4}
                      />
                      <FormHelperText>
                        AI 콘텐츠 생성 시 참고되는 정보입니다.
                      </FormHelperText>
                    </FormControl>

                    <Alert status="info">
                      <AlertIcon />
                      비즈니스 정보가 정확할수록 더 나은 AI 콘텐츠를 생성할 수
                      있습니다.
                    </Alert>
                  </VStack>
                </CardBody>
              </Card>
            </Grid>
          </TabPanel>

          {/* 알림 설정 */}
          <TabPanel p={0} pt={6}>
            <Card bg={cardBg} borderColor={borderColor} maxW="600px">
              <CardHeader>
                <Text fontSize="lg" fontWeight="bold">
                  알림 설정
                </Text>
              </CardHeader>
              <CardBody>
                <VStack spacing={6} align="stretch">
                  <FormControl
                    display="flex"
                    alignItems="center"
                    justifyContent="space-between"
                  >
                    <Box>
                      <FormLabel mb="0">이메일 알림</FormLabel>
                      <FormHelperText>
                        콘텐츠 생성 완료 시 이메일로 알림을 받습니다.
                      </FormHelperText>
                    </Box>
                    <Switch
                      isChecked={notifications.email}
                      onChange={(e) =>
                        setNotifications((prev) => ({
                          ...prev,
                          email: e.target.checked,
                        }))
                      }
                    />
                  </FormControl>

                  <Divider />

                  <FormControl
                    display="flex"
                    alignItems="center"
                    justifyContent="space-between"
                  >
                    <Box>
                      <FormLabel mb="0">푸시 알림</FormLabel>
                      <FormHelperText>
                        브라우저 푸시 알림을 받습니다.
                      </FormHelperText>
                    </Box>
                    <Switch
                      isChecked={notifications.push}
                      onChange={(e) =>
                        setNotifications((prev) => ({
                          ...prev,
                          push: e.target.checked,
                        }))
                      }
                    />
                  </FormControl>

                  <Divider />

                  <FormControl
                    display="flex"
                    alignItems="center"
                    justifyContent="space-between"
                  >
                    <Box>
                      <FormLabel mb="0">SMS 알림</FormLabel>
                      <FormHelperText>
                        중요한 업데이트를 SMS로 받습니다.
                      </FormHelperText>
                    </Box>
                    <Switch
                      isChecked={notifications.sms}
                      onChange={(e) =>
                        setNotifications((prev) => ({
                          ...prev,
                          sms: e.target.checked,
                        }))
                      }
                    />
                  </FormControl>

                  <Divider />

                  <FormControl
                    display="flex"
                    alignItems="center"
                    justifyContent="space-between"
                  >
                    <Box>
                      <FormLabel mb="0">마케팅 정보</FormLabel>
                      <FormHelperText>
                        새로운 기능 및 팁에 대한 정보를 받습니다.
                      </FormHelperText>
                    </Box>
                    <Switch
                      isChecked={notifications.marketing}
                      onChange={(e) =>
                        setNotifications((prev) => ({
                          ...prev,
                          marketing: e.target.checked,
                        }))
                      }
                    />
                  </FormControl>

                  <Button colorScheme="blue" onClick={handleSaveNotifications}>
                    알림 설정 저장
                  </Button>
                </VStack>
              </CardBody>
            </Card>
          </TabPanel>

          {/* AI 설정 */}
          <TabPanel p={0} pt={6}>
            <Card bg={cardBg} borderColor={borderColor} maxW="600px">
              <CardHeader>
                <Text fontSize="lg" fontWeight="bold">
                  AI 콘텐츠 생성 설정
                </Text>
              </CardHeader>
              <CardBody>
                <VStack spacing={6} align="stretch">
                  <FormControl>
                    <FormLabel>창의성 수준: {aiSettings.creativity}%</FormLabel>
                    <Input
                      type="range"
                      min="0"
                      max="100"
                      value={aiSettings.creativity}
                      onChange={(e) =>
                        setAiSettings((prev) => ({
                          ...prev,
                          creativity: parseInt(e.target.value),
                        }))
                      }
                    />
                    <FormHelperText>
                      높을수록 더 창의적이고 독특한 콘텐츠를 생성합니다.
                    </FormHelperText>
                  </FormControl>

                  <FormControl>
                    <FormLabel>기본 톤앤매너</FormLabel>
                    <Select
                      value={aiSettings.tone}
                      onChange={(e) =>
                        setAiSettings((prev) => ({
                          ...prev,
                          tone: e.target.value,
                        }))
                      }
                    >
                      <option value="friendly">친근한</option>
                      <option value="professional">전문적인</option>
                      <option value="casual">캐주얼한</option>
                      <option value="formal">격식 있는</option>
                    </Select>
                  </FormControl>

                  <FormControl>
                    <FormLabel>언어 설정</FormLabel>
                    <Select
                      value={aiSettings.language}
                      onChange={(e) =>
                        setAiSettings((prev) => ({
                          ...prev,
                          language: e.target.value,
                        }))
                      }
                    >
                      <option value="ko">한국어</option>
                      <option value="en">English</option>
                      <option value="ja">日本語</option>
                    </Select>
                  </FormControl>

                  <FormControl
                    display="flex"
                    alignItems="center"
                    justifyContent="space-between"
                  >
                    <Box>
                      <FormLabel mb="0">자동 콘텐츠 생성</FormLabel>
                      <FormHelperText>
                        설정된 스케줄에 따라 자동으로 콘텐츠를 생성합니다.
                      </FormHelperText>
                    </Box>
                    <Switch
                      isChecked={aiSettings.autoGenerate}
                      onChange={(e) =>
                        setAiSettings((prev) => ({
                          ...prev,
                          autoGenerate: e.target.checked,
                        }))
                      }
                    />
                  </FormControl>

                  <Button colorScheme="blue">AI 설정 저장</Button>
                </VStack>
              </CardBody>
            </Card>
          </TabPanel>

          {/* 계정 연동 */}
          <TabPanel p={0} pt={6}>
            <Card bg={cardBg} borderColor={borderColor}>
              <CardHeader>
                <Text fontSize="lg" fontWeight="bold">
                  소셜 미디어 계정 연동
                </Text>
              </CardHeader>
              <CardBody>
                <VStack spacing={4} align="stretch">
                  {connectedAccounts.map((account) => (
                    <Box
                      key={account.platform}
                      p={4}
                      border="1px solid"
                      borderColor={borderColor}
                      borderRadius="md"
                    >
                      <HStack justify="space-between">
                        <HStack>
                          <Box
                            as={getPlatformIcon(account.platform)}
                            size="20px"
                            color={`${getPlatformColor(account.platform)}.500`}
                          />
                          <VStack align="start" spacing={0}>
                            <Text fontWeight="medium">{account.name}</Text>
                            <Text fontSize="sm" color="gray.600">
                              {account.connected
                                ? account.email || account.id || "연결됨"
                                : "연결되지 않음"}
                            </Text>
                          </VStack>
                        </HStack>

                        <HStack>
                          <Badge
                            colorScheme={account.connected ? "green" : "gray"}
                          >
                            {account.connected ? "연결됨" : "연결 안됨"}
                          </Badge>

                          {account.connected ? (
                            <Button
                              size="sm"
                              variant="outline"
                              colorScheme="red"
                              onClick={() =>
                                handleDisconnectAccount(account.platform)
                              }
                            >
                              연결 해제
                            </Button>
                          ) : (
                            <Button
                              size="sm"
                              colorScheme="blue"
                              onClick={() => handleConnectAccount(account.name)}
                            >
                              연결하기
                            </Button>
                          )}
                        </HStack>
                      </HStack>
                    </Box>
                  ))}

                  <Alert status="info">
                    <AlertIcon />
                    계정을 연동하면 생성된 콘텐츠를 해당 플랫폼에 자동으로
                    게시할 수 있습니다.
                  </Alert>
                </VStack>
              </CardBody>
            </Card>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default SettingsPage;

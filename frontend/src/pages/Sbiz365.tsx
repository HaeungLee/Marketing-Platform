import React from "react";
import { Box, Heading, VStack } from "@chakra-ui/react";

const Sbiz365: React.FC = () => {
  return (
    <Box p={6}>
      <Heading as="h1" size="lg" mb={6}>
        소상공인365 분석
      </Heading>

      <VStack spacing={6}>
        <Box w="100%" h="600px" border="1px solid #ccc" borderRadius="md">
          <iframe
            src="https://bigdata.sbiz.or.kr/#/openApi/hpReport?certKey=7794d741d33deb6e8f76ac8332aaa3728f4e5f7979622ca2440410786e939415"
            width="100%"
            height="100%"
            style={{ border: "none" }}
            title="핫플레이스 분석"
          ></iframe>
        </Box>

        <Box w="100%" h="600px" border="1px solid #ccc" borderRadius="md">
          <iframe
            src="https://bigdata.sbiz.or.kr/#/openApi/startupPublic?certKey=2d2f5787eefef5f04b9420f1de7065800c5e7e0f5c3bb8716dc15905d93dfe12"
            width="100%"
            height="100%"
            style={{ border: "none" }}
            title="상권지도 분석"
          ></iframe>
        </Box>

        <Box w="100%" h="600px" border="1px solid #ccc" borderRadius="md">
          <iframe
            src="https://bigdata.sbiz.or.kr/#/openApi/slsIdex?certKey=83c9619da7b8a762caee43281fc625ff9cb4da6f4902b00f2c46fbf8f51df606"
            width="100%"
            height="100%"
            style={{ border: "none" }}
            title="매출추이 분석"
          ></iframe>
        </Box>

        <Box w="100%" h="600px" border="1px solid #ccc" borderRadius="md">          <iframe
            src="https://bigdata.sbiz.or.kr/#/openApi/simple?certKey=2ef6b4121693d2cf8f157ea952b2d2451bc30d606988fb13ad82e53b892b36d8"
            width="100%"
            height="100%"
            style={{ border: "none" }}
            title="간단분석"
          ></iframe>
        </Box>
      </VStack>
    </Box>
  );
};

export default Sbiz365;

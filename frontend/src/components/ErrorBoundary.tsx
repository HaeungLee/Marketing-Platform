import React, { Component, ErrorInfo, ReactNode } from "react";
import { Box, Heading, Text, Button } from "@chakra-ui/react";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <Box p={8} textAlign="center">
          <Heading mb={4}>문제가 발생했습니다</Heading>
          <Text mb={4}>죄송합니다. 오류가 발생했습니다.</Text>
          <Button
            colorScheme="blue"
            onClick={() => {
              this.setState({ hasError: false });
              window.location.reload();
            }}
          >
            다시 시도
          </Button>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

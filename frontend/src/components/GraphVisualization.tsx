import React from "react";
import { Box, Heading } from "@chakra-ui/react";
import { Chart } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const GraphVisualization: React.FC = () => {
  const data = {
    labels: ["1월", "2월", "3월", "4월", "5월", "6월"],
    datasets: [
      {
        label: "매출액 (억원)",
        data: [18, 16.5, 19.5, 21, 22.5, 24],
        backgroundColor: "rgba(75, 192, 192, 0.5)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "월별 매출 추이",
      },
    },
  };

  return (
    <Box p={6}>
      <Heading as="h2" size="md" mb={4}>
        매출 데이터 시각화
      </Heading>
      <Chart type="bar" data={data} options={options} />
    </Box>
  );
};

export default GraphVisualization;

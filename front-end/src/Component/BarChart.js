import React from "react";

import { Bar } from "react-chartjs-2";
const BarChart = ({ datas }) => {
  console.log(datas);
  return (
    <Bar
      data={{
        labels: ["A", "B", "C"],
        datasets: [
          {
            label: "Customer Feedback",
            data: [200, 300, 400],
          },
        ],
      }}
    />
  );
};

export default BarChart;

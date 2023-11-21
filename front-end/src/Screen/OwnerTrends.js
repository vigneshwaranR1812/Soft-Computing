import React, { useEffect, useState } from "react";
import { Button, Col, Container, Row } from "react-bootstrap";
import axios from "axios";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);
const OwnerTrends = () => {
  const [chartData, setChartData] = useState({});
  const [isRemoving, setIsRemoving] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [allData, setAllData] = useState(null);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/api/analyze-result");
        const data = response.data;
        setAllData(data.result);
        // Process data as needed for the chart
        const chartData = {
          labels: data.result.map((item) => item._id),
          datasets: [
            {
              label: "Count",
              data: data.result.map((item) => item.count),
              backgroundColor: "rgba(75, 192, 192, 0.6)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        };
        console.log(chartData);
        setChartData(chartData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []); // Empty dependency array to run the effect only once on mount

  const handleRemoveData = async () => {
    try {
      setIsRemoving(true);

      // Replace 'YOUR_FLASK_API_ENDPOINT' with the actual endpoint
      const response = await axios.delete("/api/remove-data");

      console.log(response.data); // Optional: Log the response from the Flask API
      setAllData(null);
      window.location.reload();
      setIsRemoving(false);
    } catch (error) {
      console.error("Error removing data:", error);
      setIsRemoving(false);
    }
  };
  // const data = {
  //   labels: ["Mon", "Tue", "Wed"],
  //   datasets: [
  //     {
  //       label: "369",
  //       data: [3, 6, 9],
  //       backgroundColor: "aqua",
  //       borderColor: "black",
  //       borderWidth: 1,
  //     },
  //   ],
  // };
  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };
  const updateMode = {
    resize: {
      height: "80%",
      width: "80%",
    },
  };
  return (
    <Container>
      <Row className="mt-5 mb-4" style={{ textAlign: "center" }}>
        <Col md={6}>
          <h1>Hello</h1>
        </Col>
        <Col md={6}>
          <Button
            onClick={handleRemoveData}
            disabled={isRemoving}
            variant="danger"
            type="button"
          >
            {isRemoving ? "Removing Data..." : "Remove All Data"}
          </Button>
        </Col>
      </Row>
      <Row>
        <Col md={2}></Col>
        <Col md={8} style={{ width: "90%", margin: " auto" }}>
          {isLoading && !allData ? (
            <></>
          ) : (
            <Bar data={chartData} options={options} updateMode={updateMode} />
          )}
        </Col>
        <Col md={2}></Col>
      </Row>
    </Container>
  );
};

export default OwnerTrends;

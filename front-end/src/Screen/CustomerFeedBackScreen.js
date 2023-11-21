import axios from "axios";
import React, { useState } from "react";
import { Button, Card, Col, Container, Form, Row } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const CustomerFeedBackScreen = () => {
  const history = useNavigate();
  const [textareaValue, setTextareaValue] = useState("");

  // Function to handle text area changes
  const handleTextareaChange = (event) => {
    setTextareaValue(event.target.value);
  };

  // Function to handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      // Use Axios to make a POST request (you can modify the method and URL as needed)
      const response = await axios.post("/api/analyze-feedback", {
        feedback: textareaValue,
      });
      window.alert("Feedback is Added successfully");

      window.location.reload();
      console.log("Response:", response.data);

      // Additional logic after a successful request
    } catch (error) {
      console.error("Error:", error);
      // Handle errors
    }
  };

  return (
    <Container>
      <Row>
        <Col md={3}></Col>
        <Col md={6}>
          <Card style={{ width: "100%", height: "50%", margin: "25% auto" }}>
            <Card.Body>
              <Card.Title>Give Your Feedback</Card.Title>
              <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formTextarea">
                  <Form.Label>Feedback</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={5}
                    value={textareaValue}
                    onChange={handleTextareaChange}
                  />
                  <Form.Text className="text-muted">
                    Maximum of 100 Words
                  </Form.Text>
                </Form.Group>
                <br />
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}></Col>
      </Row>
    </Container>
  );
};

export default CustomerFeedBackScreen;

import React, { useState } from "react";
import { Form, Button, Container, Row, Col } from "react-bootstrap";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import Card from "react-bootstrap/Card";

const SignUpScreen = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [userType, setUserType] = useState("customer");
  const history = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Make a login request using Axios
      const response = await axios.post(
        "/api/signup",
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
        {
          username,
          password,
          type: userType,
        }
      );
      console.log(response);
      // Check if login was successful (you might need to adjust based on your server response)
      if (
        response.data.user_detail.name &&
        response.data.user_detail.type === "customer"
      ) {
        // Navigate to the other page (replace '/otherpage' with your actual route)
        history("/feedback");
      } else if (
        response.data.user_detail.name &&
        response.data.user_detail.type === "owner"
      ) {
        // Navigate to the other page (replace '/otherpage' with your actual route)
        history("/trends");
      } else {
        // Handle login failure (show an error message, etc.)
        console.error("Login failed:", response.data.message);
      }
    } catch (error) {
      // Handle Axios request error
      console.error("Axios error:", error);
    }
  };

  return (
    <Container style={{ Height: "92vh" }}>
      <Row
        style={{ Height: "92vh" }}
        className="justify-content-md-center mt-5"
      >
        <Col md={6} style={{ marginTop: "20%" }}>
          <Card style={{ width: "90%", margin: "auto" }}>
            <Card.Body>
              <Card.Title>
                <h1>SignUp</h1>
              </Card.Title>
              <Form onSubmit={handleLogin}>
                <Form.Group controlId="formUsername">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter your username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </Form.Group>

                <Form.Group controlId="formPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </Form.Group>

                <Form.Group controlId="formUserType">
                  <Form.Label>User Type</Form.Label>
                  <Form.Control
                    as="select"
                    value={userType}
                    onChange={(e) => setUserType(e.target.value)}
                  >
                    <option value="customer">Customer</option>
                    <option value="owner">Owner</option>
                  </Form.Control>
                </Form.Group>
                <br />
                <Button variant="primary" type="submit">
                  Login
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col md={6}>
          <img src="./log.jpg" width="100%" height="100%" />
        </Col>
      </Row>
    </Container>
  );
};

export default SignUpScreen;

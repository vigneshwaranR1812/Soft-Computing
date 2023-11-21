import "./App.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LoginScreen from "./Screen/LoginScreen";
import SignUpScreen from "./Screen/SignUpScreen";
import NavBar from "./Component/Navbar";
import CustomerFeedBackScreen from "./Screen/CustomerFeedBackScreen";
import OwnerTrends from "./Screen/OwnerTrends";

const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginScreen />,
  },
  {
    path: "/",
    element: <LoginScreen />,
  },
  {
    path: "/signUp",
    element: <SignUpScreen />,
  },
  {
    path: "/feedback",
    element: <CustomerFeedBackScreen />,
  },
  {
    path: "/trends",
    element: <OwnerTrends />,
  },
  // {
  //   path: "/dashboard",
  //   element: <DashBoardScreen />,
  // },
]);
function App() {
  return (
    <>
      <>
        <NavBar />
        <RouterProvider router={router} />
      </>
    </>
  );
}

export default App;

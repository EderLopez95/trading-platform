import { createBrowserRouter } from "react-router-dom";
import LoginPage from "../../modules/auth/pages/loginPage";
import RegisterPage from "../../modules/auth/pages/registerPage";
import DashboardPage from "../../shared/components/dashboardPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <DashboardPage />,
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
]);

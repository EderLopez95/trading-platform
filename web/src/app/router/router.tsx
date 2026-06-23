import { createBrowserRouter } from "react-router-dom";
import LoginPage from "@/modules/auth/pages/LoginPage";
import RegisterPage from "@/modules/auth/pages/RegisterPage";
import DashboardPage from "@/modules/dashboard/pages/DashboardPage";
import ProtectedRoute from "@/shared/components/ProtectedRoute";
import ProfilePage from "@/modules/profile/pages/ProfilePage";
import ConfigurationsPage from "@/modules/configurations/pages/ConfigurationsPage";
import SignalsPage from "@/modules/signals/pages/SignalsPage";
import NewConfigurationPage from "@/modules/configurations/pages/NewConfigurationPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <DashboardPage />
      </ProtectedRoute>
    ),
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
  {
    path: "/signals",
    element: (
      <ProtectedRoute>
        <SignalsPage />
      </ProtectedRoute>
    ),
  },
  {
    path: "/configurations",
    element: (
      <ProtectedRoute>
        <ConfigurationsPage />
      </ProtectedRoute>
    ),
  },
  {
    path: "/profile",
    element: (
      <ProtectedRoute>
        <ProfilePage />
      </ProtectedRoute>
    ),
  },
  {
    path: "/configurations/new",
    element: (
      <ProtectedRoute>
        <NewConfigurationPage />
      </ProtectedRoute>
    ),
  },
]);

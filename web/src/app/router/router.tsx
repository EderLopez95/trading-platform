import { createBrowserRouter, Navigate } from "react-router-dom";
import LoginPage from "@/modules/auth/pages/LoginPage";
import RegisterPage from "@/modules/auth/pages/RegisterPage";
import ProtectedRoute from "@/shared/components/ProtectedRoute";
import MainLayout from "@/shared/layouts/MainLayout";
import SettingsPage from "@/modules/settings/pages/SettingsPage";
import SignalsPage from "@/modules/signals/pages/SignalsPage";

export const router = createBrowserRouter([
  {
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Navigate to="/signals" replace />,
      },
      {
        path: "/signals",
        element: <SignalsPage />,
      },
      {
        path: "/bot",
        element: <div>Bot</div>,
      },
      {
        path: "/settings",
        element: <SettingsPage />,
      },
    ],
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

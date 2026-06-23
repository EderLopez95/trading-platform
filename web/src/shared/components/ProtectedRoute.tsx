import { Navigate } from "react-router-dom";
import { type ReactNode } from "react";
import { useAuth } from "@/app/providers/AuthProvider";
import AppLoader from "./AppLoader";

type Props = {
  children: ReactNode;
};

export default function ProtectedRoute({
  children,
}: Props) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <AppLoader />;
  }

  if (!isAuthenticated) {
    return (
      <Navigate to="/login" replace/>
    );
  }

  return <>{children}</>;
}

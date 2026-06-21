import { Navigate } from "react-router-dom";
import { type ReactNode } from "react";
import { useAuth } from "@/app/providers/AuthProvider";

type Props = {
  children: ReactNode;
};

export default function ProtectedRoute({
  children,
}: Props) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

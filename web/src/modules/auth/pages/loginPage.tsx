import { useNavigate } from "react-router-dom";
import LoginForm from "../components/LoginForm";
import { authApi } from "../api/authApi";
import { useAuth } from "@/app/providers/AuthProvider";
import { type LoginFormData } from "../services/loginSchema";
import { Navigate } from "react-router-dom";
import AuthLayout from "@/shared/layouts/AuthLayout";
import toast from "react-hot-toast";

export default function LoginPage() {
  const navigate = useNavigate();  
  const { login, isAuthenticated } = useAuth();
  
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const handleLogin = async (
    data: LoginFormData
  ) => {
    try {
      const response = await authApi.login(data);
      login(response.token);
      navigate("/");
    } catch (error) {
      console.error(error);
      toast.error("Invalid credentials");
    }
  };
  return (
    <AuthLayout title="Sign In">
      <LoginForm onSubmit={handleLogin} />
    </AuthLayout>
  );
}

import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import AuthLayout from "@/shared/layouts/AuthLayout";
import RegisterForm from "../components/RegisterForm";
import { authApi } from "../api/authApi";
import { type RegisterFormData } from "../services/registerSchema";
import { isAxiosError } from "axios";

export default function RegisterPage() {
  const navigate = useNavigate();

  const handleRegister = async (
    data: RegisterFormData
  ) => {
    try {
      await authApi.register({
        email: data.email,
        password: data.password,
      });
      toast.success(
        "User created successfully"
      );
      navigate("/login");
    } catch (error) {
      console.error(error);
      if (isAxiosError(error) && error.response?.status === 409) {
        toast.error("User already exists");
      } else {
        toast.error(
          "Failed to create user"
        );
      }
    }
  };

  return (
    <AuthLayout title="Register">
      <RegisterForm
        onSubmit={handleRegister}
      />
    </AuthLayout>
  );
}

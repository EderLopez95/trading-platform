import { apiClient } from "@/shared/services/apiClient";
import {
  type LoginRequest,
  type LoginResponse,
  type RegisterRequest
} from "../types/auth.types";

export const authApi = {
  login: async (data: LoginRequest) => {
    const response = await apiClient.post<LoginResponse>(
      "/auth/login",
      data
    );
    return response.data;
  },

  register: async (data: RegisterRequest) => {
    const response = await apiClient.post(
      "/auth/register",
      data
    );
    return response.data;
  },
};

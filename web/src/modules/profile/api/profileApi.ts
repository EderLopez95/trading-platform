import { apiClient } from "@/shared/services/apiClient";
import {
  type UpdateProfileRequest,
} from "../types/profile.types";

export const profileApi = {
  getProfile: async () => {
    const response = await apiClient.get("/auth/me");

    return response.data;
  },

  updateProfile: async (
    data: UpdateProfileRequest
  ) => {
    const response = await apiClient.put(
      "/auth/telegram",
      data
    );

    return response.data;
  },
};

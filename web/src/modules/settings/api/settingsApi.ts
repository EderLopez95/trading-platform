import { apiClient } from "@/shared/services/apiClient";
import {
  type TelegramSettings,
  type UpdateTelegramRequest,
  type UpdateTelegramResponse,
} from "../types/settings.types";

export const settingsApi = {
  getTelegram: async () => {
    const response = await apiClient.get<TelegramSettings>("/auth/telegram");

    return response.data;
  },

  updateTelegram: async (data: UpdateTelegramRequest) => {
    const response = await apiClient.put<UpdateTelegramResponse>(
      "/auth/telegram",
      data
    );

    return response.data;
  },
};

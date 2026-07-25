import { apiClient } from "@/shared/services/apiClient";

export interface UpdateTelegramRequest {
  telegram_token: string;
  telegram_chat_id: string;
}

export interface UpdateTelegramResponse {
  user_id: string;
}

export const settingsApi = {
  updateTelegram: async (data: UpdateTelegramRequest) => {
    const response = await apiClient.put<UpdateTelegramResponse>(
      "/auth/telegram",
      data
    );

    return response.data;
  },
};

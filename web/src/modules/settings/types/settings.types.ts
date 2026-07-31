export interface TelegramSettings {
  telegram_token: string;
  telegram_chat_id: string;
}

export interface UpdateTelegramResponse {
  user_id: string;
}

export interface UpdateTelegramRequest {
  telegram_token: string;
  telegram_chat_id: string;
}

import { z } from "zod";

export const telegramSchema = z.object({
  telegram_token: z
    .string()
    .trim()
    .min(1, "Token is required")
    .regex(
      /^\d+:[A-Za-z0-9_-]+$/,
      "Invalid token format (e.g. 123456789:ABC-DEF...)"
    ),
  telegram_chat_id: z
    .string()
    .trim()
    .min(1, "Chat ID is required")
    .regex(/^-?\d+$/, "Chat ID must be a number"),
});

export type TelegramFormData = z.infer<typeof telegramSchema>;

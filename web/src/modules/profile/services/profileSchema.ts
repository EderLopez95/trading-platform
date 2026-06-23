import { z } from "zod";

export const profileSchema = z.object({
  telegram_token: z.string(),
  telegram_chat_id: z.string(),
});

export type ProfileFormData = z.infer<typeof profileSchema>;

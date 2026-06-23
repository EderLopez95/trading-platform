import { z } from "zod";

export const configurationSchema = z.object({
  symbols: z.array(z.string()).min(1),
  strategies: z.array(z.string()).min(1),
  trend_timeframe: z.string(),
  context_timeframe: z.string().nullable(),
  entry_timeframe: z.string(),
});

export type ConfigurationFormData = z.infer<typeof configurationSchema>;

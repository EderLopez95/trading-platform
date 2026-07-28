import { z } from "zod";

export const configurationSchema = z.object({
  symbols: z
    .array(z.string())
    .min(1, "Select at least one symbol"),
  strategies: z
    .array(z.string())
    .min(1, "Select at least one strategy"),
  trend_timeframe: z
    .string()
    .min(1, "Trend timeframe is required"),
  context_timeframe: z.string().optional(),
  entry_timeframe: z
    .string()
    .min(1, "Entry timeframe is required"),
});

export type ConfigurationFormData = z.infer<typeof configurationSchema>;

export interface Configuration {
  id: string;
  symbols: string[];
  strategies: string[];
  params?: Record<string, unknown>;
  trend_timeframe: string;
  context_timeframe?: string | null;
  entry_timeframe: string;
  enabled: boolean;
  created_at: string;
}

export interface CreateConfigurationRequest {
  symbols: string[];
  strategies: string[];
  params?: Record<string, unknown>;
  trend_timeframe: string;
  context_timeframe?: string | null;
  entry_timeframe: string;
}

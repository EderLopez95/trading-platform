export interface Configuration {
  id: string;
  user_id: string;
  symbols: string[];
  strategies: string[];
  trend_timeframe: string;
  context_timeframe: string | null;
  entry_timeframe: string;
  enabled: boolean;
}

export interface ConfigurationPayload {
  symbols: string[];
  strategies: string[];
  trend_timeframe: string;
  context_timeframe?: string | null;
  entry_timeframe: string;
}

export interface GetConfigurationsResponse {
  configurations: Configuration[];
}

export interface AnalysisStatus {
  enabled: boolean;
}

export interface Strategy {
  id: string;
  name: string;
}

export interface StrategiesResponse {
  strategies: Strategy[];
}

export interface SymbolsResponse {
  symbols: { symbol: string }[];
}

export interface TimeframesResponse {
  timeframes: { timeframe: string }[];
}

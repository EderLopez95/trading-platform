export interface Signal {
  id: string;
  symbol: string;
  strategy: string;
  signal: string;
  trend_timeframe: string;
  context_timeframe: string;
  entry_timeframe: string;
  price: number;
  signal_time: string;
}

export interface GetSignalsParams {
  symbol?: string;
  strategy?: string;
  page?: number;
  page_size?: number;
}

export interface GetSignalsResponse {
  signals: Signal[];
  page: number;
  page_size: number;
  total: number;
}

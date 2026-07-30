import { apiClient } from "@/shared/services/apiClient";
import {
  type StrategiesResponse,
  type SymbolsResponse,
  type TimeframesResponse,
} from "../types/configuration.types";

export const optionsApi = {
  getStrategies: async () => {
    const response = await apiClient.get<StrategiesResponse>(
      "/signals/strategies"
    );

    return response.data.strategies;
  },

  getSymbols: async (search?: string) => {
    const response = await apiClient.get<SymbolsResponse>(
      "/signals/symbols",
      { params: search ? { search } : undefined }
    );

    return response.data.symbols.map((item) => item.symbol);
  },

  getTimeframes: async () => {
    const response = await apiClient.get<TimeframesResponse>(
      "/signals/timeframes"
    );

    return response.data.timeframes.map((item) => item.timeframe);
  },
};

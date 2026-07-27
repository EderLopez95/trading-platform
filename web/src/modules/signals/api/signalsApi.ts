import { apiClient } from "@/shared/services/apiClient";
import {
  type GetSignalsParams,
  type GetSignalsResponse,
} from "../types/signal.types";

export const signalsApi = {
  getSignals: async (params: GetSignalsParams) => {
    const response = await apiClient.get<GetSignalsResponse>(
      "/signals/signals",
      { params }
    );

    return response.data;
  },
};

import { apiClient } from "@/shared/services/apiClient";
import { type AnalysisStatus } from "../types/configuration.types";

export const analysisApi = {
  getStatus: async () => {
    const response = await apiClient.get<AnalysisStatus>(
      "/analysis/status"
    );

    return response.data;
  },

  toggleStatus: async (enabled: boolean) => {
    const response = await apiClient.patch<AnalysisStatus>(
      "/analysis/status",
      { enabled }
    );

    return response.data;
  },
};

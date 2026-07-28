import { apiClient } from "@/shared/services/apiClient";
import {
  type Configuration,
  type ConfigurationPayload,
  type GetConfigurationsResponse,
} from "../types/configuration.types";

export const configurationsApi = {
  getConfigurations: async () => {
    const response = await apiClient.get<GetConfigurationsResponse>(
      "/configurations"
    );

    return response.data.configurations;
  },

  createConfiguration: async (data: ConfigurationPayload) => {
    const response = await apiClient.post<Configuration>(
      "/configurations",
      data
    );

    return response.data;
  },

  deleteConfiguration: async (id: string) => {
    await apiClient.delete(`/configurations/${id}`);
  },

  toggleConfiguration: async (id: string, enabled: boolean) => {
    const response = await apiClient.patch<Configuration>(
      `/configurations/${id}/status`,
      { enabled }
    );

    return response.data;
  },
};

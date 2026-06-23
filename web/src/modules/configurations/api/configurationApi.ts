import { apiClient } from "@/shared/services/apiClient";

export const configurationApi = {
  getAll: async () => {
    const response = await apiClient.get("/configurations");

    return response.data;
  },

  create: async (data: any) => {
    const response = await apiClient.post(
      "/configurations",
      data
    );

    return response.data;
  },

  updateStatus: async (
    id: string,
    enabled: boolean
  ) => {
    const response = await apiClient.patch(
      `/configurations/${id}/status`,
      {
        enabled,
      }
    );

    return response.data;
  },

  delete: async (id: string) => {
    const response = await apiClient.delete(
      `/configurations/${id}`
    );

    return response.data;
  },
};

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { configurationsApi } from "../api/configurationsApi";
import { type ConfigurationPayload } from "../types/configuration.types";

const CONFIGURATIONS_KEY = ["configurations"];

export function useConfigurations() {

  return useQuery({
    queryKey: CONFIGURATIONS_KEY,
    queryFn: configurationsApi.getConfigurations,
  });
}

export function useCreateConfiguration() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ConfigurationPayload) =>
      configurationsApi.createConfiguration(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CONFIGURATIONS_KEY });
    },
  });
}

export function useUpdateConfiguration() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: ConfigurationPayload;
    }) => configurationsApi.updateConfiguration(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CONFIGURATIONS_KEY });
    },
  });
}

export function useDeleteConfiguration() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) =>
      configurationsApi.deleteConfiguration(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CONFIGURATIONS_KEY });
    },
  });
}

export function useToggleConfiguration() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, enabled }: { id: string; enabled: boolean }) =>
      configurationsApi.toggleConfiguration(id, enabled),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: CONFIGURATIONS_KEY });
    },
  });
}

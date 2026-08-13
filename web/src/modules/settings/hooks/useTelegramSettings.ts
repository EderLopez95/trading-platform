import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { settingsApi } from "../api/settingsApi";
import { type TelegramSettings } from "../types/settings.types";

const TELEGRAM_SETTINGS_KEY = ["telegram-settings"];

export function useTelegramSettings() {

  return useQuery({
    queryKey: TELEGRAM_SETTINGS_KEY,
    queryFn: settingsApi.getTelegram,
    staleTime: 5 * 60_000,
  });
}

export function useUpdateTelegramSettings() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: settingsApi.updateTelegram,
    onSuccess: (_response, variables) => {
      queryClient.setQueryData<TelegramSettings>(
        TELEGRAM_SETTINGS_KEY,
        variables
      );
    },
  });
}

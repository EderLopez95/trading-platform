import { useQuery } from "@tanstack/react-query";
import { settingsApi } from "../api/settingsApi";

export function useTelegramSettings() {

  return useQuery({
    queryKey: ["telegram-settings"],
    queryFn: settingsApi.getTelegram,
    staleTime: 5 * 60_000,
  });
}

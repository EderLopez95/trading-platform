import { useQuery } from "@tanstack/react-query";
import { optionsApi } from "../api/optionsApi";

export function useFormOptions(enabled: boolean) {
  const strategies = useQuery({
    queryKey: ["strategies"],
    queryFn: optionsApi.getStrategies,
    enabled,
    staleTime: 5 * 60_000,
  });

  const symbols = useQuery({
    queryKey: ["symbols"],
    queryFn: optionsApi.getSymbols,
    enabled,
    staleTime: 5 * 60_000,
  });

  const timeframes = useQuery({
    queryKey: ["timeframes"],
    queryFn: optionsApi.getTimeframes,
    enabled,
    staleTime: 5 * 60_000,
  });

  return {
    strategies: strategies.data ?? [],
    symbols: symbols.data ?? [],
    timeframes: timeframes.data ?? [],
    isLoading:
      strategies.isLoading || symbols.isLoading || timeframes.isLoading,
  };
}

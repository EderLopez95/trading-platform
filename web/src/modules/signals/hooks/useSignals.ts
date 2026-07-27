import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";
import { signalsApi } from "../api/signalsApi";
import { type GetSignalsParams } from "../types/signal.types";

export function useSignals(params: GetSignalsParams) {

  return useQuery({
    queryKey: ["signals", params],
    queryFn: () => signalsApi.getSignals(params),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { analysisApi } from "../api/analysisApi";

const ANALYSIS_KEY = ["analysis-status"];

export function useAnalysisStatus() {

  return useQuery({
    queryKey: ANALYSIS_KEY,
    queryFn: analysisApi.getStatus,
  });
}

export function useToggleAnalysis() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (enabled: boolean) => analysisApi.toggleStatus(enabled),
    onSuccess: (data) => {
      queryClient.setQueryData(ANALYSIS_KEY, data);
    },
  });
}

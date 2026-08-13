import { QueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";

function isClientError(error: unknown): boolean {
  const status = (error as AxiosError)?.response?.status;

  return typeof status === "number" && status >= 400 && status < 500;
}

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      gcTime: 5 * 60_000,
      refetchOnWindowFocus: false,
      retry: (failureCount, error) => {
        if (isClientError(error)) {
          return false;
        }

        return failureCount < 2;
      },
    },
    mutations: {
      retry: false,
    },
  },
});

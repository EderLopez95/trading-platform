import axios from "axios";
import { v4 as uuid } from "uuid";
import { queryClient } from "@/app/providers/queryClient";
import { router } from "@/app/router/router";

export const apiClient = axios.create({
  baseURL: window.__APP_CONFIG__?.API_URL ?? import.meta.env.VITE_API_URL,
  timeout: 10000,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  config.headers["X-Request-Id"] =
    uuid();

  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url ?? "";
    const authEndpoints = [
      "/auth/login",
      "/auth/register",
    ];

    const shouldIgnore =
      authEndpoints.some(endpoint =>
        url.includes(endpoint)
      );

    if (
      error.response?.status === 401 &&
      !shouldIgnore
    ) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

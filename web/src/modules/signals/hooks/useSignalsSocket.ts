import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";

function resolveWsUrl(): string | null {
  const apiUrl = window.__APP_CONFIG__?.API_URL ?? import.meta.env.VITE_API_URL;

  if (!apiUrl) {
    return null;
  }

  const token = localStorage.getItem("token");

  if (!token) {
    return null;
  }

  const wsBase = apiUrl.replace(/^http/, "ws");

  return `${wsBase}/ws/signals?token=${encodeURIComponent(token)}`;
}

export function useSignalsSocket() {
  const queryClient = useQueryClient();

  useEffect(() => {
    let socket: WebSocket | null = null;
    let reconnectTimer: number | undefined;
    let closedByUs = false;

    const connect = () => {
      const url = resolveWsUrl();

      if (!url) {
        return;
      }

      socket = new WebSocket(url);

      socket.onmessage = () => {
        queryClient.invalidateQueries({ queryKey: ["signals"] });
      };

      socket.onclose = (event) => {
        if (closedByUs || event.code === 1008) {
          return;
        }

        reconnectTimer = window.setTimeout(connect, 3000);
      };
    };

    connect();

    return () => {
      closedByUs = true;

      if (reconnectTimer) {
        window.clearTimeout(reconnectTimer);
      }

      socket?.close();
    };
  }, [queryClient]);
}

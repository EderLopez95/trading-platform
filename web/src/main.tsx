import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import QueryProvider from "@/app/providers/QueryProvider";
import { AuthProvider } from "@/app/providers/AuthProvider";
import { Toaster } from "react-hot-toast";
import "@/styles/global.scss";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryProvider>
      <AuthProvider>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              fontSize: "13px",
              borderRadius: "8px",
              padding: "12px 24px"
            },
            success: {
              style: {
                backgroundColor: 'var(--toast-background-color)',
                color: 'var(--toast-text-color)',
              }
            },
            error: {
              style: {
                backgroundColor: 'var(--toast-background-color)',
                color: 'var(--toast-text-color)',
              }
            },
            loading: {
              style: {
                backgroundColor: 'var(--toast-background-color)',
                color: 'var(--toast-text-color)',
              }
            },
          }}
        />
        <App />
      </AuthProvider>
    </QueryProvider>
  </React.StrictMode>
);

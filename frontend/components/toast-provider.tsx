"use client";

import { Toaster } from "sonner";

export function ToastProvider() {
  return (
    <Toaster
      richColors
      theme="dark"
      position="top-right"
      toastOptions={{
        classNames: {
          toast: "glass-panel text-slate-100 border border-white/10",
          title: "text-white",
          description: "text-slate-300",
        },
      }}
    />
  );
}

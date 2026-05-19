"use client";

import { useCallback, useEffect, useState } from "react";
import { getUserThreads } from "@/lib/api";
import { ApiError } from "@/lib/api";
import { ThreadRecord } from "@/lib/types";

export function useThreads(email?: string | null) {
  const [threads, setThreads] = useState<ThreadRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!email) {
      setThreads([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await getUserThreads(email);

      if (Array.isArray(result)) {
        setThreads(result);
        return;
      }

      setThreads([]);
      setError(typeof result === "string" ? result : "No threads found");
    } catch (caughtError) {
      const message = caughtError instanceof ApiError ? caughtError.message : "Failed to load threads";
      setThreads([]);
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [email]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void refresh();
    }, 0);

    return () => window.clearTimeout(timer);
  }, [refresh]);

  return {
    threads,
    loading,
    error,
    refresh,
  };
}

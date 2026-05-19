"use client";

import { useEffect, useState } from "react";
import { clearAuthState, loadAuthState, saveAuthState } from "@/lib/storage";
import { UserAuthState } from "@/lib/types";
import { isSessionExpired } from "@/lib/session";

export function useAuth() {
  const [auth, setAuth] = useState<UserAuthState | null>(loadAuthState);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const current = loadAuthState();
      setAuth(current);
      setHydrated(true);
    }, 0);

    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (!auth?.expires_at) {
      return;
    }

    if (isSessionExpired(auth.expires_at)) {
      const timer = window.setTimeout(() => {
        setAuth(null);
        clearAuthState();
      }, 0);

      return () => window.clearTimeout(timer);
    }

    const msUntilExpiry = Math.max(auth.expires_at - Date.now(), 0);
    const timer = window.setTimeout(() => {
      setAuth(null);
      clearAuthState();
    }, msUntilExpiry);

    return () => window.clearTimeout(timer);
  }, [auth]);

  const persistAuth = (value: UserAuthState) => {
    setAuth(value);
    saveAuthState(value);
  };

  const clearAuth = () => {
    setAuth(null);
    clearAuthState();
  };

  return {
    auth,
    hydrated,
    persistAuth,
    clearAuth,
    isAuthenticated: Boolean(auth?.access_token),
    isSessionExpired: isSessionExpired(auth?.expires_at),
  };
}

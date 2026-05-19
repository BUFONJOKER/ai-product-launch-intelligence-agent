import { LoginResponse, UserAuthState } from "@/lib/types";

export function decodeJwtExpiry(token: string): number {
  const payload = token.split(".")[1];

  if (!payload) {
    return Date.now() + 10 * 60 * 1000;
  }

  try {
    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
    const decoded = typeof atob === "function" ? atob(normalized.padEnd(Math.ceil(normalized.length / 4) * 4, "=")) : Buffer.from(normalized, "base64").toString("utf8");
    const body = JSON.parse(decoded) as { exp?: number };

    return typeof body.exp === "number" ? body.exp * 1000 : Date.now() + 10 * 60 * 1000;
  } catch {
    return Date.now() + 10 * 60 * 1000;
  }
}

export function createAuthStateFromLogin(response: LoginResponse): UserAuthState {
  return {
    access_token: response.access_token,
    name: response.name,
    email: response.email,
    api_key_openai: response.api_key_openai,
    expires_at: decodeJwtExpiry(response.access_token),
  };
}

export function isSessionExpired(expiresAt?: number | null) {
  return typeof expiresAt === "number" && expiresAt <= Date.now();
}

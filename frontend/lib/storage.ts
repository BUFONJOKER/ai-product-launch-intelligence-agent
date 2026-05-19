import { UserAuthState, WorkspaceHistoryEntry, WorkspaceSnapshot } from "@/lib/types";

const AUTH_KEY = "pla-auth";
const WORKSPACE_HISTORY_KEY = "pla-workspace-history";
const WORKSPACE_SNAPSHOT_KEY = "pla-workspace-snapshot";

export function loadAuthState(): UserAuthState | null {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = window.localStorage.getItem(AUTH_KEY);

  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as UserAuthState;
  } catch {
    return null;
  }
}

export function saveAuthState(value: UserAuthState) {
  window.localStorage.setItem(AUTH_KEY, JSON.stringify(value));
}

export function clearAuthState() {
  window.localStorage.removeItem(AUTH_KEY);
}

export function loadWorkspaceHistory(): WorkspaceHistoryEntry[] {
  if (typeof window === "undefined") {
    return [];
  }

  const raw = window.localStorage.getItem(WORKSPACE_HISTORY_KEY);

  if (!raw) {
    return [];
  }

  try {
    const parsed = JSON.parse(raw) as WorkspaceHistoryEntry[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function saveWorkspaceHistory(entries: WorkspaceHistoryEntry[]) {
  window.localStorage.setItem(WORKSPACE_HISTORY_KEY, JSON.stringify(entries.slice(0, 12)));
}

export function upsertWorkspaceHistory(entry: WorkspaceHistoryEntry) {
  const current = loadWorkspaceHistory();
  const next = [entry, ...current.filter((item) => item.thread_id !== entry.thread_id)].slice(0, 12);
  saveWorkspaceHistory(next);
  return next;
}

export function loadWorkspaceSnapshot(): WorkspaceSnapshot | null {
  if (typeof window === "undefined") {
    return null;
  }

  const raw = window.localStorage.getItem(WORKSPACE_SNAPSHOT_KEY);

  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as WorkspaceSnapshot;
  } catch {
    return null;
  }
}

export function saveWorkspaceSnapshot(snapshot: WorkspaceSnapshot) {
  window.localStorage.setItem(WORKSPACE_SNAPSHOT_KEY, JSON.stringify(snapshot));
}

export function clearWorkspaceSnapshot() {
  window.localStorage.removeItem(WORKSPACE_SNAPSHOT_KEY);
}

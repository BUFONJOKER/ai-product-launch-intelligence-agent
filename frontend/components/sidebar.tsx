"use client";

import { Search, Plus, LogOut, Settings } from "lucide-react";
import Link from "next/link";
import { ThreadRecord, WorkspaceHistoryEntry } from "@/lib/types";
import { ThreadList } from "@/components/thread-list";

interface SidebarProps {
  userName: string;
  userEmail: string;
  threads: ThreadRecord[];
  activeThreadId: string | null;
  searchQuery: string;
  onSearchChange: (value: string) => void;
  onCreateThread: () => void;
  onSelectThread: (threadId: string) => void;
  onLogout: () => void;
  loading?: boolean;
  historyEntries: WorkspaceHistoryEntry[];
  onSelectHistory: (threadId: string) => void;
}

export function Sidebar({
  userName,
  userEmail,
  threads,
  activeThreadId,
  searchQuery,
  onSearchChange,
  onCreateThread,
  onSelectThread,
  onLogout,
  loading,
  historyEntries,
  onSelectHistory,
}: SidebarProps) {
  const filteredThreads = threads.filter((thread) => thread.thread_id.includes(searchQuery) || thread.email.includes(searchQuery));

  return (
    <aside className="glass-panel flex h-full flex-col rounded-[2rem] p-4 lg:p-5">
      <div className="rounded-[1.5rem] border border-white/8 bg-white/5 p-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Workspace</p>
            <h2 className="mt-1 text-lg font-semibold text-white">{userName}</h2>
          </div>
          <div className="flex gap-2">
            <Link
              href="/settings"
              className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-white/5 text-slate-200 transition-colors hover:bg-white/10"
              aria-label="Settings"
            >
              <Settings className="h-4 w-4" />
            </Link>
            <button
              onClick={onLogout}
              className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-white/5 text-slate-200 transition-colors hover:bg-white/10"
              aria-label="Logout"
              type="button"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
        <p className="mt-2 text-sm text-slate-400">{userEmail}</p>

        <button
          type="button"
          onClick={onCreateThread}
          className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-full bg-white px-4 py-3 text-sm font-medium text-slate-950 transition-transform hover:scale-[1.01]"
          disabled={loading}
        >
          <Plus className="h-4 w-4" />
          New Thread
        </button>
      </div>

      <label className="mt-4 flex items-center gap-3 rounded-[1.4rem] border border-white/8 bg-white/5 px-4 py-3 text-sm text-slate-300">
        <Search className="h-4 w-4 text-slate-400" />
        <input
          value={searchQuery}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Search threads"
          className="w-full bg-transparent outline-none placeholder:text-slate-500"
        />
      </label>

      <div className="mt-4 flex-1 overflow-hidden rounded-[1.5rem] border border-white/8 bg-white/4 p-3">
        <div className="mb-3 flex items-center justify-between px-1">
          <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Thread history</p>
          <span className="text-xs text-slate-500">{filteredThreads.length}</span>
        </div>
        <div className="h-[calc(100%-2rem)] overflow-y-auto pr-1">
          <ThreadList threads={filteredThreads} activeThreadId={activeThreadId} onSelectThread={onSelectThread} />
        </div>
      </div>

      <div className="mt-4 rounded-[1.5rem] border border-white/8 bg-white/4 p-3">
        <div className="mb-3 flex items-center justify-between px-1">
          <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Workspace history</p>
          <span className="text-xs text-slate-500">{historyEntries.length}</span>
        </div>
        <div className="max-h-64 space-y-2 overflow-y-auto pr-1">
          {historyEntries.length === 0 ? (
            <p className="rounded-2xl border border-dashed border-white/10 px-4 py-6 text-sm text-slate-400">
              Completed workspaces will appear here and persist across refreshes.
            </p>
          ) : (
            historyEntries.map((entry) => (
              <button
                key={entry.id}
                type="button"
                onClick={() => onSelectHistory(entry.thread_id)}
                className="flex w-full items-start justify-between rounded-2xl border border-white/8 bg-[#081227] px-4 py-3 text-left transition hover:bg-white/8"
              >
                <div>
                  <p className="text-sm font-medium text-white">{entry.company_name}</p>
                  <p className="mt-1 text-xs text-slate-400">{entry.agent_invoke}</p>
                  <p className="mt-1 text-[11px] text-slate-500">{entry.thread_id.slice(0, 8)}…</p>
                </div>
                <span className="rounded-full bg-white/8 px-2 py-1 text-[10px] uppercase tracking-[0.2em] text-slate-300">
                  {entry.status}
                </span>
              </button>
            ))
          )}
        </div>
      </div>
    </aside>
  );
}

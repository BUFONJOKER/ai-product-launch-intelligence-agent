"use client";

import { motion } from "framer-motion";
import { ThreadRecord } from "@/lib/types";
import { Clock, Trash2 } from "lucide-react";
import { getThreadMetadata, loadWorkspaceHistory } from "@/lib/storage";

interface ThreadListProps {
  threads: ThreadRecord[];
  activeThreadId: string | null;
  onSelectThread: (threadId: string) => void;
  onDeleteThread?: (threadId: string) => void;
}

export function ThreadList({ threads, activeThreadId, onSelectThread, onDeleteThread }: ThreadListProps) {
  return (
    <div className="space-y-2">
      {threads.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-white/10 px-4 py-6 text-sm text-slate-400">
          No threads yet. Create a new workspace to begin.
        </div>
      ) : (
        threads.map((thread, index) => {
          const active = thread.thread_id === activeThreadId;
          const metadata = getThreadMetadata(thread.thread_id);
          const combined = metadata?.company_name || "Untitled Project";

          // split into company / product
          const split = (() => {
            if (!combined) return { company: "Untitled", product: "" };
            if (combined.includes("—")) {
              const [c, p] = combined.split("—");
              return { company: c.trim(), product: p.trim() };
            }
            if (combined.includes(" - ")) {
              const [c, p] = combined.split(" - ");
              return { company: c.trim(), product: p.trim() };
            }
            // fallback: first word = company, rest = product
            const parts = combined.trim().split(/\s+/);
            return { company: parts[0], product: parts.slice(1).join(" ") };
          })();

          const history = loadWorkspaceHistory();
          const last = history.find((h) => h.thread_id === thread.thread_id)?.updated_at ?? null;

          const initials = split.company
            .split(/\s+/)
            .map((s) => s[0] ?? "")
            .slice(0, 2)
            .join("")
            .toUpperCase();

          return (
            <motion.div
              key={thread.thread_id}
              whileHover={{ x: 4, scale: 1.01 }}
              whileTap={{ scale: 0.995 }}
              onClick={() => onSelectThread(thread.thread_id)}
              className={`group relative flex w-full cursor-pointer items-center justify-between gap-3 rounded-2xl border px-3 py-3 text-left transition-all ${active
                  ? "border-cyan-400/40 bg-gradient-to-r from-cyan-500/15 to-cyan-400/5 shadow-[inset_0_1px_2px_rgba(34,211,238,0.06)]"
                  : "border-white/8 bg-white/4 hover:border-white/15 hover:bg-white/8"
                }`}
            >
              <div className="flex items-start gap-3 min-w-0">
                <div className={`flex h-12 w-12 items-center justify-center rounded-xl border ${active ? "border-cyan-400/30 bg-cyan-500/10" : "border-white/6 bg-white/6"
                  }`}
                >
                  <span className="text-sm font-semibold text-white/90">{initials}</span>
                </div>
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-semibold text-white truncate">{split.company}</p>
                    <p className="text-sm text-slate-400 truncate">— {split.product || "Project"}</p>
                  </div>
                  <div className="mt-1 flex items-center gap-2 text-xs text-slate-400">
                    <span className="truncate">{metadata?.agent_invoke?.replace(/_/g, " ") ?? "ANALYST"}</span>
                    <span>•</span>
                    <time>{last ? formatDate(last) : "—"}</time>
                  </div>
                </div>
              </div>

              <div className="flex-shrink-0">
                <div className="flex items-center gap-2">
                  {active ? (
                    <motion.div
                      className="flex h-8 w-8 items-center justify-center rounded-full bg-cyan-400/20 border border-cyan-400/30"
                      animate={{ scale: [1, 1.07, 1] }}
                      transition={{ duration: 1.8, repeat: Infinity }}
                    >
                      <div className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
                    </motion.div>
                  ) : (
                    <div className="h-2 w-2 rounded-full bg-slate-500 group-hover:bg-slate-400" />
                  )}

                  {typeof onDeleteThread === "function" ? (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        if (confirm("Delete this thread? This cannot be undone.")) {
                          onDeleteThread(thread.thread_id);
                        }
                      }}
                      aria-label="Delete thread"
                      className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-rose-500/10 bg-rose-500/5 text-rose-300 transition-colors hover:bg-rose-500/10"
                      type="button"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  ) : null}
                </div>
              </div>
            </motion.div>
          );
        })
      )}
    </div>
  );
}

function formatDate(dateString: string) {
  try {
    const date = new Date(dateString);
    const now = new Date();
    const diffMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));

    if (diffMinutes < 1) return "just now";
    if (diffMinutes < 60) return `${diffMinutes}m ago`;

    const diffHours = Math.floor(diffMinutes / 60);
    if (diffHours < 24) return `${diffHours}h ago`;

    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString();
  } catch {
    return "";
  }
}

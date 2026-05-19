"use client";

import { motion } from "framer-motion";
import { ThreadRecord } from "@/lib/types";
import { Clock } from "lucide-react";
import { getThreadMetadata } from "@/lib/storage";

interface ThreadListProps {
  threads: ThreadRecord[];
  activeThreadId: string | null;
  onSelectThread: (threadId: string) => void;
}

export function ThreadList({ threads, activeThreadId, onSelectThread }: ThreadListProps) {
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
          const companyName = metadata?.company_name || "Untitled Project";
          const agent = metadata?.agent_invoke.replace(/_/g, " ").toUpperCase() || "ANALYST";
          const updatedAt = metadata?.updated_at ? formatDate(metadata.updated_at) : "";

          return (
            <motion.button
              key={thread.thread_id}
              whileHover={{ x: 2 }}
              whileTap={{ scale: 0.99 }}
              onClick={() => onSelectThread(thread.thread_id)}
              className={`group relative flex w-full flex-col rounded-2xl border px-4 py-3 text-left transition-all ${
                active
                  ? "border-cyan-400/40 bg-gradient-to-r from-cyan-500/15 to-cyan-400/5 shadow-[inset_0_1px_2px_rgba(34,211,238,0.1)]"
                  : "border-white/8 bg-white/4 hover:border-white/15 hover:bg-white/8"
              }`}
            >
              <div className="flex w-full items-start justify-between gap-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <div
                      className={`h-2 w-2 rounded-full transition-all ${
                        active
                          ? "bg-cyan-400 shadow-[0_0_8px_rgba(34,211,238,0.6)]"
                          : "bg-slate-500 group-hover:bg-slate-400"
                      }`}
                    />
                    <p className="font-semibold text-white leading-tight">{companyName}</p>
                  </div>
                  <div className="mt-2 flex flex-wrap items-center gap-2">
                    <span className="text-[10px] font-medium uppercase tracking-wider text-slate-400 bg-white/5 px-2 py-1 rounded-full">
                      {agent}
                    </span>
                    {updatedAt && (
                      <span className="flex items-center gap-1 text-[10px] text-slate-500">
                        <Clock className="h-2.5 w-2.5" />
                        {updatedAt}
                      </span>
                    )}
                  </div>
                </div>
                {active && (
                  <motion.div
                    className="flex h-8 w-8 items-center justify-center rounded-full bg-cyan-400/20 border border-cyan-400/30"
                    animate={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <div className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
                  </motion.div>
                )}
              </div>
            </motion.button>
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

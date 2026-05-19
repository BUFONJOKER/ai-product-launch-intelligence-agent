"use client";

import { motion } from "framer-motion";
import { ThreadRecord } from "@/lib/types";

interface ThreadListProps {
  threads: ThreadRecord[];
  activeThreadId: string | null;
  onSelectThread: (threadId: string) => void;
}

function formatThreadId(threadId: string) {
  return `${threadId.slice(0, 8)}…${threadId.slice(-6)}`;
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

          return (
            <motion.button
              key={thread.thread_id}
              whileHover={{ x: 2 }}
              whileTap={{ scale: 0.99 }}
              onClick={() => onSelectThread(thread.thread_id)}
              className={`flex w-full items-center justify-between rounded-2xl border px-4 py-3 text-left transition-all ${active ? "border-cyan-300/30 bg-cyan-300/10" : "border-white/8 bg-white/4 hover:bg-white/8"}`}
            >
              <div>
                <div className="flex items-center gap-2">
                  <span className={`h-2.5 w-2.5 rounded-full ${active ? "bg-cyan-300" : index % 2 === 0 ? "bg-violet-300" : "bg-slate-400"}`} />
                  <p className="text-sm font-medium text-white">{formatThreadId(thread.thread_id)}</p>
                </div>
                <p className="mt-1 text-xs text-slate-400">{thread.email}</p>
              </div>
              <span className="text-[10px] uppercase tracking-[0.2em] text-slate-500">{active ? "Active" : "Thread"}</span>
            </motion.button>
          );
        })
      )}
    </div>
  );
}

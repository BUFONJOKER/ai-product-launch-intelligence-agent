"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface AgentCardProps {
  title: string;
  description: string;
  selected: boolean;
  onSelect: () => void;
  onStart: () => void;
  icon: LucideIcon;
  accent?: string;
}

export function AgentCard({ title, description, selected, onSelect, onStart, icon: Icon, accent = "cyan" }: AgentCardProps) {
  return (
    <motion.article
      role="button"
      tabIndex={0}
      onClick={onSelect}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onSelect();
        }
      }}
      whileHover={{ y: -4 }}
      transition={{ type: "spring", stiffness: 420, damping: 28 }}
      className={`group relative overflow-hidden rounded-[1.7rem] border p-5 text-left transition-all ${selected ? "border-cyan-300/30 bg-cyan-300/10" : "border-white/10 bg-white/5 hover:bg-white/8"}`}
    >
      <div className={`absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(125,211,252,0.12),transparent_35%)] ${accent === "violet" ? "opacity-100" : "opacity-70"}`} />
      <div className="relative flex h-full flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className={`flex h-12 w-12 items-center justify-center rounded-2xl border ${selected ? "border-cyan-300/30 bg-cyan-300/15" : "border-white/10 bg-white/6"}`}>
            <Icon className={`h-5 w-5 ${accent === "violet" ? "text-violet-200" : "text-cyan-200"}`} />
          </div>
          <span className={`rounded-full px-3 py-1 text-[11px] uppercase tracking-[0.24em] ${selected ? "bg-cyan-300/15 text-cyan-100" : "bg-white/6 text-slate-400"}`}>
            {selected ? "Selected" : "Agent"}
          </span>
        </div>

        <div className="space-y-2">
          <h3 className="text-xl font-semibold tracking-[-0.03em] text-white">{title}</h3>
          <p className="text-sm leading-7 text-slate-300">{description}</p>
        </div>

        <div className="mt-auto flex items-center justify-between">
          <span className="text-xs uppercase tracking-[0.24em] text-slate-500">Hover for focus</span>
          <button
            type="button"
            onClick={(event) => {
              event.stopPropagation();
              onStart();
            }}
            className="rounded-full bg-white px-4 py-2 text-sm font-medium text-slate-950 transition-transform hover:scale-[1.02]"
          >
            Start Agent
          </button>
        </div>
      </div>
    </motion.article>
  );
}

import { StreamEvent } from "@/lib/types";

interface SseStatusIndicatorProps {
  status: "idle" | "starting" | "streaming" | "loading-response" | "complete" | "error";
  latestEvent?: StreamEvent | null;
}

export function SseStatusIndicator({ status, latestEvent }: SseStatusIndicatorProps) {
  const labelMap = {
    idle: "Idle",
    starting: "Starting run",
    streaming: "Streaming orchestration",
    "loading-response": "Loading final state",
    complete: "Complete",
    error: "Error",
  } as const;

  return (
    <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/6 px-3 py-1 text-xs text-slate-200">
      <span
        className={`h-2 w-2 rounded-full ${status === "error" ? "bg-rose-300" : status === "complete" ? "bg-emerald-300" : "bg-cyan-300 animate-pulse"}`}
      />
      <span>{labelMap[status]}</span>
      {latestEvent ? <span className="text-slate-400">{latestEvent.node ?? latestEvent.tool ?? latestEvent.thread_id ?? ""}</span> : null}
    </div>
  );
}

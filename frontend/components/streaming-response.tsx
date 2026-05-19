"use client";

import { useEffect, useMemo, useState } from "react";
import { StreamEvent } from "@/lib/types";
import { SseStatusIndicator } from "@/components/sse-status-indicator";
import { TimerBadge } from "@/components/timer-badge";
import { MarkdownRenderer } from "@/components/markdown-renderer";
import { AgentInvoke } from "@/lib/types";
import { loadWorkspaceHistory } from "@/lib/storage";

interface StreamingResponseProps {
  status: "idle" | "starting" | "streaming" | "loading-response" | "complete" | "error";
  events: StreamEvent[];
  threadId: string | null;
  elapsedMs: number;
  error?: string | null;
  companyName?: string;
  finalResponse?: unknown;
  selectedAgent: AgentInvoke;
}

function getSelectedAgentOutput(value: unknown, selectedAgent: AgentInvoke) {
  if (typeof value === "string") {
    return value;
  }

  if (!value) {
    return "";
  }

  if (typeof value === "object" && value !== null) {
    const record = value as Record<string, unknown>;
    const keyMap = {
      launch_metrics_specialist: "launch_metrics_specialist_agent_output",
      market_sentiment_specialist: "market_sentiment_specialist_agent_output",
      product_launch_analyst: "product_launch_analyst_agent_output",
    } as const;

    const selected = record[keyMap[selectedAgent]];

    if (typeof selected === "string") {
      return selected;
    }
  }

  return "";
}

function getAgentHeading(selectedAgent: AgentInvoke): string {
  const headingMap = {
    launch_metrics_specialist: "Product Launch Metrics",
    market_sentiment_specialist: "Market Sentiment",
    product_launch_analyst: "Product Launch Analysis",
  } as const;

  return headingMap[selectedAgent];
}

export function StreamingResponse({ status, events, threadId, elapsedMs, error, finalResponse, selectedAgent, companyName }: StreamingResponseProps) {
  const [visibleText, setVisibleText] = useState("");
  const text = useMemo(() => getSelectedAgentOutput(finalResponse, selectedAgent), [finalResponse, selectedAgent]);
  const isRunning = status === "starting" || status === "streaming" || status === "loading-response";

  useEffect(() => {
    if (status !== "complete" || !text) {
      return;
    }

    setVisibleText(text);
  }, [status, text]);

  const latestEvent = events.at(-1) ?? null;

  return (
    <section className="glass-panel rounded-[2rem] p-5 lg:p-6">
      <div className="mb-6 pb-6 border-b border-white/10">
        <div className="flex flex-col gap-2 lg:gap-3">
          <div className="flex flex-wrap items-baseline gap-2 lg:gap-3">
            <h2 className="text-3xl lg:text-4xl font-bold text-white">{companyName ?? "Untitled Project"}</h2>
            {companyName ? (
              <p className="text-sm text-slate-400 lg:ml-2">{getAgentHeading(selectedAgent)}</p>
            ) : null}
          </div>
          <div className="flex flex-wrap items-center gap-2 lg:gap-3">
            <span className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-cyan-400/10 border border-cyan-400/30 px-4 py-2 text-sm font-semibold text-cyan-100">
              <span className="h-2 w-2 rounded-full bg-cyan-400" />
              Agent: {selectedAgent.replace(/_/g, " ")}
            </span>
            <span className="text-sm font-medium text-slate-300">{companyName ? "" : ""}</span>
          </div>
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-4 text-xs text-slate-400">
          {/* try to show last saved run timestamp if available in workspace history */}
          <span>
            Generated: {(() => {
              try {
                const history = loadWorkspaceHistory();
                const entry = threadId ? history.find((h) => h.thread_id === threadId) : null;
                return entry?.updated_at ? new Date(entry.updated_at).toLocaleString() : new Date().toLocaleString();
              } catch {
                return new Date().toLocaleString();
              }
            })()}
          </span>
          <span>Duration: {Math.round(elapsedMs / 1000)}s</span>
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Live stream</p>
          <h2 className="mt-1 text-2xl font-semibold tracking-[-0.03em] text-white">Agent execution console</h2>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <SseStatusIndicator status={status} latestEvent={latestEvent} />
          <TimerBadge ms={elapsedMs} />
        </div>
      </div>

      <div className={`mt-5 grid gap-5 ${isRunning ? "xl:grid-cols-[0.42fr_0.58fr]" : "grid-cols-1"}`}>
        {isRunning ? (
          <div className="rounded-[1.6rem] border border-white/8 bg-white/4 p-4">
            <div className="mb-4 flex items-center justify-between">
              <p className="text-sm font-medium text-white">Event trace</p>
              <span className="text-xs text-slate-500">{threadId ? threadId.slice(0, 8) : "pending"}</span>
            </div>
            <div className="space-y-2">
              {events.length === 0 ? (
                <p className="rounded-2xl border border-dashed border-white/10 px-4 py-10 text-center text-sm text-slate-400">
                  Streaming events will appear here once the agent starts.
                </p>
              ) : (
                events.map((event, index) => (
                  <div key={`${event.type}-${index}`} className="rounded-2xl border border-white/8 bg-[#081227] px-4 py-3 text-sm text-slate-300">
                    <span className="mr-2 inline-flex rounded-full bg-white/8 px-2 py-0.5 text-[10px] uppercase tracking-[0.2em] text-slate-400">
                      {event.type}
                    </span>
                    <span>{event.node ?? event.tool ?? event.thread_id ?? ""}</span>
                  </div>
                ))
              )}
            </div>
            {error ? <p className="mt-4 rounded-2xl border border-rose-400/20 bg-rose-400/10 px-4 py-3 text-sm text-rose-100">{error}</p> : null}
          </div>
        ) : null}

        <div className="rounded-[1.6rem] border border-white/8 bg-white/4 p-4">
          <div className="mb-4 flex items-center justify-between">
            <p className="text-sm font-medium text-white">Agent response</p>
            <span className="text-xs uppercase tracking-[0.2em] text-slate-500">{selectedAgent.replace(/_/g, " ")}</span>
          </div>

          {status === "complete" && text ? (
            <div className="rounded-3xl border border-white/8 bg-[#07101f] p-5">
              <h3 className="mb-4 text-center text-3xl font-bold italic text-white">{getAgentHeading(selectedAgent)}</h3>
              <MarkdownRenderer content={visibleText || text} />
            </div>
          ) : (
            <p className="rounded-3xl border border-dashed border-white/10 px-4 py-16 text-center text-sm text-slate-400">
              The completed markdown response will appear here after the agent run finishes.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

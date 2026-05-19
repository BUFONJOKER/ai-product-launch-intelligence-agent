import Link from "next/link";
import { ArrowRight, BrainCircuit, Sparkles, Radar } from "lucide-react";

const highlights = [
  "Real-time AI orchestration with LangGraph-aware state retention.",
  "Authenticated product launch workspaces backed by thread-aware persistence.",
  "Glassmorphism dashboards, streaming timelines, and markdown-rich outputs.",
];

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-hidden">
      <div className="aurora-blur a1 left-[-80px] top-[-60px]" />
      <div className="aurora-blur a2 right-[-80px] top-[14%]" />
      <div className="aurora-blur a3 left-[20%] bottom-[-70px]" />

      <div className="grid-fade absolute inset-0 opacity-60" />

      <section className="relative mx-auto flex min-h-screen w-full max-w-7xl flex-col justify-center px-6 py-16 lg:px-10">
        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
          <div className="space-y-8">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200 backdrop-blur-xl">
              <Sparkles className="h-4 w-4 text-cyan-300" />
              Product Launch Intelligence, rebuilt for real-time AI workspaces.
            </div>

            <div className="space-y-5">
              <h1 className="max-w-4xl text-5xl font-semibold tracking-[-0.05em] text-white md:text-7xl">
                A cinematic command center for product launch analysis, streaming insight, and AI strategy.
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-slate-300 md:text-xl">
                Analyze product launch metrics, market sentiment, and strategic signals in a premium workspace that mirrors the backend&apos;s thread-aware LangGraph orchestration.
              </p>
            </div>

            <div className="flex flex-wrap gap-4">
              <Link
                href="/auth/signup"
                className="group inline-flex items-center gap-2 rounded-full bg-white px-6 py-3 text-sm font-medium text-slate-950 transition-transform duration-300 hover:scale-[1.02]"
              >
                Start free
                <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
              </Link>
              <Link
                href="/auth/login"
                className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-6 py-3 text-sm font-medium text-white backdrop-blur-xl transition-colors hover:bg-white/10"
              >
                Open dashboard
                <Radar className="h-4 w-4" />
              </Link>
            </div>

            <div className="grid gap-3 sm:grid-cols-3">
              {highlights.map((item) => (
                <div key={item} className="glass-soft rounded-2xl p-4 text-sm text-slate-300">
                  {item}
                </div>
              ))}
            </div>
          </div>

          <div className="glass-panel relative overflow-hidden rounded-[2rem] p-6">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(125,211,252,0.15),_transparent_50%)]" />
            <div className="relative space-y-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Product Launch telemetry</p>
                  <h2 className="mt-2 text-2xl font-semibold text-white">Intelligence stream</h2>
                </div>
                <div className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-200">
                  Live ready
                </div>
              </div>

              <div className="space-y-3">
                {[
                  ["Thread orchestration", "Persisted agent state across product launches"],
                  ["Streaming events", "Node and tool lifecycle updates in real time"],
                  ["AI response", "Markdown-rich strategic output with sources"],
                ].map(([title, description]) => (
                  <div key={title} className="rounded-2xl border border-white/8 bg-white/5 p-4">
                    <div className="flex items-start gap-3">
                      <div className="mt-1 h-2.5 w-2.5 rounded-full bg-cyan-300 shadow-[0_0_18px_rgba(125,211,252,0.8)]" />
                      <div>
                        <p className="font-medium text-white">{title}</p>
                        <p className="mt-1 text-sm text-slate-400">{description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="rounded-3xl border border-white/10 bg-[#060b1a] p-5">
                <div className="flex items-center gap-2 text-sm text-slate-400">
                  <BrainCircuit className="h-4 w-4 text-cyan-300" />
                  Agent workspace preview
                </div>
                <div className="mt-4 grid gap-3">
                  {[
                    ["launch_metrics_specialist", "KPI analysis and product launch traction"],
                    ["market_sentiment_specialist", "Audience reaction and social perception"],
                    ["product_launch_analyst", "Competitive product launch recommendations"],
                  ].map(([name, desc]) => (
                    <div key={name} className="flex items-center justify-between rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
                      <div>
                        <p className="font-medium text-white">{name}</p>
                        <p className="text-sm text-slate-400">{desc}</p>
                      </div>
                      <div className="h-2.5 w-2.5 rounded-full bg-emerald-300 animate-pulse-soft" />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

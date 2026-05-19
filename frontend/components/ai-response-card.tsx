import { MarkdownRenderer } from "@/components/markdown-renderer";

interface AIResponseCardProps {
  title: string;
  value: unknown;
  accent?: string;
}

export function AIResponseCard({ title, value, accent = "cyan" }: AIResponseCardProps) {
  const content = typeof value === "string" ? value : value ? JSON.stringify(value, null, 2) : "No response available yet.";

  return (
    <article className="glass-soft overflow-hidden rounded-[1.75rem] p-5">
      <div className="mb-4 flex items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-slate-400">{title}</p>
          <h3 className={`mt-1 text-lg font-semibold text-white ${accent === "violet" ? "drop-shadow-[0_0_20px_rgba(167,139,250,0.2)]" : ""}`}>
            Analysis output
          </h3>
        </div>
        <div className={`h-2.5 w-2.5 rounded-full ${accent === "violet" ? "bg-violet-300" : "bg-cyan-300"} shadow-[0_0_16px_rgba(125,211,252,0.75)]`} />
      </div>
      <MarkdownRenderer content={content} />
    </article>
  );
}

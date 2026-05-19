import { ReactNode } from "react";

interface EmptyStateProps {
  title: string;
  description: string;
  action?: ReactNode;
}

export function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="glass-soft flex min-h-[320px] flex-col items-center justify-center rounded-[1.75rem] px-6 py-10 text-center">
      <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl border border-white/10 bg-white/6 text-cyan-200 shadow-[0_0_40px_rgba(34,211,238,0.12)]">
        <span className="text-2xl">✦</span>
      </div>
      <h3 className="text-2xl font-semibold tracking-[-0.03em] text-white">{title}</h3>
      <p className="mt-2 max-w-xl text-sm leading-7 text-slate-300">{description}</p>
      {action ? <div className="mt-6">{action}</div> : null}
    </div>
  );
}

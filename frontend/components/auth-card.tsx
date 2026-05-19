import { ReactNode } from "react";

interface AuthCardProps {
  eyebrow: string;
  title: string;
  subtitle: string;
  children: ReactNode;
}

export function AuthCard({ eyebrow, title, subtitle, children }: AuthCardProps) {
  return (
    <section className="glass-panel relative w-full max-w-xl overflow-hidden rounded-[2rem] p-6 sm:p-8">
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-300/50 to-transparent" />
      <div className="space-y-2">
        <p className="text-xs uppercase tracking-[0.3em] text-slate-400">{eyebrow}</p>
        <h1 className="text-3xl font-semibold tracking-[-0.04em] text-white sm:text-4xl">{title}</h1>
        <p className="max-w-lg text-sm leading-7 text-slate-300 sm:text-base">{subtitle}</p>
      </div>
      <div className="mt-8">{children}</div>
    </section>
  );
}

interface TimerBadgeProps {
  ms: number;
}

export function TimerBadge({ ms }: TimerBadgeProps) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");

  return (
    <div className="inline-flex items-center gap-2 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs font-medium text-cyan-100">
      <span className="h-2 w-2 rounded-full bg-cyan-300 animate-pulse" />
      {minutes}:{seconds}
    </div>
  );
}

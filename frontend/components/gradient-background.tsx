export function GradientBackground() {
  return (
    <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="aurora-blur a1 left-[-100px] top-[-120px]" />
      <div className="aurora-blur a2 right-[-80px] top-[12%]" />
      <div className="aurora-blur a3 bottom-[-80px] left-[18%]" />
      <div className="grid-fade absolute inset-0 opacity-75" />
    </div>
  );
}

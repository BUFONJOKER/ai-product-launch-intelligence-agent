"use client";

import { motion, type HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";

interface AnimatedButtonProps extends HTMLMotionProps<"button"> {
  tone?: "primary" | "secondary" | "ghost";
}

const tones = {
  primary:
    "bg-white text-slate-950 shadow-[0_18px_50px_rgba(255,255,255,0.12)] hover:shadow-[0_22px_60px_rgba(125,211,252,0.18)]",
  secondary: "bg-cyan-400/15 text-cyan-100 border border-cyan-300/20 hover:bg-cyan-400/20",
  ghost: "bg-white/5 text-white border border-white/10 hover:bg-white/10",
};

export function AnimatedButton({ className, tone = "primary", ...props }: AnimatedButtonProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.01 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 500, damping: 30 }}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-full px-5 py-3 text-sm font-medium transition-all duration-300 cursor-pointer disabled:cursor-not-allowed disabled:opacity-60",
        tones[tone],
        className,
      )}
      {...props}
    />
  );
}

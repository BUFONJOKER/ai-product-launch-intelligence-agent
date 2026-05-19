"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Eye, EyeOff, LoaderCircle } from "lucide-react";
import { toast } from "sonner";
import { AnimatedButton } from "@/components/animated-button";
import { AuthCard } from "@/components/auth-card";
import { GradientBackground } from "@/components/gradient-background";
import { useAuth } from "@/hooks/use-auth";
import { login } from "@/lib/api";
import { createAuthStateFromLogin } from "@/lib/session";
import { saveAuthState } from "@/lib/storage";

const schema = z.object({
  email: z.string().email("Enter a valid email address."),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

type LoginFormValues = z.infer<typeof schema>;

export default function LoginPage() {
  const router = useRouter();
  const { auth, hydrated, isSessionExpired } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({ resolver: zodResolver(schema) });

  const onSubmit = handleSubmit(async (values) => {
    try {
      const result = await login(values);
      const authState = createAuthStateFromLogin(result);
      saveAuthState(authState);
      toast.success("Login successful", { description: `Welcome back, ${result.name}.` });
      router.push("/dashboard");
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to log in.");
    }
  });

  useEffect(() => {
    if (!hydrated) {
      return;
    }

    if (auth && !isSessionExpired) {
      router.replace("/dashboard");
    }
  }, [auth, hydrated, isSessionExpired, router]);

  return (
    <main className="relative min-h-screen overflow-hidden px-6 py-10">
      <GradientBackground />
      <div className="relative mx-auto flex min-h-[calc(100vh-5rem)] max-w-6xl items-center justify-center">
        <AuthCard
          eyebrow="Secure access"
          title="Sign in to your launch intelligence workspace"
          subtitle="Resume thread-aware analysis, inspect live agent execution, and review polished strategic outputs."
        >
          <form onSubmit={onSubmit} className="space-y-5">
            <label className="block space-y-2">
              <span className="text-sm text-slate-300">Email</span>
              <input
                type="email"
                {...register("email")}
                className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/15"
                placeholder="you@company.com"
              />
              {errors.email ? <span className="text-xs text-rose-300">{errors.email.message}</span> : null}
            </label>

            <label className="block space-y-2">
              <span className="text-sm text-slate-300">Password</span>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  {...register("password")}
                  className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 pr-12 text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/15"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((value) => !value)}
                  className="absolute inset-y-0 right-3 inline-flex items-center text-slate-400 transition hover:text-white"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.password ? <span className="text-xs text-rose-300">{errors.password.message}</span> : null}
            </label>

            <AnimatedButton type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? <LoaderCircle className="h-4 w-4 animate-spin" /> : null}
              {isSubmitting ? "Authenticating" : "Login"}
            </AnimatedButton>
          </form>

          <div className="mt-6 flex items-center justify-between text-sm text-slate-400">
            <span>Need an account?</span>
            <button type="button" onClick={() => router.push("/auth/signup")} className="text-cyan-200 transition hover:text-cyan-100">
              Create one
            </button>
          </div>
        </AuthCard>
      </div>
    </main>
  );
}

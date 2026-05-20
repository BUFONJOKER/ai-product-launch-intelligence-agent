"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, Save, Eye, EyeOff, Settings } from "lucide-react";
import { toast } from "sonner";
import { GradientBackground } from "@/components/gradient-background";
import { useAuth } from "@/hooks/use-auth";
import { updateUser, ApiError } from "@/lib/api";
import { saveAuthState } from "@/lib/storage";
import { SignUpRequest } from "@/lib/types";

export default function SettingsPage() {
  const router = useRouter();
  const { auth, hydrated, isAuthenticated, clearAuth } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showApiKey, setShowApiKey] = useState(false);
  const [formData, setFormData] = useState<SignUpRequest>({
    name: "",
    email: "",
    password: "",
    api_key_openai: "",
  });

  useEffect(() => {
    if (!hydrated) {
      return;
    }

    if (!isAuthenticated) {
      router.push("/auth/login");
      return;
    }

    if (auth) {
      setFormData({
        name: auth.name || "",
        email: auth.email || "",
        password: "",
        api_key_openai: auth.api_key_openai || "",
      });
    }
  }, [auth, hydrated, isAuthenticated, router]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!formData.name || !formData.email) {
      toast.error("Name and email are required");
      return;
    }

    setIsLoading(true);
    try {
      const updateData: SignUpRequest = {
        name: formData.name,
        email: formData.email,
        password: formData.password || "",
        api_key_openai: formData.api_key_openai,
      };

      const response = await updateUser(updateData);
      toast.success("Profile updated successfully");

      // Update localStorage with new user data
      if (auth) {
        const updated = {
          ...auth,
          name: response.name,
          email: response.email,
          api_key_openai: formData.api_key_openai,
        };
        saveAuthState(updated);
      }

      // Reload to show new data
      router.refresh();
    } catch (error) {
      const message = error instanceof ApiError ? error.message : "Failed to update profile";
      toast.error(message);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <GradientBackground>
      <div className="relative min-h-screen">
        <main className="relative">
          <div className="mx-auto max-w-2xl px-4 py-8 lg:px-8 lg:py-12">
            {/* Header */}
            <div className="mb-8 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => router.back()}
                  className="rounded-lg p-2 hover:bg-white/10 transition-colors"
                  aria-label="Go back"
                >
                  <ArrowLeft className="h-5 w-5 text-slate-400" />
                </button>
                <div>
                  <div className="flex items-center gap-2">
                    <Settings className="h-8 w-8 text-cyan-400" />
                    <h1 className="text-3xl font-bold text-white">Settings</h1>
                  </div>
                  <p className="text-slate-400">Manage your profile and preferences</p>
                </div>
              </div>
            </div>

            {/* Settings Form */}
            <div className="glass-panel rounded-2xl p-6 lg:p-8">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Profile Section */}
                <div className="space-y-4 pb-6 border-b border-white/10">
                  <h2 className="text-lg font-semibold text-white">Profile Information</h2>

                  {/* Name Field */}
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-slate-300 mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder-slate-500 transition-colors focus:border-cyan-300/50 focus:bg-white/8 focus:outline-none"
                      placeholder="Enter your full name"
                    />
                  </div>

                  {/* Email Field */}
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                      Email Address
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-white placeholder-slate-500 transition-colors focus:border-cyan-300/50 focus:bg-white/8 focus:outline-none"
                      placeholder="Enter your email"
                    />
                  </div>
                </div>

                {/* Security Section */}
                <div className="space-y-4 pb-6 border-b border-white/10">
                  <h2 className="text-lg font-semibold text-white">Security</h2>

                  {/* Password Field */}
                  <div>
                    <label htmlFor="password" className="block text-sm font-medium text-slate-300 mb-2">
                      Password (optional)
                    </label>
                    <div className="relative">
                      <input
                        type={showPassword ? "text" : "password"}
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInputChange}
                        className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 pr-10 text-white placeholder-slate-500 transition-colors focus:border-cyan-300/50 focus:bg-white/8 focus:outline-none"
                        placeholder="Leave empty to keep current password"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    </div>
                    <p className="text-xs text-slate-500 mt-1">Leave empty to keep your current password</p>
                  </div>
                </div>

                {/* API Key Section */}
                <div className="space-y-4">
                  <h2 className="text-lg font-semibold text-white">API Configuration</h2>

                  {/* OpenAI API Key Field */}
                  <div>
                    <label htmlFor="api_key_openai" className="block text-sm font-medium text-slate-300 mb-2">
                      OpenAI API Key
                    </label>
                    <div className="relative">
                      <input
                        type={showApiKey ? "text" : "password"}
                        id="api_key_openai"
                        name="api_key_openai"
                        value={formData.api_key_openai}
                        onChange={handleInputChange}
                        className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 pr-10 text-white placeholder-slate-500 transition-colors focus:border-cyan-300/50 focus:bg-white/8 focus:outline-none"
                        placeholder="Enter your OpenAI API key"
                      />
                      <button
                        type="button"
                        onClick={() => setShowApiKey(!showApiKey)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                      >
                        {showApiKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 pt-6">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="flex-1 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-500 px-4 py-2.5 font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    <Save className="h-4 w-4" />
                    {isLoading ? "Saving..." : "Save Changes"}
                  </button>
                  <button
                    type="button"
                    onClick={() => router.back()}
                    className="rounded-lg border border-white/10 px-4 py-2.5 font-medium text-slate-300 transition-colors hover:bg-white/5"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>

            {/* Logout Button */}
            <div className="mt-6">
              <button
                onClick={() => {
                  clearAuth();
                  router.push("/auth/login");
                }}
                className="w-full rounded-lg border border-rose-400/20 bg-rose-400/10 px-4 py-2.5 font-medium text-rose-100 transition-colors hover:bg-rose-400/20"
              >
                Sign Out
              </button>
            </div>
          </div>
        </main>
      </div>
    </GradientBackground>
  );
}

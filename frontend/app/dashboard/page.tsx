"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { BrainCircuit, Sparkles, BarChart3, Radar, LayoutGrid, LoaderCircle } from "lucide-react";
import { toast } from "sonner";
import { AgentCard } from "@/components/agent-card";
import { AnimatedButton } from "@/components/animated-button";
import { EmptyState } from "@/components/empty-state";
import { GradientBackground } from "@/components/gradient-background";
import { LoadingSkeleton } from "@/components/loading-skeleton";
import { Sidebar } from "@/components/sidebar";
import { StreamingResponse } from "@/components/streaming-response";
import { useAgentRun } from "@/hooks/use-agent-run";
import { useAuth } from "@/hooks/use-auth";
import { useThreads } from "@/hooks/use-threads";
import { createThread, getAgentResponse, ApiError } from "@/lib/api";
import { AgentInvoke, GetAgentResponse, WorkspaceHistoryEntry, WorkspaceRunStatus } from "@/lib/types";
import {
  clearWorkspaceSnapshot,
  loadWorkspaceHistory,
  loadWorkspaceSnapshot,
  saveThreadMetadata,
  saveWorkspaceHistory,
  saveWorkspaceSnapshot,
  upsertWorkspaceHistory,
  removeThreadMetadata
} from "@/lib/storage";
import { deleteUserThread } from "@/lib/api";


const agents: Array<{
  title: string;
  description: string;
  invoke: AgentInvoke;
  icon: typeof BrainCircuit;
  accent?: string;
}> = [
    {
      title: "launch_metrics_specialist",
      description: "Analyzes launch KPIs, growth metrics, and performance trends.",
      invoke: "launch_metrics_specialist",
      icon: BarChart3,
    },
    {
      title: "market_sentiment_specialist",
      description: "Analyzes social sentiment, audience reactions, and market perception.",
      invoke: "market_sentiment_specialist",
      icon: Radar,
      accent: "violet",
    },
    {
      title: "product_launch_analyst",
      description: "Provides strategic launch analysis, recommendations, and competitor insights.",
      invoke: "product_launch_analyst",
      icon: Sparkles,
    },
  ];

export default function DashboardPage() {
  const router = useRouter();
  const { auth, hydrated, clearAuth, isSessionExpired: authExpired } = useAuth();
  const { threads, loading: threadsLoading, refresh: refreshThreads } = useThreads(auth?.email ?? null);
  const agentRun = useAgentRun(auth?.api_key_openai ?? null);
  const [workspaceHistory, setWorkspaceHistory] = useState<WorkspaceHistoryEntry[]>(() => loadWorkspaceHistory());
  const [initialSnapshot] = useState(() => loadWorkspaceSnapshot());

  const [searchQuery, setSearchQuery] = useState("");
  const [companyName, setCompanyName] = useState(initialSnapshot?.companyName ?? "");
  const [selectedAgent, setSelectedAgent] = useState<AgentInvoke>(initialSnapshot?.agentInvoke ?? "product_launch_analyst");
  const [activeThreadId, setActiveThreadId] = useState<string | null>(initialSnapshot?.activeThreadId ?? null);
  const [manualThreadId, setManualThreadId] = useState<string | null>(initialSnapshot?.activeThreadId ?? null);
  const [restoredResponse, setRestoredResponse] = useState<GetAgentResponse | null>(initialSnapshot?.response ?? null);
  const [restoringThread, setRestoringThread] = useState(false);
  const [workspaceStatus, setWorkspaceStatus] = useState<WorkspaceRunStatus>(initialSnapshot?.response ? "complete" : "idle");

  const handleDeleteThread = async (threadId: string) => {
    if (!auth?.email) {
      toast.error("Sign in to delete threads.");
      return;
    }

    try {
      await deleteUserThread(auth.email, threadId);
      // remove local metadata & local workspace history
      removeThreadMetadata(threadId);
      setWorkspaceHistory((prev) => prev.filter((h) => h.thread_id !== threadId));
      if (activeThreadId === threadId) {
        setActiveThreadId(null);
        setManualThreadId(null);
        clearWorkspaceSnapshot();
      }
      await refreshThreads();
      toast.success("Thread deleted");
    } catch (err) {
      toast.error(err instanceof ApiError ? err.message : "Failed to delete thread.");
    }
  };

  useEffect(() => {
    if (hydrated && !auth) {
      router.replace("/auth/login");
    }
  }, [hydrated, auth, router]);

  useEffect(() => {
    if (hydrated && auth && authExpired) {
      toast.warning("Your session expired. Please sign in again.");
      clearAuth();
      clearWorkspaceSnapshot();
      router.replace("/auth/login");
    }
  }, [auth, authExpired, clearAuth, hydrated, router]);

  useEffect(() => {
    saveWorkspaceHistory(workspaceHistory);
  }, [workspaceHistory]);

  useEffect(() => {
    if (!activeThreadId) {
      return;
    }

    saveWorkspaceSnapshot({
      activeThreadId,
      companyName,
      agentInvoke: selectedAgent,
      response: restoredResponse ?? agentRun.response,
    });
  }, [activeThreadId, companyName, selectedAgent, restoredResponse, agentRun.response]);

  const visibleThreads = useMemo(() => {
    return threads.filter((thread) => thread.thread_id.includes(searchQuery) || thread.email.includes(searchQuery));
  }, [searchQuery, threads]);

  const getCachedWorkspaceEntry = (threadId: string, agent: AgentInvoke) => {
    return workspaceHistory.find((entry) => entry.thread_id === threadId && entry.agent_invoke === agent && Boolean(entry.response));
  };

  const restoreThread = async (threadId: string) => {
    if (!auth?.api_key_openai) {
      toast.error("Your OpenAI API key is missing from local storage.");
      return;
    }

    setActiveThreadId(threadId);
    setManualThreadId(threadId);
    setRestoringThread(true);
    setRestoredResponse(null);

    const existingHistory = workspaceHistory.find((entry) => entry.thread_id === threadId);
    if (existingHistory?.response) {
      setCompanyName(existingHistory.company_name);
      setSelectedAgent(existingHistory.agent_invoke);
      setRestoredResponse(existingHistory.response);
      setWorkspaceStatus(existingHistory.status);
      // persist metadata so sidebar shows company/product
      saveThreadMetadata({ thread_id: threadId, company_name: existingHistory.company_name, agent_invoke: existingHistory.agent_invoke });
      setRestoringThread(false);
      return;
    }

    try {
      const response = await getAgentResponse({ thread_id: threadId, api_key_openai: auth.api_key_openai });
      setRestoredResponse(response);
      setWorkspaceStatus("complete");
      const existing = workspaceHistory.find((entry) => entry.thread_id === threadId);
      if (existing) {
        const next = upsertWorkspaceHistory({
          ...existing,
          response,
          status: "complete",
          updated_at: new Date().toISOString(),
        });
        setWorkspaceHistory(next);
      }
    } catch (error) {
      toast.error(error instanceof ApiError ? error.message : "Failed to load thread state.");
    } finally {
      setRestoringThread(false);
    }
  };

  const createNewThread = async () => {
    if (!auth?.email) {
      toast.error("Sign in to create a thread.");
      return;
    }

    try {
      const response = await createThread({ email: auth.email });
      setActiveThreadId(response.thread_id);
      setManualThreadId(response.thread_id);
      setRestoredResponse(null);
      setCompanyName("");
      setWorkspaceStatus("idle");
      clearWorkspaceSnapshot();
      toast.success("Thread created", { description: "A new product launch workspace is ready." });
      await refreshThreads();
    } catch (error) {
      toast.error(error instanceof ApiError ? error.message : "Failed to create thread.");
    }
  };

  const startAgent = async () => {
    if (!auth?.api_key_openai || !auth?.email) {
      toast.error("Sign in again to restore your session key.");
      return;
    }

    if (!manualThreadId) {
      toast.error("Create a thread before starting an agent.");
      return;
    }

    if (!companyName.trim()) {
      toast.error("Enter a company & product before starting the agent.");
      return;
    }

    // require at least two words (company + product)
    if (companyName.trim().split(/\s+/).length < 2) {
      toast.error("Please enter both company and product (e.g. Apple Vision Pro).");
      return;
    }

    const cachedEntry = getCachedWorkspaceEntry(manualThreadId, selectedAgent);
    if (cachedEntry?.response) {
      const cachedResponse = cachedEntry.response;

      setRestoredResponse(cachedResponse);
      setWorkspaceStatus("complete");
      saveWorkspaceSnapshot({
        activeThreadId: manualThreadId,
        companyName: companyName.trim(),
        agentInvoke: selectedAgent,
        response: cachedResponse,
      });
      // persist thread metadata so sidebar updates
      if (manualThreadId && companyName?.trim()) {
        saveThreadMetadata({ thread_id: manualThreadId, company_name: companyName.trim(), agent_invoke: selectedAgent });
      }

      toast.success("Loaded saved response", {
        description: "This agent response was already generated for the selected thread.",
      });
      return;
    }

    try {
      setRestoredResponse(null);
      setWorkspaceStatus("starting");
      const completedResponse = await agentRun.run({
        thread_id: manualThreadId,
        api_key_openai: auth.api_key_openai,
        company_name: companyName.trim(),
        agent_invoke: selectedAgent,
      });
      const normalizedResponse = completedResponse ?? null;

      setWorkspaceStatus("complete");

      const snapshot = {
        id: `${manualThreadId}-${selectedAgent}`,
        thread_id: manualThreadId,
        company_name: companyName.trim(),
        agent_invoke: selectedAgent,
        status: "complete" as WorkspaceRunStatus,
        updated_at: new Date().toISOString(),
        response: normalizedResponse,
        response_preview: typeof normalizedResponse?.product_launch_analyst_agent_output === "string"
          ? normalizedResponse.product_launch_analyst_agent_output.slice(0, 180)
          : typeof normalizedResponse?.market_sentiment_specialist_agent_output === "string"
            ? normalizedResponse.market_sentiment_specialist_agent_output.slice(0, 180)
            : typeof normalizedResponse?.launch_metrics_specialist_agent_output === "string"
              ? normalizedResponse.launch_metrics_specialist_agent_output.slice(0, 180)
              : null,
      } satisfies WorkspaceHistoryEntry;

      setWorkspaceHistory(upsertWorkspaceHistory(snapshot));
      saveWorkspaceSnapshot({
        activeThreadId: manualThreadId,
        companyName: companyName.trim(),
        agentInvoke: selectedAgent,
        response: normalizedResponse,
      });
      // persist thread metadata for nicer thread cards
      saveThreadMetadata({ thread_id: manualThreadId, company_name: companyName.trim(), agent_invoke: selectedAgent });
      await refreshThreads();
    } catch (error) {
      setWorkspaceStatus("error");
      toast.error(error instanceof ApiError ? error.message : "Agent run failed.");
    }
  };

  const handleLogout = () => {
    clearAuth();
    router.replace("/auth/login");
  };

  const finalResponse = agentRun.response ?? restoredResponse;
  const streamStatus = agentRun.status === "idle" ? workspaceStatus : agentRun.status;

  if (!hydrated || !auth) {
    return (
      <main className="relative flex min-h-screen items-center justify-center px-6 py-10">
        <GradientBackground />
        <div className="glass-panel relative z-10 flex w-full max-w-xl flex-col items-center rounded-[2rem] p-8 text-center">
          <LoaderCircle className="h-7 w-7 animate-spin text-cyan-200" />
          <p className="mt-4 text-lg font-medium text-white">Loading secure workspace</p>
          <p className="mt-2 text-sm text-slate-400">Restoring your session and thread-aware state.</p>
        </div>
      </main>
    );
  }

  return (
    <main className="relative min-h-screen overflow-hidden px-4 py-4 lg:px-6 lg:py-6">
      <GradientBackground />

      <div className="relative mx-auto grid min-h-[calc(100vh-2rem)] max-w-[1700px] gap-4 lg:grid-cols-[340px_1fr]">
        <Sidebar
          userName={auth.name}
          userEmail={auth.email}
          threads={visibleThreads}
          activeThreadId={activeThreadId}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          onCreateThread={createNewThread}
          onSelectThread={restoreThread}
          onDeleteThread={handleDeleteThread}
          onLogout={handleLogout}
          loading={threadsLoading}
        />

        <section className="flex flex-col gap-4">
          <div className="glass-panel rounded-[2rem] p-5 lg:p-6">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Product Launch workspace</p>
                <h1 className="mt-2 text-3xl font-semibold tracking-[-0.04em] text-white lg:text-5xl">Cinematic AI agent cockpit</h1>
                <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-300 lg:text-base">
                  Create a thread, select a specialist, and stream the workflow while the backend persists each agent state in LangGraph.
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200">
                  <LayoutGrid className="h-4 w-4 text-cyan-200" />
                  {activeThreadId ? activeThreadId.slice(0, 8) : "No active thread"}
                </div>
                {agentRun.isBusy ? <div className="inline-flex rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-2 text-sm text-cyan-100">Streaming</div> : null}
              </div>
            </div>
          </div>

          <div className="glass-panel rounded-[2rem] p-5 lg:p-6">
            <div className="grid gap-5 lg:grid-cols-[1fr_auto] lg:items-end">
              <label className="space-y-5">
                <span className="text-sm text-slate-300">Company & Product</span>
                <input
                  value={companyName}
                  onChange={(event) => setCompanyName(event.target.value)}
                  placeholder="Enter Company & Product Name (e.g. Apple Vision Pro)"
                  className="h-11 w-full rounded-full border border-white/8 bg-gradient-to-r from-white/3 to-white/6 px-5 text-sm font-medium text-white outline-none transition-shadow duration-200 focus:border-cyan-300/40 focus:shadow-[0_8px_30px_rgba(34,211,238,0.12)]"
                />
              </label>

              <div className="flex flex-wrap items-center gap-3">
                <AnimatedButton tone="ghost" onClick={() => void createNewThread()}>
                  <Sparkles className="h-4 w-4" />
                  New Thread
                </AnimatedButton>
                <AnimatedButton onClick={() => void startAgent()} disabled={agentRun.isBusy}>
                  {agentRun.isBusy ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <BrainCircuit className="h-4 w-4" />}
                  {agentRun.isBusy ? "Running agent" : "Start Agent"}
                </AnimatedButton>
              </div>
            </div>
          </div>

          <div className="grid gap-4 lg:grid-cols-3">
            {agents.map((agent) => (
              <AgentCard
                key={agent.invoke}
                title={agent.title}
                description={agent.description}
                selected={selectedAgent === agent.invoke}
                icon={agent.icon}
                accent={agent.accent}
                onSelect={() => setSelectedAgent(agent.invoke)}
                onStart={() => {
                  setSelectedAgent(agent.invoke);
                  const cachedEntry = activeThreadId ? getCachedWorkspaceEntry(activeThreadId, agent.invoke) : null;

                  if (cachedEntry?.response) {
                    setSelectedAgent(agent.invoke);
                    setRestoredResponse(cachedEntry.response);
                    setWorkspaceStatus("complete");
                    saveWorkspaceSnapshot({
                      activeThreadId,
                      companyName,
                      agentInvoke: agent.invoke,
                      response: cachedEntry.response,
                    });
                    // persist metadata so sidebar shows company/product for this thread
                    if (activeThreadId && companyName?.trim()) {
                      saveThreadMetadata({ thread_id: activeThreadId, company_name: companyName.trim(), agent_invoke: agent.invoke });
                    }
                    toast.success("Loaded saved response", {
                      description: "This agent response was already generated for the selected thread.",
                    });
                    return;
                  }

                  void startAgent();
                }}
              />
            ))}
          </div>

          {threadsLoading ? <LoadingSkeleton className="h-72 rounded-[2rem]" /> : null}

          <StreamingResponse
            status={streamStatus}
            events={agentRun.events}
            threadId={agentRun.threadId ?? manualThreadId}
            elapsedMs={agentRun.elapsedMs}
            error={agentRun.error}
            finalResponse={finalResponse}
            selectedAgent={selectedAgent}
            companyName={companyName}
          />

          {!finalResponse && !agentRun.isBusy && !restoringThread ? (
            <EmptyState
              title="No analysis loaded"
              description="Create a thread, choose a specialist, and start the agent to render the live orchestration and the final markdown response."
            />
          ) : null}

          {restoringThread ? <LoadingSkeleton className="h-48 rounded-[2rem]" /> : null}
        </section>
      </div>
    </main>
  );
}

"use client";

import { useEffect, useRef, useState } from "react";
import { getAgentResponse, startAgentStream, ApiError } from "@/lib/api";
import { AgentRunRequest, GetAgentResponse, StreamEvent } from "@/lib/types";
import { readStreamEvents } from "@/lib/stream";

type RunStatus = "idle" | "starting" | "streaming" | "loading-response" | "complete" | "error";

export function useAgentRun(apiKeyOpenAI?: string | null) {
  const [status, setStatus] = useState<RunStatus>("idle");
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [response, setResponse] = useState<GetAgentResponse | null>(null);
  const [threadId, setThreadId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [startedAt, setStartedAt] = useState<number | null>(null);
  const [now, setNow] = useState<number>(() => Date.now());
  const currentRunId = useRef(0);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (!startedAt) {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      return;
    }

    if (status === "complete" || status === "error") {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      return;
    }

    if (!timerRef.current) {
      timerRef.current = window.setInterval(() => {
        setNow(Date.now());
      }, 1000);
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [startedAt, status]);

  const elapsedMs = startedAt ? now - startedAt : 0;

  const reset = () => {
    setEvents([]);
    setResponse(null);
    setThreadId(null);
    setError(null);
    setStartedAt(null);
    setStatus("idle");
  };

  const run = async (payload: AgentRunRequest) => {
    if (!apiKeyOpenAI) {
      throw new Error("Missing OpenAI API key in local storage.");
    }

    const runId = currentRunId.current + 1;
    currentRunId.current = runId;

    setStatus("starting");
    setError(null);
    setEvents([]);
    setResponse(null);
    setStartedAt(Date.now());

    let streamedThreadId = payload.thread_id;

    try {
      const streamResponse = await startAgentStream({
        ...payload,
        api_key_openai: apiKeyOpenAI,
      });

      setStatus("streaming");

      await readStreamEvents(streamResponse, (event) => {
        if (currentRunId.current !== runId) {
          return;
        }

        setEvents((previous) => [...previous, event]);

        if (event.type === "thread_id" && event.thread_id) {
          streamedThreadId = event.thread_id;
          setThreadId(event.thread_id);
        }
      });

      setStatus("loading-response");

      const finalThreadId = streamedThreadId;

      const finalResponse = await getAgentResponse({
        thread_id: finalThreadId,
        api_key_openai: apiKeyOpenAI,
      });

      if (currentRunId.current !== runId) {
        return;
      }

      setThreadId(finalThreadId);
      setResponse(finalResponse);
      setStatus("complete");

      return finalResponse;
    } catch (caughtError) {
      const message = caughtError instanceof ApiError ? caughtError.message : "Failed to run agent";
      setStatus("error");
      setError(message);
      throw caughtError;
    }
  };

  return {
    status,
    events,
    response,
    threadId,
    error,
    elapsedMs,
    run,
    reset,
    isBusy: status === "starting" || status === "streaming" || status === "loading-response",
  };
}

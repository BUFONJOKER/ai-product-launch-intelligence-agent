import {
  AgentRunRequest,
  BackendErrorBody,
  CreateThreadRequest,
  CreateThreadResponse,
  GetAgentRequest,
  GetAgentResponse,
  LoginRequest,
  LoginResponse,
  SignUpRequest,
  SignUpResponse,
  ThreadRecord,
} from "@/lib/types";

export class ApiError extends Error {
  status: number;
  body?: BackendErrorBody;

  constructor(message: string, status: number, body?: BackendErrorBody) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

const API_BASE = "/api/proxy";

async function parseErrorBody(response: Response): Promise<BackendErrorBody | undefined> {
  const contentType = response.headers.get("content-type") ?? "";

  if (!contentType.includes("application/json")) {
    return undefined;
  }

  try {
    return (await response.json()) as BackendErrorBody;
  } catch {
    return undefined;
  }
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const errorBody = await parseErrorBody(response);
    const message = errorBody?.detail ?? errorBody?.message ?? `Request failed with status ${response.status}`;
    throw new ApiError(message, response.status, errorBody);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export async function signup(request: SignUpRequest) {
  return requestJson<SignUpResponse>("/api/users/signup", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function login(request: LoginRequest) {
  return requestJson<LoginResponse>("/api/users/login", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function updateUser(request: SignUpRequest) {
  return requestJson<SignUpResponse>("/api/users/update_user", {
    method: "PUT",
    body: JSON.stringify(request),
  });
}

export async function createThread(request: CreateThreadRequest) {
  return requestJson<CreateThreadResponse>("/api/users/add_user_agent_thread_id", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function getUserThreads(email: string) {
  return requestJson<ThreadRecord[] | string>(`/api/users/get_user_threads/${encodeURIComponent(email)}`);
}

export async function getAgentResponse(request: GetAgentRequest) {
  return requestJson<GetAgentResponse>("/api/agent_runs/get_agent_response", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function startAgentStream(request: AgentRunRequest) {
  const response = await fetch(`${API_BASE}/api/agent_runs/start_agent`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok || !response.body) {
    const errorBody = await parseErrorBody(response);
    const message = errorBody?.detail ?? errorBody?.message ?? `Request failed with status ${response.status}`;
    throw new ApiError(message, response.status, errorBody);
  }

  return response;
}

export type AgentInvoke =
  | "product_launch_analyst"
  | "market_sentiment_specialist"
  | "launch_metrics_specialist";

export interface SignUpRequest {
  name: string;
  email: string;
  password: string;
  api_key_openai: string;
}

export interface SignUpResponse {
  name: string;
  email: string;
  message: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: "bearer" | string;
  name: string;
  email: string;
  api_key_openai: string;
  message: string;
}

export interface CreateThreadRequest {
  email: string;
}

export interface CreateThreadResponse {
  email: string;
  thread_id: string;
  message: string;
}

export interface ThreadRecord {
  email: string;
  thread_id: string;
}

export interface AgentRunRequest {
  thread_id: string;
  api_key_openai: string;
  company_name: string;
  agent_invoke: AgentInvoke;
}

export interface GetAgentRequest {
  thread_id: string;
  api_key_openai: string;
}

export interface GetAgentResponse {
  thread_id: string;
  launch_metrics_specialist_agent_output: unknown;
  market_sentiment_specialist_agent_output: unknown;
  product_launch_analyst_agent_output: unknown;
}

export interface UserAuthState {
  access_token: string;
  name: string;
  email: string;
  api_key_openai: string;
  expires_at: number;
}

export type WorkspaceRunStatus = "idle" | "starting" | "streaming" | "loading-response" | "complete" | "error";

export interface WorkspaceHistoryEntry {
  id: string;
  thread_id: string;
  company_name: string;
  agent_invoke: AgentInvoke;
  status: WorkspaceRunStatus;
  updated_at: string;
  response?: GetAgentResponse | null;
  response_preview?: string | null;
}

export interface WorkspaceSnapshot {
  activeThreadId: string | null;
  companyName: string;
  agentInvoke: AgentInvoke;
  response: GetAgentResponse | null;
}

export interface BackendErrorBody {
  detail?: string;
  message?: string;
  error?: string;
}

export interface StreamEvent {
  type: "thread_id" | "node_start" | "node_end" | "tool_start" | "tool_end";
  thread_id?: string;
  node?: string;
  tool?: string;
}

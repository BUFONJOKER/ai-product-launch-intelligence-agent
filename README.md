# AI Product Launch Intelligence Agent 🚀

A developer-focused, production-ready multi-agent system designed to analyze product launches in real time. Built with a high-performance **FastAPI** backend powered by **LangGraph** stateful workflows, it features a sleek **Next.js 14 (App Router)** frontend with robust Server-Sent Events (SSE) streaming capabilities.

---

## ✨ Features

### 💻 Frontend

* **Real-Time Streaming UX:** Progressively renders live agent node transitions and tool invocations via SSE.
* **Server-Side API Proxying:** Eliminates cross-origin (CORS) frustrations and protects internal system endpoints.
* **Adaptive Architecture:** Fully optimized for Next.js App Router layout paradigms using lightweight React hooks.

### ⚙️ Backend

* **Stateful Multi-Agent Workflows:** Built on LangGraph to manage complex, multi-step conversation histories using unique thread IDs.
* **Deep Web Integration:** Employs specialized Tavily Search tools for automated competitor analysis.
* **Enterprise-Grade Security:** Features JWT auth handling backed by cryptographic AES-256 encryption for user-provided API keys.

---

## 🤖 Meet the Specialist Agents

The execution engine coordinates three dedicated AI nodes to dissect any target market event all agents used llm `GPT-5-nano by openai`:

1. **Product Launch Analyst (`product_launch_analyst`):** Conducts evidence-driven positioning matrixes, cataloging baseline structural strengths and structural product weaknesses.
2. **Market Sentiment Specialist (`market_sentiment_specialist`):** Scrapes community trends and social data points to isolate public perception shifts and notable influencer reactions.
3. **Launch Metrics Specialist (`launch_metrics_specialist`):** Calculates performance indicators, financial impacts, and expected user acquisition trajectories.

---

## 🌐 Live Deployments & Artifacts

### 💻 Frontend (Next.js)

* **Live Demo:** [Hugging Face Space Live UI](https://bufon-joker-ai-product-launch-intelligence-agent-c4840fe.hf.space/)
* **Docker Hub Image:** [`bufonjoker/ai-product-launch-intelligence-agent-frontend`](https://hub.docker.com/r/bufonjoker/ai-product-launch-intelligence-agent-frontend)

### ⚙️ Backend (FastAPI)

* **API Base Endpoint:** [Hugging Face Space Live API](https://bufon-joker-ai-product-launch-intelligence-agent-backend.hf.space)
* **Interactive Docs:** [API Docs](https://bufon-joker-ai-product-launch-intelligence-agent-backend.hf.space/docs)
* **Docker Hub Image:** [`bufonjoker/ai-product-launch-intelligence-agent-backend:latest`](https://www.google.com/search?q=https://hub.docker.com/r/bufonjoker/ai-product-launch-intelligence-agent-backend)

---

## 🛠️ Quick Start & Environment Setup

### ⚙️ Backend Setup (FastAPI)

#### Prerequisites

* Python 3.11+
* PostgreSQL 12+
* `uv` (Recommended package manager)

```bash
# Navigate & sync dependencies
cd backend
uv sync

# Set up your environment variables
cp .env.example .env

```

Ensure your `.env` contains the required keys:

```env
TAVILY_API_KEY=Your_Tavily_API_Key_Here
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=Your_LangSmith_API_Key_Here
LANGSMITH_PROJECT=Your_LangSmith_Project_Name
DB_URL=Supabase_Database_URL_Here
DB_URL_API=Supabase_Database_URL_Here
DEBUG=True
ACCESS_TOKEN_SECRET_KEY=Your_JWT_Secret_Key_Here
ENCRYPTION_MASTER_KEY=Your_32_Byte_Hexadecimal_Key_Here

```

> **Pro Tip:** Generate your master key quickly using: `python -c "import secrets; print(secrets.token_hex(16))"`

```bash
# Run database migrations
uv run alembic upgrade head

# Start development server
python -m main

```

The backend service will now be active at `http://localhost:8000`.

---

### 💻 Frontend Setup (Next.js)

#### Prerequisites

* Node.js 18+
* npm / pnpm / yarn

```bash
# Navigate & install packages
cd frontend
npm install

# Configure local variables
nano .env.local

```

Add your backend proxy routing endpoints to `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_API_URL=http://localhost:8000

```

```bash
# Fire up local development hot-reload
npm run dev

```

The application interface will now be accessible at `http://localhost:3000`.

---


## 🐳 Containerized Production Deployment

### Run Backend Container

```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name launch-agent-backend \
  bufonjoker/ai-product-launch-intelligence-agent-backend:latest

```

### Run Frontend Container

```bash
docker run -d \
  -p 3000:3000 \
  -e BACKEND_API_URL="http://your-backend-ip:8000" \
  --name launch-agent-frontend \
  bufonjoker/ai-product-launch-intelligence-agent-frontend:latest

```
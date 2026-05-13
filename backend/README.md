# AI Product Launch Intelligence Agent Backend

A FastAPI-based backend for analyzing product launches using AI-powered specialist agents. The system provides real-time market insights, sentiment analysis, and launch metrics through a LangGraph workflow with stateful conversation management.

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Agents](#agents)
- [API Reference](#api-reference)
- [Setup & Installation](#setup--installation)
- [Environment Configuration](#environment-configuration)
- [Running the Backend](#running-the-backend)
- [API Usage Examples](#api-usage-examples)

## Architecture

The backend uses a **LangGraph-based agentic workflow** with the following components:

```
FastAPI Server
├── User Management (Authentication & Authorization)
├── Agent Execution Engine
│   ├── StateGraph Workflow (LangGraph)
│   ├── Specialist Agent Nodes
│   └── PostgreSQL State Persistence (Checkpointer)
├── API Routes
│   ├── /api/users (User authentication)
│   └── /api/agent_runs (Agent execution)
└── Supporting Services
    ├── Database (SQLAlchemy + Alembic)
    ├── Encryption (API key management)
    ├── Tool Integration (Tavily Search)
    └── Token Management (JWT)
```

### Key Design Patterns

- **Multi-Agent System**: Specialist agents handle different aspects of product launch analysis
- **Thread-Based Conversation State**: Each analysis run has a unique thread ID for state persistence
- **Streaming Responses**: Real-time event streaming via SSE (Server-Sent Events)
- **Stateful Execution**: Previous agent outputs are preserved for multi-step workflows
- **Modular Agents**: Each specialist agent can run independently or as part of the workflow

## Features

- ✅ **User Authentication** - JWT-based login/signup with encrypted API key storage
- ✅ **Real-time Agent Streaming** - Monitor agent execution with live event updates
- ✅ **Stateful Workflows** - Preserve conversation state across multiple agent invocations
- ✅ **Web Research Integration** - Tavily Search tool for gathering market data
- ✅ **Multiple Specialist Agents** - Modular agents for different analysis types
- ✅ **Database Persistence** - PostgreSQL with Alembic migrations
- ✅ **API Key Encryption** - Secure storage and decryption of OpenAI API keys
- ✅ **API Discovery** - Auto-generated endpoint directory

## Agents

The system includes three specialist agents that work together to analyze product launches:

### 1. Product Launch Analyst Agent
Provides critical, evidence-driven evaluation of competitor product launches.

**Responsibilities:**
- Analyzes market and product positioning
- Identifies launch strengths and weaknesses
- Provides strategic insights backed by sources

**Invoke Type:** `product_launch_analyst`

### 2. Market Sentiment Specialist Agent
Analyzes market sentiment and public perception around a product launch.

**Responsibilities:**
- Gauges market sentiment from various sources
- Identifies key opinion leaders and influencers
- Assesses social media and community reactions

**Invoke Type:** `market_sentiment_specialist`

### 3. Launch Metrics Specialist Agent
Evaluates quantitative metrics and performance indicators.

**Responsibilities:**
- Gathers launch performance metrics
- Analyzes user acquisition and engagement data
- Provides ROI and financial impact analysis

**Invoke Type:** `launch_metrics_specialist`

## API Reference

### User Management

#### POST `/api/users/signup`
Register a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure_password",
  "api_key_openai": "sk-..."
}
```

**Response (201):**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "api_key_openai": "encrypted_key",
  "message": "User created successfully"
}
```

#### POST `/api/users/login`
Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "name": "John Doe",
  "email": "john@example.com",
  "api_key_openai": "decrypted_key",
  "message": "User retrieved successfully"
}
```

### Agent Execution

#### POST `/api/agent_runs/run`
Execute an agent workflow with streaming responses.

**Request Body:**
```json
{
  "company_name": "TechCorp Inc",
  "agent_invoke": "product_launch_analyst",
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "api_key_openai": "sk-..."
}
```

**Streaming Response (Server-Sent Events):**
```
data: {"type": "thread_id", "thread_id": "550e8400-e29b-41d4-a716-446655440000"}

data: {"type": "node_start", "node": "product_launch_analyst"}

data: {"type": "tool_start", "tool": "tavily_search"}

data: {"type": "node_end", "node": "product_launch_analyst"}
```

#### GET `/api/agent_runs/get`
Retrieve the complete state of a workflow run.

**Query Parameters:**
- `thread_id` (required): UUID of the workflow run

**Response (200):**
```json
{
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "product_launch_analyst_agent_output": "...",
  "market_sentiment_specialist_agent_output": "...",
  "launch_metrics_specialist_agent_output": "..."
}
```

#### GET `/`
Get the auto-generated API endpoint directory.

**Response (200):**
```json
{
  "message": "API endpoint directory",
  "description": "Use the paths below to explore the available application routes.",
  "endpoints": [
    {
      "path": "/api/users/login",
      "methods": ["POST"],
      "summary": "Get User",
      "description": "Authenticate a user and return an access token..."
    }
  ]
}
```

## Setup & Installation

### Prerequisites

- **Python 3.11+**
- **PostgreSQL 12+**
- **uv** (Python package manager) - [Install uv](https://docs.astral.sh/uv/getting-started/)

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd ai-product-launch-intelligence-agent/backend
```

### Step 2: Install Dependencies with uv

```bash
uv sync
```

This command:
- Creates a virtual environment
- Installs all dependencies from `pyproject.toml`
- Installs development dependencies

### Step 3: Set Up Environment Variables

Create a `.env` file in the backend directory:

```bash
cp .env.example .env  # if template exists
# OR
nano .env  # create manually
```

## Environment Configuration

Configure the `.env` file with the following variables:

```env
# Database Configuration
DB_URL=postgresql://user:password@localhost:5432/launch_agent
DB_URL_API=postgresql://user:password@localhost:5432/launch_agent

# API Keys
TAVILY_API_KEY=your_tavily_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Security Keys
ACCESS_TOKEN_SECRET_KEY=your_jwt_secret_key_here
ENCRYPTION_MASTER_KEY=your_encryption_master_key_here

# Environment
ENV=development
DEBUG=False
```

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost/db` |
| `DB_URL_API` | PostgreSQL for API (usually same as DB_URL) | `postgresql://user:pass@localhost/db` |
| `TAVILY_API_KEY` | Tavily Search API key | `tvly-...` |
| `ACCESS_TOKEN_SECRET_KEY` | JWT secret key (use a strong random string) | Any strong random string |
| `ENCRYPTION_MASTER_KEY` | Master key for API key encryption | Any 32-character string |

### Generating Secure Keys

```bash
# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate encryption master key
python -c "import secrets; print(secrets.token_hex(16))"
```

## Running the Backend

### Development Mode with Auto-reload

```bash
uv run python main.py
```

Server starts at: `http://localhost:8000`

### Production Mode with uvicorn

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Run Database Migrations

```bash
# Create initial migration (if needed)
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head
```

### Check API Status

Visit `http://localhost:8000/` to see the auto-generated API endpoint directory.

Access Swagger UI documentation at: `http://localhost:8000/docs`

## API Usage Examples

### Complete Workflow Example

#### 1. User Signup

```bash
curl -X POST "http://localhost:8000/api/users/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "password": "securepass123",
    "api_key_openai": "sk-proj-..."
  }'
```

#### 2. User Login

```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "securepass123"
  }'
```

Response includes `access_token` and `api_key_openai`.

#### 3. Run Product Launch Analyst Agent (Streaming)

```bash
curl -X POST "http://localhost:8000/api/agent_runs/run" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "OpenAI",
    "agent_invoke": "product_launch_analyst",
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "api_key_openai": "sk-..."
  }' \
  --stream
```

#### 4. Run Another Agent on Same Thread

```bash
curl -X POST "http://localhost:8000/api/agent_runs/run" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "OpenAI",
    "agent_invoke": "market_sentiment_specialist",
    "thread_id": "550e8400-e29b-41d4-a716-446655440000",
    "api_key_openai": "sk-..."
  }' \
  --stream
```

Previous `product_launch_analyst_agent_output` is preserved in state.

#### 5. Retrieve Complete Analysis

```bash
curl -X GET "http://localhost:8000/api/agent_runs/get?thread_id=550e8400-e29b-41d4-a716-446655440000"
```

Response contains all three agent outputs.

### Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Login
login_response = requests.post(
    f"{BASE_URL}/api/users/login",
    json={"email": "alice@example.com", "password": "securepass123"}
)
token = login_response.json()["access_token"]
api_key = login_response.json()["api_key_openai"]

# Run agent with streaming
response = requests.post(
    f"{BASE_URL}/api/agent_runs/run",
    json={
        "company_name": "OpenAI",
        "agent_invoke": "product_launch_analyst",
        "thread_id": "550e8400-e29b-41d4-a716-446655440000",
        "api_key_openai": api_key
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        event = json.loads(line.decode())
        print(f"Event: {event['type']}")

# Get results
results = requests.get(
    f"{BASE_URL}/api/agent_runs/get?thread_id=550e8400-e29b-41d4-a716-446655440000"
)
print(json.dumps(results.json(), indent=2))
```

## Project Structure

```
backend/
├── main.py                    # FastAPI app entry point
├── config.py                  # Environment configuration
├── pyproject.toml            # Project dependencies
├── agent/                    # Agent workflow
│   ├── model/                # LLM initialization
│   ├── nodes/                # Specialist agent implementations
│   ├── state_schema/         # Agent state definitions
│   ├── tools/                # Tool integrations (Tavily)
│   └── workflow/             # StateGraph workflow builder
├── api/                      # API layer
│   ├── routers/              # Endpoint definitions
│   ├── schemas/              # Pydantic models
│   ├── services/             # Business logic
│   ├── models/               # SQLAlchemy models
│   ├── database/             # Database connection
│   └── access_tokens/        # JWT token management
└── alembic/                  # Database migrations
```

## Troubleshooting

### Database Connection Error
Ensure PostgreSQL is running and `.env` contains valid `DB_URL`.

### TAVILY_API_KEY Missing
Get your API key from [Tavily](https://tavily.com/) and add to `.env`.

### Agent Timeout
Increase tool call limits in agent node files or adjust timeout settings.

### State Not Persisting
Verify PostgreSQL checkpointer table exists: `alembic upgrade head`

---

**Happy analyzing!** 🚀

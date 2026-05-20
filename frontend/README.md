# AI Product Launch Intelligence Agent — Frontend

A developer-focused, production-ready Next.js frontend for the AI Product Launch Intelligence Agent. This README explains how the frontend is organized, how it communicates with the backend, how to run it locally, build for production, and how to contribute.

## Table of contents

- [AI Product Launch Intelligence Agent — Frontend](#ai-product-launch-intelligence-agent--frontend)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Quick start](#quick-start)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Run locally](#run-locally)
    - [Build for production](#build-for-production)
  - [Environment variables](#environment-variables)
  - [Architecture \& data flow](#architecture--data-flow)
  - [Folder structure](#folder-structure)
  - [API integration and proxy](#api-integration-and-proxy)
  - [Authentication flow](#authentication-flow)
  - [UI components and state management](#ui-components-and-state-management)
  - [Routing](#routing)
  - [Development workflow](#development-workflow)
  - [Deployment](#deployment)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License \& credits](#license--credits)

## Overview

This frontend is a Next.js app (App Router) that provides a web UI for running agent workflows, streaming responses, and visualizing analyses produced by the backend. It focuses on developer ergonomics (hooks, modular components) and streaming UX for long-running tasks.

## Features

- Run and manage AI agent executions.
- Streamed response rendering for real-time visibility.
- Authentication and session handling for API access.
- Reusable UI components and hooks for rapid feature development.
- Proxying server-side API calls to a configurable backend URL.

## Technologies

- Next.js (App Router)
- React 18+
- TypeScript
- Tailwind CSS (or plain CSS depending on project config)
- Vercel / Docker deployment targets

## Quick start

### Prerequisites

- Node.js 18 or newer
- npm (or yarn / pnpm)
- A running backend API (see repository root/backend) or reachable backend URL

### Installation

Clone the repository and install dependencies in the `frontend` folder:

```bash
cd frontend
npm install
```

### Run locally

Create a `.env.local` in the `frontend` folder (see Environment variables below), then:

```bash
npm run dev
# opens at http://localhost:3000 by default
```

The development server supports hot reload and server-side routes for proxying.

### Build for production

```bash
npm run build
npm run start
```

Or use Docker (example):

```bash
docker build -t ai-product-launch-frontend:latest .
docker run -p 3000:3000 -e BACKEND_API_URL="https://your-backend" ai-product-launch-frontend:latest
```

## Environment variables

Create `.env.local` in the `frontend` directory and set the variables below for development. For production, set these in your hosting platform (Vercel, Docker env, etc.).

Recommended variables:

```env
# Client-facing API url (used by frontend code)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Server-side proxy base URL (used by Next.js server routes)
BACKEND_API_URL=http://localhost:8000

# Optional: alternate public backend URL
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

- `NEXT_PUBLIC_API_URL` — used by client code when calling backend endpoints directly.
- `BACKEND_API_URL` — used by the server-side proxy (recommended to avoid exposing secrets and CORS issues).

## Architecture & data flow

1. The UI sends requests to either:
	 - the server-side proxy route at `/api/proxy/*`, which forwards requests to the configured backend (`BACKEND_API_URL`), or
	 - directly to `NEXT_PUBLIC_API_URL` for client-side calls where appropriate.
2. The backend handles authentication, agent orchestration, and data persistence. The frontend renders streaming responses and agent state updates.

This separation keeps backend credentials and CORS configuration on the server side while allowing the client to fetch public endpoints when needed.

## Folder structure

High-level overview of key folders and files:

- `app/` — Next.js App Router pages and server/route handlers (SSR and API proxy).
- `components/` — Reusable UI components (agent card, streaming response, sidebar, etc.).
- `hooks/` — Custom React hooks (auth, streaming, agent-run lifecycle hooks).
- `lib/` — API helpers, session management, storage utilities, and small client libraries.
- `public/` — Static assets (images, icons).
- `styles/` or `globals.css` — Global and utility styles.
- `package.json` — Frontend dependencies and scripts.

Example files to inspect when contributing:

- [app/page.tsx](app/page.tsx) — top-level page and routing entry
- [app/api/proxy/[...path]/route.ts](app/api/proxy/[...path]/route.ts) — proxy implementation
- [components/streaming-response.tsx](components/streaming-response.tsx) — stream UI renderer
- [hooks/use-agent-run.ts](hooks/use-agent-run.ts) — orchestrates agent execution from the UI

## API integration and proxy

The app includes a server-side proxy that forwards requests to the backend. This helps to:

- Avoid CORS issues in development and production
- Keep backend base URL and secrets server-side
- Centralize API error handling and request shaping

Typical use in client code:

```ts
// lib/api.ts (example)
export async function fetchAgentRuns() {
	return fetch('/api/proxy/agent/runs').then(r => r.json())
}
```

Server proxy route (located in `app/api/proxy/[...path]/route.ts`) reads `BACKEND_API_URL` and forwards the request path and query string.

## Authentication flow

This project supports token-based authentication with the backend. Typical flow:

1. User signs in via the UI which sends credentials to the backend auth endpoint.
2. Backend responds with a short-lived access token (JWT) and optionally a refresh token.
3. The frontend stores tokens in secure storage (preferably `httpOnly` cookies set by the backend; if client-stored, use `localStorage` as fallback with XSS caveats).
4. Client sends the access token in `Authorization: Bearer <token>` headers for protected API calls.
5. Refresh tokens are exchanged server-side (or via safe refresh route) to obtain new access tokens when needed.

Implementation notes:

- Prefer server-set `httpOnly` cookies to avoid exposing tokens to JavaScript.
- If using client-side storage, ensure the app defends against XSS and avoids storing sensitive long-lived tokens.

## UI components and state management

- `components/` contains small, focused components used across the app (cards, lists, streaming UI, etc.).
- `hooks/` contains reusable hooks for behavior (e.g., `useAgentRun`, `useAuth`, `useStreaming`).
- State is managed using a combination of React local state + lightweight global state via Context and custom hooks. Persisted session/credentials are handled via `lib/session.ts`.

Patterns used:

- Keep components presentational and move data fetching into hooks or server components.
- Streaming responses are buffered and rendered progressively using `ReadableStream` or SSE depending on backend support.

## Routing

This project uses Next.js App Router. Key points:

- Pages and layouts live under `app/`.
- Client components are marked with `'use client'` at the top of the file.
- Server components (default) are used for initial data fetching where possible.

## Development workflow

- Run the dev server: `npm run dev`
- Format and lint: `npm run lint` or `npm run format` (if configured)
- Build: `npm run build` and `npm run start` for production verification

Recommended contributor steps:

1. Open a feature branch.
2. Run `npm install` and `npm run dev`.
3. Add or update components and hooks, keeping changes small and focused.
4. Run `npm run build` locally before opening a PR.

## Deployment

Vercel (recommended for Next.js app router):

1. Connect the repository to Vercel.
2. Add `BACKEND_API_URL` and `NEXT_PUBLIC_API_URL` to project environment variables.
3. Deploy the `main` branch.

Docker

Build image and run (example):

```bash
docker build -t ai-product-launch-frontend:latest .
docker run -p 3000:3000 -e BACKEND_API_URL="https://your-backend" ai-product-launch-frontend:latest
```

Hugging Face Space

- If deploying as a static/dynamic demo on Hugging Face, ensure the backend URL is reachable and set in the space settings.

## Troubleshooting

- Backend unreachable: verify `BACKEND_API_URL` and that the backend is running.
- CORS errors: ensure server proxy is used for protected endpoints or backend allows the origin.
- Auth failures: check token storage strategy (cookies vs localStorage) and inspect requests in DevTools.
- Build failures: run `npm run build` locally and inspect the error stack; ensure Node version >= 18.

If you hit an unexpected error, open an issue with logs and reproduction steps.

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repo and create a feature branch.
2. Run the app locally and add tests for new features where applicable.
3. Open a PR describing your changes and why they help the project.

## License & credits

See the repository root for license information and contributor credits.

---

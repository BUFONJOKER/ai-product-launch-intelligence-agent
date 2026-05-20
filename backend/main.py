import os

from fastapi import FastAPI
from fastapi.routing import APIRoute
from api.routers.user_routes import user_router
from api.routers.agent_run_routes import agent_run_router
import uvicorn
from config import DEBUG
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=DEBUG)

# Production Security: Read allowed origins from an environment variable,
# defaulting to localhost for local development.
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(agent_run_router)


@app.get("/")
def root():
    """Return a compact directory of the API endpoints registered in the app."""
    endpoints = []

    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue

        if route.path == "/":
            continue

        description = route.description or (route.endpoint.__doc__ or "").strip()

        endpoints.append(
            {
                "path": route.path,
                "methods": sorted(route.methods or []),
                "summary": route.summary or route.name.replace("_", " ").title(),
                "description": description or "No description available.",
            }
        )

    endpoints.sort(key=lambda item: item["path"])

    return {
        "message": "API endpoint directory",
        "description": "Use the paths below to explore the available application routes.",
        "endpoints": endpoints,
    }


if __name__ == "__main__":
    # CRITICAL FIX: Must default to "0.0.0.0" in container environments
    # to let Hugging Face pass incoming traffic through.
    host = os.getenv("HOST", "0.0.0.0")

    # Hugging Face will automatically inject PORT=7860 into your environment variables,
    # falling back to 8000 locally.
    port = int(os.getenv("PORT", "8000"))

    # Production Notice: Turn reload off in production for better performance
    is_debug = os.getenv("ENVIRONMENT", "development").lower() == "development"

    uvicorn.run("main:app", host=host, port=port, reload=is_debug)
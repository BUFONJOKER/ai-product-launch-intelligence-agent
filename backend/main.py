from fastapi import FastAPI
from fastapi.routing import APIRoute
from api.routers.user_routes import user_router
from api.routers.agent_run_routes import agent_run_router
import uvicorn
from config import DEBUG

app = FastAPI(debug=DEBUG)

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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

import os
from fastapi import FastAPI
from api.routers.user_routes import user_router
from api.routers.agent_run_routes import agent_run_router
import uvicorn
from config import DEBUG


app = FastAPI(debug=DEBUG)

app.include_router(user_router)
app.include_router(agent_run_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

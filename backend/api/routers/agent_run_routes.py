from typing import List
from api.services.agent_services import run_agent_service, get_agent_response_service
from api.schemas.agent_data import AgentRun, AgentResponse
from api.database.db_connection import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

agent_run_router = APIRouter(
    prefix="/api/agent_runs",
    tags=["agent-runs"]
)



@agent_run_router.get("/agent_response")
def get_agent_response(agent_response:AgentResponse):
    agent_response = get_agent_response_service(agent_response)
    if agent_response is None:
        raise HTTPException(status_code=404, detail="Agent response not found")
    return agent_response

@agent_run_router.post("/start_agent", response_model=AgentResponse, status_code=201)
def create_agent_run(agent_run: AgentRun):
    return run_agent_service(agent_run)

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import uuid
import json

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection

from agent.workflow.build_workflow import build_workflow
from agent.model.initialize_model import load_model
from agent.state_schema.agent_state import AgentState
from api.schemas.agent_data import AgentRun

from config import DB_URL

agent_run_router = APIRouter(prefix="/api/agent_runs", tags=["agent-runs"])


async def stream_agent(agent_run: AgentRun):

    thread_id = agent_run.thread_id or str(uuid.uuid4())

    yield f"data: {json.dumps({'type': 'thread_id', 'thread_id': thread_id})}\n\n"

    config = {"configurable": {"thread_id": thread_id}}

    initial_state = AgentState(
        company_name=agent_run.company_name, agent_invoke=agent_run.agent_invoke
    )

    async with await AsyncConnection.connect(
        DB_URL, autocommit=True, prepare_threshold=None
    ) as conn:

        checkpointer = AsyncPostgresSaver(conn)

        await checkpointer.setup()

        model = load_model()

        workflow = build_workflow(model=model, checkpointer=checkpointer)

        async for event in workflow.astream_events(
            initial_state, config=config, version="v2"
        ):

            event_type = event["event"]

            # NODE START
            if event_type == "on_chain_start":

                payload = {
                    "type": "node_start",
                    "node": event.get("name")
                }

                yield f"data: {json.dumps(payload)}\n\n"

            # NODE END
            elif event_type == "on_chain_end":

                payload = {
                    "type": "node_end",
                    "node": event.get("name")
                }

                yield f"data: {json.dumps(payload)}\n\n"

            # TOOL START
            elif event_type == "on_tool_start":

                payload = {
                    "type": "tool_start",
                    "tool": event.get("name")
                }

                yield f"data: {json.dumps(payload)}\n\n"

            # TOOL END
            elif event_type == "on_tool_end":

                payload = {
                    "type": "tool_end",
                    "tool": event.get("name")
                }

                yield f"data: {json.dumps(payload)}\n\n"


@agent_run_router.post("/start_agent")
async def start_agent(agent_run: AgentRun):

    return StreamingResponse(stream_agent(agent_run), media_type="text/event-stream")



async def get_final_response(thread_id: str):
    """Retrieve the latest saved workflow state values for a thread.

    This function connects to the configured checkpointer, reloads the
    model and workflow, then fetches the persisted state associated with
    `thread_id`.

    Args:
        thread_id (str): UUID string that identifies the agent run.

    Returns:
        dict: The stored state values for the thread, typically containing
            outputs from the specialist agents (e.g. keys like
            `product_launch_analyst_agent_output`).
    """

    config = {"configurable": {"thread_id": thread_id}}

    async with await AsyncConnection.connect(
        DB_URL, autocommit=True, prepare_threshold=None
    ) as conn:

        checkpointer = AsyncPostgresSaver(conn)

        model = load_model()

        workflow = build_workflow(model=model, checkpointer=checkpointer)

        state = await workflow.aget_state(config)

        return state.values

@agent_run_router.get("/get_agent_response/{thread_id}")
async def get_agent_response(thread_id: str):

    result = await get_final_response(thread_id)

    return {
        "thread_id": thread_id,
        "launch_metrics_specialist_agent_output": result.get("launch_metrics_specialist_agent_output"),
        "market_sentiment_specialist_agent_output": result.get("market_sentiment_specialist_agent_output"),
        "product_launch_analyst_agent_output": result.get("product_launch_analyst_agent_output"),
    }

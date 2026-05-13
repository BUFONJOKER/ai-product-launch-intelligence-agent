from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import uuid
import json

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection

from agent.workflow.build_workflow import build_workflow
from agent.model.initialize_model import load_model
from agent.state_schema.agent_state import AgentState
from api.schemas.agent_data import AgentRunRequest, GetAgentRequest, GetAgentResponse
from api.api_key_encryption.encrypt_decrypt import decrypt_key
from config import DB_URL

agent_run_router = APIRouter(prefix="/api/agent_runs", tags=["agent-runs"])


async def stream_agent(request: AgentRunRequest, api_key_openai):

    thread_id = request.thread_id or str(uuid.uuid4())

    yield f"{json.dumps({'type': 'thread_id', 'thread_id': thread_id})}\n\n"

    config = {
        "configurable": {"thread_id": thread_id},
        "run_name": f"{request.company_name}_agent_run_{thread_id}",
    }

    async with await AsyncConnection.connect(
        DB_URL, autocommit=True, prepare_threshold=None
    ) as conn:

        checkpointer = AsyncPostgresSaver(conn)

        # await checkpointer.setup()

        model = load_model(api_key_openai)

        workflow = build_workflow(model=model, checkpointer=checkpointer)

        # Preserve previously generated specialist outputs for this thread,
        # then run only the requested specialist for the current invocation.
        previous_state = await workflow.aget_state(config)
        previous_values = previous_state.values if previous_state else {}

        initial_state = AgentState(
            company_name=request.company_name,
            agent_invoke=request.agent_invoke,
            launch_metrics_specialist_agent_output=previous_values.get(
                "launch_metrics_specialist_agent_output", ""
            ),
            market_sentiment_specialist_agent_output=previous_values.get(
                "market_sentiment_specialist_agent_output", ""
            ),
            product_launch_analyst_agent_output=previous_values.get(
                "product_launch_analyst_agent_output", ""
            ),
        )

        async for event in workflow.astream_events(
            initial_state, config=config, version="v2"
        ):

            event_type = event["event"]

            # NODE START
            if event_type == "on_chain_start":

                payload = {"type": "node_start", "node": event.get("name")}

                yield f"{json.dumps(payload)}\n\n"

            # NODE END
            elif event_type == "on_chain_end":

                payload = {"type": "node_end", "node": event.get("name")}

                yield f"{json.dumps(payload)}\n\n"

            # TOOL START
            elif event_type == "on_tool_start":

                payload = {"type": "tool_start", "tool": event.get("name")}

                yield f"{json.dumps(payload)}\n\n"

            # TOOL END
            elif event_type == "on_tool_end":

                payload = {"type": "tool_end", "tool": event.get("name")}

                yield f"{json.dumps(payload)}\n\n"


@agent_run_router.post("/start_agent")
async def start_agent(request: AgentRunRequest):
    api_key_openai = request.api_key_openai
    api_key_openai = decrypt_key(api_key_openai)
    return StreamingResponse(
        stream_agent(request, api_key_openai), media_type="text/event-stream"
    )


async def get_final_response(thread_id: str, api_key_openai: str):
    """Retrieve the latest saved workflow state values for a thread.

    This function connects to the configured checkpointer, reloads the
    model and workflow, then fetches the persisted state associated with
    `thread_id`.

    Args:
        thread_id (str): UUID string that identifies the agent run.
        api_key_openai (str): The user's OpenAI API key (will be encrypted before storage).

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

        model = load_model(api_key_openai)

        workflow = build_workflow(model=model, checkpointer=checkpointer)

        state = await workflow.aget_state(config)

        return state.values


@agent_run_router.post("/get_agent_response", response_model=GetAgentResponse)
async def get_agent_response(request: GetAgentRequest):
    api_key_openai = decrypt_key(request.api_key_openai)
    result = await get_final_response(request.thread_id, api_key_openai)

    return {
        "thread_id": request.thread_id,
        "launch_metrics_specialist_agent_output": result.get(
            "launch_metrics_specialist_agent_output"
        ),
        "market_sentiment_specialist_agent_output": result.get(
            "market_sentiment_specialist_agent_output"
        ),
        "product_launch_analyst_agent_output": result.get(
            "product_launch_analyst_agent_output"
        ),
    }

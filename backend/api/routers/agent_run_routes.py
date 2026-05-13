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
    """Stream agent workflow events in real-time as server-sent events.

    This function executes the agent workflow asynchronously and yields events
    as JSON-formatted server-sent events (SSE). It preserves previously generated
    specialist outputs from prior runs on the same thread, then executes only the
    requested specialist agent for the current invocation. Events include thread
    initialization, node start/end, and tool start/end notifications.

    Args:
        request (AgentRunRequest): The agent execution request containing company name,
            agent invoke type, thread ID, and encrypted API key.
        api_key_openai (str): The decrypted OpenAI API key for LLM operations.

    Yields:
        str: JSON-formatted server-sent event strings, each newline-terminated.
            Event types include:
            - 'thread_id': Initial thread identifier for the run
            - 'node_start'/'node_end': Workflow node lifecycle events
            - 'tool_start'/'tool_end': Tool invocation lifecycle events
    """

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
    """HTTP endpoint to initiate an agent workflow run with server-sent event streaming.

    This endpoint accepts a request to start an agent run, decrypts the provided
    OpenAI API key, and returns a streaming response that yields real-time events
    as the workflow executes. The response is formatted as server-sent events (SSE)
    for easy consumption by frontend clients.

    Args:
        request (AgentRunRequest): The agent execution request including company name,
            agent invoke type, thread ID, and encrypted API key.

    Returns:
        StreamingResponse: An HTTP response that streams events with media type
            'text/event-stream'. Each event is a JSON object followed by two newlines.
    """
    api_key_openai = request.api_key_openai
    api_key_openai = decrypt_key(api_key_openai)
    return StreamingResponse(
        stream_agent(request, api_key_openai), media_type="text/event-stream"
    )


async def get_final_response(thread_id: str, api_key_openai: str):
    """Retrieve the latest saved workflow state values for a thread.

    This function connects to the configured PostgreSQL checkpointer, reinitializes
    the LLM model and workflow graph, then fetches the persisted AgentState
    associated with the given thread_id. It returns the complete state values
    dictionary containing all specialist agent outputs and metadata from the run.

    Args:
        thread_id (str): UUID string that uniquely identifies the agent workflow run.
        api_key_openai (str): The user's decrypted OpenAI API key for model initialization.

    Returns:
        dict: The stored AgentState values for the thread, containing keys such as:
            - launch_metrics_specialist_agent_output (str)
            - market_sentiment_specialist_agent_output (str)
            - product_launch_analyst_agent_output (str)
            - company_name (str)
            - agent_invoke (str)
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
    """HTTP endpoint to retrieve the final agent response for a completed run.

    This endpoint accepts a request with a thread ID and encrypted API key, retrieves
    the persisted workflow state from the database, decrypts the API key, and returns
    the specialist agent outputs in a structured response. It serves as the primary
    method for clients to fetch the results of an agent workflow execution.

    Args:
        request (GetAgentRequest): The request containing thread_id (UUID string)
            and encrypted api_key_openai.

    Returns:
        GetAgentResponse: A structured response containing:
            - thread_id (str): The workflow run identifier
            - launch_metrics_specialist_agent_output (str): Metrics analysis output
            - market_sentiment_specialist_agent_output (str): Market sentiment analysis output
            - product_launch_analyst_agent_output (str): Product launch analysis output
    """
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

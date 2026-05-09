import asyncio

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agent.workflow.build_workflow import build_workflow
from agent.model.initialize_model import load_model
from agent.state_schema.agent_state import AgentState

from config import DB_URL
from psycopg import AsyncConnection


async def run_agent(company_name: str, agent_invoke: str,thread_id: str):
    """Run the AI product-launch agent workflow asynchronously.

    This function prepares an initial agent state, initializes persistence
    and model resources, compiles the workflow, invokes it, and returns
    the workflow response along with a unique `thread_id` for tracking.

    Args:
        company_name (str): The name of the company to analyze.
        agent_invoke (str): Identifier of which specialist agent to run
            (e.g., "product_launch_analyst", "market_sentiment_specialist",
            "launch_metrics_specialist").

    Returns:
        dict: A dictionary containing:
            - `thread_id` (str): UUID string for this run.
            - `response`: The raw response from the invoked workflow.
            - `agent_run_status` (str): Short status message.
    """


    config = {"configurable": {"thread_id": thread_id}}

    initial_state = AgentState(company_name=company_name, agent_invoke=agent_invoke)

    async with await AsyncConnection.connect(
        DB_URL, autocommit=True, prepare_threshold=None
    ) as conn:

        checkpointer = AsyncPostgresSaver(conn)

        await checkpointer.setup()

        model = load_model()

        workflow = build_workflow(model=model, checkpointer=checkpointer)

        response = await workflow.ainvoke(initial_state, config=config)

        return {
            "thread_id": thread_id,
            "response": response,
            "agent_run_status": "agent run completed successfully",
        }


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


if __name__ == "__main__":

    # IMPORTANT FOR WINDOWS + PSYCOPG ASYNC
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # company_name = "Apple Vision Pro"

    # agent_options = [
    #     "product_launch_analyst",
    #     "market_sentiment_specialist",
    #     "launch_metrics_specialist",
    # ]

    # asyncio.run(run_agent(company_name=company_name, agent_invoke=agent_options[0]))

    result = asyncio.run(
        get_final_response(thread_id="728f54fe-0915-4db2-a560-be465b24695f")
    )

    print(result["product_launch_analyst_agent_output"])
    print("------------------------------")
    print(result["launch_metrics_specialist_agent_output"])
    print("------------------------------")
    print(result["market_sentiment_specialist_agent_output"])

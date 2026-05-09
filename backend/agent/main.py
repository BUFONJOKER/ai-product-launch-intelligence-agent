import asyncio
import uuid

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agent.workflow.build_workflow import build_workflow
from agent.model.initialize_model import load_model
from agent.state_schema.agent_state import AgentState

from config import DB_URL


async def run_agent(company_name:str, agent_invoke:str):

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = AgentState(
        company_name=company_name,
        agent_invoke=agent_invoke
    )

    async with AsyncPostgresSaver.from_conn_string(DB_URL) as checkpointer:

        await checkpointer.setup()

        model = load_model()

        workflow = build_workflow(
            model=model,
            checkpointer=checkpointer
        )

        response = await workflow.ainvoke(
            initial_state,
            config=config
        )

        print(response)

    return response


if __name__ == "__main__":

    # IMPORTANT FOR WINDOWS + PSYCOPG ASYNC
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

    company_name = "Apple Vision Pro"

    agent_options = [
        "product_launch_analyst",
        "market_sentiment_specialist",
        "launch_metrics_specialist",
    ]

    asyncio.run(run_agent(company_name=company_name, agent_invoke=agent_options[0]))
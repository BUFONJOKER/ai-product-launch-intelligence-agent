from agent.main import run_agent, get_final_response


async def run_agent_service(company_name: str, agent_invoke: str, thread_id: str):
    """Service function to run the agent workflow.

    This function serves as the main entry point for executing the agent
    workflow. It accepts parameters that specify the company to analyze,
    which specialist agent to invoke, and a thread ID for tracking the run.

    Args:
        company_name (str): The name of the company to analyze.
        agent_invoke (str): Identifier of which specialist agent to run
        thread_id (str): The UUID string for tracking the agent run.
    
    Returns:
        dict: A dictionary containing the thread ID, the response from the
            agent workflow, and a status message.
    """


    agent_run_result = await run_agent(company_name, agent_invoke, thread_id)

    # Optionally, you can also fetch the final response using the thread_id
    # final_response = await get_agent_response(thread_id)

    if agent_run_result is None:
        return {
            "thread_id": thread_id,
            "response": None,
            "agent_run_status": "agent run failed or returned no result",
        }

    else:
        return {
            "thread_id": thread_id,
            "response": agent_run_result["response"],
            "agent_run_status": agent_run_result["agent_run_status"],
        }

async def get_agent_response_service(thread_id: str):
    """Service function to retrieve the final response of an agent run.

    This function can be used to fetch the final output of an agent workflow
    execution using the unique thread ID associated with that run.

    Args:
        thread_id (str): The UUID string for the agent run to retrieve the
            response for.

    Returns:
        dict: A dictionary containing the thread ID and the final response from
            the agent workflow, or an error message if retrieval fails.
    """

    final_response = await get_final_response(thread_id)

    if final_response is None:
        return {
            "thread_id": thread_id,
            "response": None,
            "status": "failed to retrieve agent response or no response found",
        }

    else:

        return {
            "thread_id": thread_id,
            "response": final_response,
            "status": "agent response retrieved successfully",
            "launch_metrics_specialist_agent_output": final_response.get("launch_metrics_specialist_agent_output"),
            "market_sentiment_specialist_agent_output": final_response.get("market_sentiment_specialist_agent_output"),
            "product_launch_analyst_agent_output": final_response.get("product_launch_analyst_agent_output"),
        }
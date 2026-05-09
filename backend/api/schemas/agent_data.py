from pydantic import BaseModel, Field
from typing import Literal, Any


class AgentResponse(BaseModel):
    """State container passed between nodes in the agent workflow.

    Args:
        company_name (str): Name of the company being analyzed.
        agent_invoke (str): Identifier for which specialist agent to run.
        launch_metrics_specialist_agent_output (str): Output text from the
            launch metrics specialist agent.
        market_sentiment_specialist_agent_output (str): Output text from the
            market sentiment specialist agent.
        product_launch_analyst_agent_output (str): Output text from the
            product launch analyst agent.

    Returns:
        AgentState: A validated Pydantic model instance representing the
            current workflow state.
    """

    thread_id: str = Field(description="UUID string for this run")

    response: Any = Field(description="The raw response from the invoked workflow")
    status: str = Field(default="agent response retrieved successfully")
    launch_metrics_specialist_agent_output: Any = Field(description="Output from the launch metrics specialist agent")
    market_sentiment_specialist_agent_output: Any = Field(description="Output from the market sentiment specialist agent")
    product_launch_analyst_agent_output: Any = Field(description="Output from the product launch analyst agent")

class AgentRunResponse(BaseModel):
    """State container passed between nodes in the agent workflow.

    Args:
        company_name (str): Name of the company being analyzed.
        agent_invoke (str): Identifier for which specialist agent to run.
        launch_metrics_specialist_agent_output (str): Output text from the
            launch metrics specialist agent.
        market_sentiment_specialist_agent_output (str): Output text from the
            market sentiment specialist agent.
        product_launch_analyst_agent_output (str): Output text from the
            product launch analyst agent.

    Returns:
        AgentState: A validated Pydantic model instance representing the
            current workflow state.
    """

    thread_id: str = Field(description="UUID string for this run")

    response: Any = Field(description="The raw response from the invoked workflow")

    agent_run_status: str = Field(description="Short status message about the agent run")



class AgentRun(BaseModel):
    """State container passed between nodes in the agent workflow.

    Args:
        company_name (str): Name of the company being analyzed.
        agent_invoke (str): Identifier for which specialist agent to run.
        launch_metrics_specialist_agent_output (str): Output text from the
            launch metrics specialist agent.
        market_sentiment_specialist_agent_output (str): Output text from the
            market sentiment specialist agent.
        product_launch_analyst_agent_output (str): Output text from the
            product launch analyst agent.

    Returns:
        AgentState: A validated Pydantic model instance representing the
            current workflow state.
    """
    thread_id: str = Field(description="UUID string for this run")
    company_name: str = Field(description="Name of the company being analyzed")
    agent_invoke: Literal[
        "product_launch_analyst",
        "market_sentiment_specialist",
        "launch_metrics_specialist",
    ] = Field(
        description="Identifier of which specialist agent to run (e.g., 'product_launch_analyst', 'market_sentiment_specialist', 'launch_metrics_specialist')"
    )

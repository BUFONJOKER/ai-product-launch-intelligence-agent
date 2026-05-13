from pydantic import BaseModel, Field
from typing import Literal, Any


class AgentRunRequest(BaseModel):
    """Input payload used to start or route an agent workflow run.

    Attributes:
        thread_id: UUID string that identifies the workflow run.
        api_key_openai: The user's OpenAI API key, which is encrypted before storage.
        company_name: The company name that will be analyzed by the workflow.
        agent_invoke: The specialist agent that should handle this request.
    """

    thread_id: str = Field(description="UUID string that identifies this workflow run")
    api_key_openai: str = Field(
        description="The user's OpenAI API key, encrypted before storage"
    )
    company_name: str = Field(description="The company name being analyzed")
    agent_invoke: Literal[
        "product_launch_analyst",
        "market_sentiment_specialist",
        "launch_metrics_specialist",
    ] = Field(description="Identifier of the specialist agent to run")


class GetAgentResponse(BaseModel):
    """Aggregated workflow outputs returned to the caller.

    Attributes:
        thread_id: UUID string that identifies the workflow run.
        launch_metrics_specialist_agent_output: Output produced by the launch metrics specialist agent.
        market_sentiment_specialist_agent_output: Output produced by the market sentiment specialist agent.
        product_launch_analyst_agent_output: Output produced by the product launch analyst agent.
    """

    thread_id: str = Field(description="UUID string that identifies this workflow run")
    launch_metrics_specialist_agent_output: Any = Field(
        description="Output produced by the launch metrics specialist agent"
    )
    market_sentiment_specialist_agent_output: Any = Field(
        description="Output produced by the market sentiment specialist agent"
    )
    product_launch_analyst_agent_output: Any = Field(
        description="Output produced by the product launch analyst agent"
    )


class GetAgentRequest(BaseModel):
    """Request payload used to fetch the current agent workflow state.

    Attributes:
        thread_id: UUID string that identifies the workflow run.
        api_key_openai: The user's OpenAI API key, which is encrypted before storage.
    """

    thread_id: str = Field(description="UUID string that identifies this workflow run")
    api_key_openai: str = Field(
        description="The user's OpenAI API key, encrypted before storage"
    )

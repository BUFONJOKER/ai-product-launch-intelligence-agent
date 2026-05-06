from pydantic import BaseModel, Field

class AgentState(BaseModel):
    """State schema for the agent workflow."""
    company_name: str = Field(description="Name of the company being analyzed")

    agent_invoke: str = Field(description="Identifier for which agent to invoke")

    launch_metrics_specialist_agent_output: str = Field(default="", description="Output from the Launch Metrics Specialist Agent")

    market_sentiment_specialist_agent_output: str = Field(default="", description="Output from the Market Sentiment Specialist Agent")

    product_launch_analyst_agent_output: str = Field(default="", description="Output from the Product Launch Analyst Agent")
from pydantic import BaseModel

class AgentState(BaseModel):
    """State schema for the agent workflow."""
    user_input: str
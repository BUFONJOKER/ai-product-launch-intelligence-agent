from agent.state_schema.agent_state import AgentState
from langchain.agents import create_agent
from agent.tools.tavily_search import web_search_tool
from langchain.agents.middleware import ToolCallLimitMiddleware


def ProductLaunchAnalystAgent(model, state: AgentState):
    """Run a product launch analysis using a provided language model.

    This function constructs a specialized system prompt, attaches a
    web-search tool, creates a LangChain agent, and invokes it to analyze
    the product launch for `state.company_name`.

    Args:
        model: A language model instance compatible with LangChain agents
            (for example, a `ChatOpenAI` instance returned by
            `load_model`).
        state (AgentState): The agent state object containing input
            values such as `company_name` and `agent_invoke`.

    Returns:
        dict: A dictionary with a single key
            `'product_launch_analyst_agent_output'` containing the
            agent's textual analysis output.
    """
    company_name = state.company_name

    system_prompt = """
    You are a senior Go-To-Market (GTM) strategist specializing in competitive intelligence. Your task is to provide a critical, evidence-driven evaluation of competitor product launches.

    ### EXECUTION GUIDELINES:
    1. **Tone**: Crisp, professional, and executive-focused.
    2. **Evidence**: Every claim must be backed by observable signals (e.g., specific messaging, pricing changes, channel selection, or engagement data).
    3. **Constraints**: Adhere strictly to the point counts and structures below.

    ### OUTPUT STRUCTURE:

    ## 1. Market and Product Positioning
    Provide exactly 5 bullet points analyzing how the product is framed within the current market landscape and its value proposition.

    ## 2. Launch Strengths
    Provide a Markdown table with two columns: **Strength** and **Evidence / Rationale**.
    Include exactly 5 rows of distinct successful tactics.

    ## 3. Launch Weaknesses
    Provide a Markdown table with two columns: **Weakness** and **Evidence / Rationale**.
    Include exactly 5 rows of execution gaps or strategic shortcomings.

    ## 4. Sources
    List the URLs of all websites, articles, or documentation crawled or searched during this analysis as a bulleted list. Each bullet must follow the format: [Title of Page](URL).

    IMPORTANT: Use only verifiable data. If a specific metric is unavailable, focus on qualitative signals like "increased frequency of social mentions" or "ad spend shift."
    """

    # Get the web search tool
    search_tool = web_search_tool()

    # Create agent with the tool
    agent = create_agent(
        model,
        tools=[search_tool],
        system_prompt=system_prompt,
        middleware=[
            # Global limit
            ToolCallLimitMiddleware(thread_limit=5, run_limit=3)
        ],
    )

    # Invoke the agent
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze the product launch of {company_name} and provide insights on its market positioning, strengths, weaknesses, and actionable learnings for competitors.",
                }
            ]
        }
    )

    # Extract the final response
    final_response = result["messages"][-1].content

    return {"product_launch_analyst_agent_output": final_response}
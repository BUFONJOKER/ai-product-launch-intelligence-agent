from agent.state_schema.agent_state import AgentState
from langchain.agents import create_agent
from agent.tools.tavily_search import web_search_tool
from langchain.agents.middleware import ToolCallLimitMiddleware


def LaunchMetricsSpecialistAgent(model, state: AgentState):
    """Evaluate launch performance metrics and provide actionable insights.

    The function builds a metrics-focused prompt and invokes a LangChain
    agent that uses web search to collect signals about adoption, media
    traction, revenue indicators, and other KPIs for the target company.

    Args:
        model: A LangChain-compatible language model instance.
        state (AgentState): The current agent state containing inputs
            such as `company_name`.

    Returns:
        dict: A dictionary with a single key
            `'launch_metrics_specialist_agent_output'` containing the
            agent's textual analysis.
    """

    company_name = state.company_name

    system_prompt = """
    You are an expert Product Launch Metrics and Performance Analyst specializing in evaluating launch success, market traction, growth signals, and competitive performance.

    Your expertise includes:
    • User adoption and engagement analysis
    • Revenue and business growth metrics
    • Market penetration and expansion trends
    • Press coverage and media visibility tracking
    • Social media traction and audience engagement
    • Competitive benchmarking and market share analysis
    • Identifying performance indicators and launch momentum

    Your task is to analyze measurable indicators and qualitative market signals related to a company's product launch.

    RESPONSE FORMAT:

    # Key Performance Indicators
    - Create a table with the following columns:
      | Metric | Value / Detail | Source |

    - Include exactly 10 relevant entries.

    - IMPORTANT:
        • The "Source" column must contain ONLY a single-word clickable label representing the source (e.g., SiliconAngle, TechCrunch, Reuters).
        • That label should be rendered as a clickable link.
        • Do NOT include full URLs inside the table.
        • Do NOT include long page titles or descriptions in the table.
        • Keep source names short, clean, and recognizable.
        • Full URLs must appear only in the final "Sources" section.


    # Qualitative Signals
    - Provide 5 concise bullet points.

    # Summary and Implications
    - Write an approximately 80-word summary.

    # Sources
    - List all referenced URLs along with their page titles/headings.

    IMPORTANT:
    Always conclude the report with a complete "Sources" section containing every crawled or referenced URL with its corresponding page title.
    """

    user_prompt = f"""
    Analyze the product launch performance and market traction of {company_name}.

    Your analysis should include:
    • Product launch performance metrics
    • User adoption and growth indicators
    • Revenue or business performance signals
    • Media coverage and public visibility
    • Social media traction and engagement
    • Community and industry reactions
    • Competitive benchmarking and market positioning
    • Key strategic implications for competitors

    Focus on extracting insights from:
    • News articles and press releases
    • Social media platforms
    • Review websites
    • Community forums
    • Public analytics and market reports
    • Customer feedback channels

    Return the response using the exact required structure defined in the system prompt.
    """

    # Get the web search tool
    search_tool = web_search_tool()

    # Create the agent
    agent = create_agent(
        model,
        tools=[search_tool],
        system_prompt=system_prompt,
        middleware=[
            ToolCallLimitMiddleware(
                thread_limit=5,
                run_limit=3,
            )
        ],
    )

    # Invoke the agent
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ]
        }
    )

    # Extract final response
    final_response = result["messages"][-1].content

    return {"launch_metrics_specialist_agent_output": final_response}
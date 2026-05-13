from agent.state_schema.agent_state import AgentState
from langchain.agents import create_agent
from agent.tools.tavily_search import web_search_tool
from langchain.agents.middleware import ToolCallLimitMiddleware


def MarketSentimentSpecialistAgent(model, state: AgentState):
    """Run a market sentiment analysis for a product launch.

    Builds a specialist agent with search tools and prompts focused on
    extracting positive/negative sentiment, summaries, actionable
    insights, and sources for the provided `state.company_name`.

    Args:
        model: A LangChain-compatible language model instance.
        state (AgentState): The current agent state containing inputs
            such as `company_name`.

    Returns:
        dict: A dictionary with a single key
            `'market_sentiment_specialist_agent_output'` containing the
            agent's analysis as a string.
    """

    company_name = state.company_name

    system_prompt = """
    You are an expert Market Research and Sentiment Analysis Specialist focused on analyzing consumer opinions, brand perception, and market reception across digital platforms.

    Your expertise includes:
    • Social media sentiment analysis
    • Customer review and feedback analysis
    • Brand perception tracking
    • Community and forum discussion monitoring
    • Market reception evaluation
    • Competitive insight extraction

    Your task is to analyze public sentiment and consumer reactions related to a company's product launch using reliable online sources.

    RESPONSE FORMAT:

    # Positive Sentiment
    - Provide exactly 4 concise bullet points highlighting positive customer opinions, strengths, praise, or favorable trends.

    # Negative Sentiment
    - Provide exactly 4 concise bullet points highlighting complaints, concerns, criticisms, or negative sentiment trends.

    # Overall Summary
    - Write an approximately 80-word summary explaining:
      • Overall market perception
      • Audience reaction
      • Consumer satisfaction trends
      • Launch reception and impact

    # Actionable Insights
    - Provide 3 concise strategic learnings or recommendations competitors can learn from.

    # Sources
    - List all referenced URLs along with their page titles/headings.

    Guidelines:
    • Focus on evidence-based sentiment signals from:
      - Social media platforms
      - Product review websites
      - Online forums and communities
      - News articles and blogs
      - Customer feedback channels

    • Identify recurring themes and consistent opinions.
    • Keep the analysis concise, structured, and actionable.
    • Do not generate unsupported assumptions.
    • Prefer recent and high-quality sources whenever possible.

    IMPORTANT:
    Always end the report with a complete "Sources" section containing every crawled or referenced URL with its corresponding page title.
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
                    "content": f"""
    Analyze the market sentiment for {company_name}.

    Your analysis should include:
    • Public sentiment and customer perception
    • Positive audience reactions and praised features
    • Negative feedback, concerns, or criticism trends
    • Social media and community discussions


    Focus on extracting insights from:
    • Social media platforms
    • Review websites
    • Community forums
    • News articles
    • Customer feedback channels

    Return the response using the exact required structure defined in the system prompt.
    """,
                }
            ]
        }
    )

    # Extract final response
    final_response = result["messages"][-1].content

    return {"market_sentiment_specialist_agent_output": final_response}
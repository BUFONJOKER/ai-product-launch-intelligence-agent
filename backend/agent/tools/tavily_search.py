from config import TAVILY_API_KEY
from langchain_tavily import TavilySearch


def web_search_tool():
    """Create and return a configured Tavily web-search tool.

    The returned object is intended to be passed into LangChain agents
    as a searchable tool for retrieving web results. The function reads
    the API key from the shared `config` module.

    Returns:
        TavilySearch: Configured Tavily search tool instance.
    """

    # Initialize Tavily Search Tool
    tavily_search_tool = TavilySearch(
        max_results=5,
        topic="general",
        tavily_api_key=TAVILY_API_KEY,
    )

    return tavily_search_tool


# if __name__ == "__main__":
#     user_input = "Which nation will host icc cricket worlducp 2027? Include only wikipedia sources."
#     main(user_input)

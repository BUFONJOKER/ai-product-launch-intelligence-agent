# import streamlit as st
# import subprocess
# import sys
# from pathlib import Path
from agent.state_schema.agent_state import AgentState
from langchain.agents import create_agent
from agent.tools.tavily_search import web_search_tool
# from agent.model.initialize_model import load_model
from langchain.agents.middleware import ToolCallLimitMiddleware


def MarketSentimentSpecialistAgent(model, state: AgentState):
    """Analyze market sentiment and public perception around a product launch."""

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

    return {
        'market_sentiment_specialist_agent_output': final_response
    }


# def main():
#     """Main Streamlit application."""
#     st.set_page_config(
#         page_title="Market Sentiment Analyst",
#         page_icon="🚀",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

#     st.title("🚀 AI Market Sentiment Intelligence Agent")
#     st.subheader("Analyze competitor market sentiment with AI-driven insights")

#     # Sidebar for configuration
#     with st.sidebar:
#         st.header("Configuration")
#         company_name = st.text_input(
#             "Enter company name to analyze:",
#             value="Manus AI",
#             placeholder="e.g., Manus AI, OpenAI, etc.",
#         )

#         analyze_button = st.button("🔍 Analyze Launch", use_container_width=True)

#         # Export option
#         export_format = st.selectbox(
#             "Export format:", ["None", "Markdown (.md)", "Text (.txt)"], index=0
#         )

#     # Main content area
#     if analyze_button and company_name:
#         with st.spinner(f"Analyzing {company_name}'s product launch..."):
#             try:
#                 # Load model
#                 model = load_model()

#                 # Create state
#                 state = AgentState(company_name=company_name)

#                 # Run analysis
#                 analysis = MarketSentimentSpecialistAgent(model, state)

#                 # Store in session state for export
#                 st.session_state.analysis = analysis
#                 st.session_state.company_name = company_name

#                 # Display results
#                 st.success("✅ Analysis complete!")
#                 st.markdown("---")
#                 st.markdown(analysis)

#             except Exception as e:
#                 st.error(f"❌ An error occurred: {str(e)}")
#                 st.info(
#                     "Please ensure all required environment variables are set in the .env file."
#                 )

#     elif not company_name and analyze_button:
#         st.warning("Please enter a company name to analyze.")

#     # Export functionality
#     if "analysis" in st.session_state and st.session_state.analysis:
#         st.markdown("---")
#         st.subheader("📥 Export Results")

#         col1, col2 = st.columns(2)

#         with col1:
#             if st.button("📄 Download as Markdown"):
#                 analysis_text = st.session_state.analysis
#                 filename = f"{st.session_state.company_name}_analysis.md"
#                 st.download_button(
#                     label="Download Markdown",
#                     data=analysis_text,
#                     file_name=filename,
#                     mime="text/markdown",
#                 )

#         with col2:
#             if st.button("📝 Download as Text"):
#                 analysis_text = st.session_state.analysis
#                 filename = f"{st.session_state.company_name}_analysis.txt"
#                 st.download_button(
#                     label="Download Text",
#                     data=analysis_text,
#                     file_name=filename,
#                     mime="text/plain",
#                 )


# if __name__ == "__main__":
#     # Check if we're already running in Streamlit
#     try:
#         from streamlit.runtime.scriptrunner import get_script_run_ctx

#         if get_script_run_ctx() is not None:
#             # We're already in Streamlit, run the app
#             main()
#         else:
#             # Not in Streamlit, launch it
#             current_file = Path(__file__).resolve()
#             subprocess.run(
#                 [sys.executable, "-m", "streamlit", "run", str(current_file)],
#                 check=False,
#             )
#     except (ImportError, RuntimeError):
#         # Streamlit not available or not in context, launch it
#         current_file = Path(__file__).resolve()
#         subprocess.run(
#             [sys.executable, "-m", "streamlit", "run", str(current_file)], check=False
#         )

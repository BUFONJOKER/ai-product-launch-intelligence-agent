# import streamlit as st
# import subprocess
# import sys
# from pathlib import Path
from agent.state_schema.agent_state import AgentState
from langchain.agents import create_agent
from agent.tools.tavily_search import web_search_tool
# from agent.model.initialize_model import load_model
from langchain.agents.middleware import ToolCallLimitMiddleware

def LaunchMetricsSpecialistAgent(model, state: AgentState):
    """Analyze product launch performance, growth metrics, and market traction."""

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

    return {
        'launch_metrics_specialist_agent_output': final_response
    }


# def main():
#     """Main Streamlit application."""
#     st.set_page_config(
#         page_title="Launch Metrics Specialist",
#         page_icon="🚀",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

#     st.title("🚀 AI Launch Metrics Specialist Agent")
#     st.subheader(
#         "Analyze competitor product launch performance with AI-driven insights"
#     )

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
#                 analysis = LaunchMetricsSpecialistAgent(model, state)

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

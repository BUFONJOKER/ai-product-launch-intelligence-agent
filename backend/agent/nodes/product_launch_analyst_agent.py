import streamlit as st
# import subprocess
# import sys
# from pathlib import Path
from agent.state_schema.agent_state import AgentState
from langchain.agents import create_agent
from agent.tools.tavily_search import web_search_tool
# from agent.model.initialize_model import load_model
from langchain.agents.middleware import ToolCallLimitMiddleware

def ProductLaunchAnalystAgent(model, state: AgentState):
    """Analyze a product launch using AI agent."""
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

    return {
        'product_launch_analyst_agent_output': final_response
    }


# def main():
#     """Main Streamlit application."""
#     st.set_page_config(
#         page_title="Product Launch Analyst",
#         page_icon="🚀",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

#     st.title("🚀 AI Product Launch Intelligence Agent")
#     st.subheader("Analyze competitor product launches with AI-driven insights")

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
#                 analysis = ProductLaunchAnalystAgent(model, state)

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

from langgraph.graph import StateGraph, START, END
from agent.state_schema.agent_state import AgentState
from agent.nodes.product_launch_analyst_agent import ProductLaunchAnalystAgent
from agent.nodes.market_sentiment_specialist_agent import MarketSentimentSpecialistAgent
from agent.nodes.launch_metrics_specialist_agent import LaunchMetricsSpecialistAgent
from agent.model.initialize_model import load_model
from functools import partial
import streamlit as st
import subprocess
import sys
from pathlib import Path


def build_workflow(model):

    graph = StateGraph(AgentState)

    def make_agent_node(agent_fn):
        def node(state: AgentState):
            return agent_fn(model, state)

        return node

    def agent_invoke_node(state: AgentState):
        return state

    graph.add_node("agent_invoke_node", agent_invoke_node)

    graph.add_node("product_launch_analyst", make_agent_node(ProductLaunchAnalystAgent))
    graph.add_node(
        "market_sentiment_specialist", make_agent_node(MarketSentimentSpecialistAgent)
    )
    graph.add_node(
        "launch_metrics_specialist", make_agent_node(LaunchMetricsSpecialistAgent)
    )

    def agent_to_invoke(state: AgentState):
        return state.agent_invoke

    def agent_invoke_node(state: AgentState):
        return state

    graph.add_edge(START, "agent_invoke_node")

    graph.add_conditional_edges(
        "agent_invoke_node",
        agent_to_invoke,
        {
            "product_launch_analyst": "product_launch_analyst",
            "market_sentiment_specialist": "market_sentiment_specialist",
            "launch_metrics_specialist": "launch_metrics_specialist",
        },
    )

    graph.add_edge("product_launch_analyst", END)
    graph.add_edge("market_sentiment_specialist", END)
    graph.add_edge("launch_metrics_specialist", END)

    workflow = graph.compile()

    return workflow


def main():
    st.set_page_config(
        page_title="AI Product Launch Intelligence Agent", page_icon="🤖"
    )

    st.title("AI Product Launch Intelligence Agent")

    st.write(
        "This agent provides insights and analysis for product launches, including market sentiment analysis, launch metrics evaluation, and overall product launch strategy assessment."
    )

    st.write(
        "To get started, simply enter the name of the company you want to analyze and select which agent you want to invoke for insights."
    )

    company_name = st.text_input("Company Name", key="company_name")

    agent_options = [
        "product_launch_analyst",
        "market_sentiment_specialist",
        "launch_metrics_specialist",
    ]

    agent_invoke = st.selectbox(
        "Select Agent to Invoke", options=agent_options, key="agent_invoke"
    )

    if st.button("Run Agent"):
        model = load_model()
        workflow = build_workflow(model)

        initial_state = AgentState(company_name=company_name, agent_invoke=agent_invoke)

        with st.spinner("Running agent...", show_time=True):
            result = workflow.invoke(initial_state)

        if agent_invoke == "product_launch_analyst":
            st.write(result["product_launch_analyst_agent_output"])
        elif agent_invoke == "market_sentiment_specialist":
            st.write(result["market_sentiment_specialist_agent_output"])
        elif agent_invoke == "launch_metrics_specialist":
            st.write(result["launch_metrics_specialist_agent_output"])




if __name__ == "__main__":
    # Check if we're already running in Streamlit
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        if get_script_run_ctx() is not None:
            # We're already in Streamlit, run the app
            main()
        else:
            # Not in Streamlit, launch it
            current_file = Path(__file__).resolve()
            subprocess.run(
                [sys.executable, "-m", "streamlit", "run", str(current_file)],
                check=False,
            )
    except (ImportError, RuntimeError):
        # Streamlit not available or not in context, launch it
        current_file = Path(__file__).resolve()
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(current_file)], check=False
        )

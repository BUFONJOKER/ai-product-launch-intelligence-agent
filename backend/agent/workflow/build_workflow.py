from langgraph.graph import StateGraph, START, END
from agent.state_schema.agent_state import AgentState
from agent.nodes.supervisor_agent import SupervisorAgent
from agent.nodes.product_launch_analyst_agent import ProductLaunchAnalystAgent
from agent.nodes.market_sentiment_specialist_agent import MarketSentimentSpecialistAgent
from agent.nodes.launch_metrics_specialist_agent import LaunchMetricsSpecialistAgent

from functools import partial

def build_workflow(model):

    graph = StateGraph(AgentState)

    graph.add_node("supervisor", partial(SupervisorAgent, model=model))
    graph.add_node("product_launch_analyst",partial(ProductLaunchAnalystAgent, model=model))
    graph.add_node("market_sentiment_specialist",partial(MarketSentimentSpecialistAgent, model=model))
    graph.add_node("launch_metrics_specialist",partial(LaunchMetricsSpecialistAgent, model=model))

    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "product_launch_analyst")
    graph.add_edge("supervisor", "market_sentiment_specialist")
    graph.add_edge("supervisor", "launch_metrics_specialist")
    graph.add_edge("product_launch_analyst", END)
    graph.add_edge("market_sentiment_specialist", END)
    graph.add_edge("launch_metrics_specialist", END)

    workflow = graph.compile()

    return workflow

if __name__ == "__main__":
    workflow = build_workflow(model="gpt-4")
    png_data = workflow.get_graph().draw_mermaid_png()

    # Save image
    with open("workflow.png", "wb") as f:
        f.write(png_data)

    print("Workflow image saved successfully!")
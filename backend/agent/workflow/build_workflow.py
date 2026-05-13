from langgraph.graph import StateGraph, START, END
from agent.state_schema.agent_state import AgentState
from agent.nodes.product_launch_analyst_agent import ProductLaunchAnalystAgent
from agent.nodes.market_sentiment_specialist_agent import MarketSentimentSpecialistAgent
from agent.nodes.launch_metrics_specialist_agent import LaunchMetricsSpecialistAgent

def build_workflow(model, checkpointer):
    """Construct and compile the agent state workflow graph.

    This function wires the specialist agent nodes into a `StateGraph`
    using the provided `model` for agent invocations and `checkpointer`
    for persistence. The compiled workflow can then be invoked or
    awaited by higher-level orchestration code.

    Args:
        model: A LangChain-compatible language model instance used by
            each agent node.
        checkpointer: A persistence/checkpointer object (e.g.
            AsyncPostgresSaver) used when compiling the workflow.

    Returns:
        Workflow: A compiled workflow object with `.invoke` / `.ainvoke`
            methods for running the agent pipeline.
    """

    graph = StateGraph(AgentState)

    def make_agent_node(agent_fn):
        """Create a node function that wraps a specialist agent.

        The returned `node` callable matches the StateGraph node
        signature and will invoke `agent_fn` with the shared `model` and
        the current `state`.
        """

        def node(state: AgentState):
            """Invoke the underlying agent function with the provided state.

            Args:
                state (AgentState): Current execution state for the workflow.

            Returns:
                dict: The agent's produced outputs.
            """

            return agent_fn(model, state)

        return node

    def agent_invoke_node(state: AgentState):
        """Pass-through node that carries the initial state into the graph.

        Args:
            state (AgentState): The incoming agent state.

        Returns:
            AgentState: The same state object, forwarded to conditional logic.
        """

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
        """Callback used by conditional edges to select the next node.

        It reads `state.agent_invoke` and returns the identifier used to
        choose which specialist node to run.

        Args:
            state (AgentState): Current workflow state.

        Returns:
            str: The key/name of the agent to invoke.
        """

        return state.agent_invoke

    def agent_invoke_node(state: AgentState):
        """(Duplicate pass-through used when registering nodes.)

        Mirrors the earlier `agent_invoke_node` implementation. Kept as a
        simple forwarder for compatibility with the graph API.
        """

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

    workflow = graph.compile(checkpointer=checkpointer)

    return workflow

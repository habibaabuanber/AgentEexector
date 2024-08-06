from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage
from Agents_langgrapg.backend_agent import backend_agent, backend_supervisor
from helpers.graph_helpers import agent_node
from typing import TypedDict, List, Annotated
import operator


# Define the state structure for the backend team
class TeamState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: List[str]
    next: str


# Initialize the backend graph
backend_graph = StateGraph(TeamState)

# Add nodes to the backend graph
backend_graph.add_node("DocumentationSearcher",
                       agent_node(backend_agent, "DocumentationSearcher"))
backend_graph.add_node("CodeGenerator",
                       agent_node(backend_agent, "CodeGenerator"))
backend_graph.add_node("CodeTester", agent_node(backend_agent, "CodeTester"))
backend_graph.add_node("supervisor", backend_supervisor)

# Define the edges between nodes
# backend_graph.add_edge("supervisor","DocumentationSearcher")
backend_graph.add_edge("DocumentationSearcher","supervisor")
# backend_graph.add_edge("DocumentationSearcher","CodeGenerator")
backend_graph.add_edge("CodeGenerator", "supervisor")
# backend_graph.add_edge("DocumentationSearcher", "supervisor")
# backend_graph.add_edge("supervisor","CodeTester")
backend_graph.add_edge("CodeTester", "supervisor")

# Add conditional edges for routing
backend_graph.add_conditional_edges(
    "supervisor", lambda x: x["next"], {
        "DocumentationSearcher": "DocumentationSearcher",
        "CodeGenerator": "CodeGenerator",
        "CodeTester": "CodeTester",
        "FINISH": END,
    })

# Set the entry point
backend_graph.set_entry_point("DocumentationSearcher")
backend_graph.set_finish_point("CodeTester")
backend = backend_graph.compile()

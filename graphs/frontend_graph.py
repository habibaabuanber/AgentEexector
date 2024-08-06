from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage
from Agents_langgrapg.frontend_agent import frontend_agent, frontend_supervisor
from helpers.graph_helpers import agent_node
from typing import TypedDict, List, Annotated
import operator


# Define the state structure for the frontend team
class TeamState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: List[str]
    next: str


# Initialize the frontend graph
frontend_graph = StateGraph(TeamState)

# Add nodes to the frontend graph
frontend_graph.add_node("DocumentationSearcher",
                        agent_node(frontend_agent, "DocumentationSearcher"))
frontend_graph.add_node("CodeGenerator",
                        agent_node(frontend_agent, "CodeGenerator"))
frontend_graph.add_node("CodeTester", agent_node(frontend_agent, "CodeTester"))
frontend_graph.add_node("supervisor", frontend_supervisor)

# Define the edges between nodes
# frontend_graph.add_edge("DocumentationSearcher","supervisor")
frontend_graph.add_edge("CodeGenerator", "supervisor")
# frontend_graph.add_edge("supervisor","DocumentationSearcher")
frontend_graph.add_edge("DocumentationSearcher", "supervisor")
# frontend_graph.add_edge("supervisor","CodeTester")
frontend_graph.add_edge("CodeTester", "supervisor")

# Add conditional edges for routing
frontend_graph.add_conditional_edges(
    "supervisor", lambda x: x["next"], {
        "CodeGenerator": "CodeGenerator",
        "DocumentationSearcher": "DocumentationSearcher",
        "CodeTester": "CodeTester",
        "FINISH": END,
    })

# Set the entry point
frontend_graph.set_entry_point("supervisor")
frontend_graph.set_finish_point("CodeTester")
frontend = frontend_graph.compile()

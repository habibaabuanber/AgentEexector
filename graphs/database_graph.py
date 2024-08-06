from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage
from Agents_langgrapg.database_agent import database_agent, database_supervisor
from helpers.graph_helpers import agent_node
from typing import TypedDict, List, Annotated
import operator


# Define the state structure for the database team
class TeamState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: List[str]
    next: str


# Initialize the database graph
database_graph = StateGraph(TeamState)

# Add nodes to the database graph
database_graph.add_node("DocumentationSearcher",
                        agent_node(database_agent, "DocumentationSearcher"))
database_graph.add_node("CodeGenerator",
                        agent_node(database_agent, "CodeGenerator"))
database_graph.add_node("CodeTester", agent_node(database_agent, "CodeTester"))
database_graph.add_node("supervisor", database_supervisor)

# Define the edges between nodes
# database_graph.add_edge("supervisor","DocumentationSearcher")
database_graph.add_edge("DocumentationSearcher","supervisor")
database_graph.add_edge("CodeGenerator", "supervisor")
# database_graph.add_edge("DocumentationSearcher", "supervisor")
database_graph.add_edge("CodeTester", "supervisor")

# Add conditional edges for routing
database_graph.add_conditional_edges(
    "supervisor", lambda x: x["next"], {
        "DocumentationSearcher": "DocumentationSearcher",
        "CodeGenerator": "CodeGenerator",
        "CodeTester": "CodeTester",
        "FINISH": END,
    })

# Set the entry point
database_graph.set_entry_point("supervisor")
database=database_graph.compile()
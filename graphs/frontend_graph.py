# frontend_graph.py
from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage
from Agents_langgrapg.frontend_agent import frontend_agent, frontend_supervisor,DocumentationSearcher,CodeGenerator,CodeTester
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
# frontend = frontend_graph.compile()
# Add nodes to the frontend graph
frontend_graph.add_node("DocumentationSearcher",
                        agent_node(frontend_agent, DocumentationSearcher))
frontend_graph.add_node("CodeGenerator",
                        agent_node(frontend_agent, CodeGenerator))
frontend_graph.add_node("CodeTester", agent_node(frontend_agent, CodeTester))
frontend_graph.add_node("supervisor", frontend_supervisor)

# Define the edges between nodes
frontend_graph.add_edge("DocumentationSearcher","CodeGenerator")
frontend_graph.add_edge("CodeGenerator", "CodeTester")
frontend_graph.add_edge("CodeTester", "supervisor")


# Set the entry point
frontend_graph.set_entry_point("DocumentationSearcher")
frontend_graph.set_finish_point("CodeTester")

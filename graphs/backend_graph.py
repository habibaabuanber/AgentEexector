from langgraph.graph import END, StateGraph, START
from langchain_core.messages import BaseMessage
from Agents_langgrapg.backend_agent import backend_agent, backend_supervisor,generate_code
from tools.Search_documentation import search_documentation
from tools. code_tester import test_code
from helpers.graph_helpers import agent_node
from typing import TypedDict, List, Annotated , Optional
import operator
import functools

# Define the state structure for the backend team
class backend_team_state(TypedDict):
    user_story: str
    guidelines: Optional[str]
    templates: Optional[str]
    generated_code: Optional[str]
    test_results: Optional[str]
    is_syntax_correct: Optional[bool]


# Initialize the backend graph
backend_graph = StateGraph(backend_team_state)



# Add nodes to the backend graph
backend_graph.add_node("search_documentation", lambda state: search_documentation(state["user_story"]))
backend_graph.add_node("generate_code", lambda state: generate_code(state["guidelines"], state["templates"]))
backend_graph.add_node("test_code", lambda state: test_code(state["generated_code"]))
backend_graph.add_node(backend_supervisor,"supervisor")

# Define the edges between nodes
# backend_graph.add_edge("supervisor","DocumentationSearcher")
backend_graph.add_edge(START,"search_documentation")
backend_graph.add_edge("search_documentation", "generate_code")
backend_graph.add_edge("generate_code", "test_code")
backend_graph.add_edge("test_code", END)

BackendTeam_graph = backend_graph.compile()
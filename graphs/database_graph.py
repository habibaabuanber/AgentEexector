from langgraph.graph import END, StateGraph , START
from langchain_core.messages import BaseMessage
from Agents_langgrapg.database_agent import database_agent, database_supervisor,generate_code
from tools.Search_documentation import search_documentation
from tools. code_tester import test_code
from helpers.graph_helpers import agent_node
from typing import TypedDict, List, Annotated,Optional
import operator
import functools

# Define the state structure for the database team
class database_team_state(TypedDict):
    user_story: str
    guidelines: Optional[str]
    templates: Optional[str]
    generated_code: Optional[str]
    test_results: Optional[str]
    is_syntax_correct: Optional[bool]


# Initialize the database graph
database_graph = StateGraph(database_team_state)
# database=database_graph.compile()


# Add nodes to the database graph
database_graph.add_node("search_documentation", lambda state: search_documentation(state["user_story"]))
database_graph.add_node("generate_code", lambda state: generate_code(state["guidelines"], state["templates"]))
database_graph.add_node("test_code", lambda state: test_code(state["generated_code"]))


# Define the edges between nodes
database_graph.add_edge(START , "search_documentation")
database_graph.add_edge("search_documentation","generate_code")
database_graph.add_edge("generate_code", "test_code")
database_graph.add_edge("test_code", END)


DatabaseTeam_graph=database_graph.compile()

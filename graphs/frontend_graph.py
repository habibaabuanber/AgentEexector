# frontend_graph.py
from langgraph.graph import END, StateGraph , START,END
from langchain_core.messages import BaseMessage
from Agents_langgrapg.frontend_agent import generate_code,frontend_agent, frontend_supervisor
from tools.Search_documentation import search_documentation
from tools. code_tester import test_code
from helpers.graph_helpers import agent_node
from typing import TypedDict, List, Annotated , Optional
import operator
import functools

# Define the state structure for the frontend team
class frontend_team_state(TypedDict):
    user_story: str
    guidelines: Optional[str]
    templates: Optional[str]
    generated_code: Optional[str]
    test_results: Optional[str]
    is_syntax_correct: Optional[bool]


# Initialize the frontend graph
frontend_graph = StateGraph(frontend_team_state)
# frontend = frontend_graph.compile()



# Add nodes to the frontend graph
frontend_graph.add_node("search_documentation", lambda state: search_documentation(state["user_story"]))
frontend_graph.add_node("generate_code", lambda state: generate_code(state["guidelines"], state["templates"]))
frontend_graph.add_node("test_code", lambda state: test_code(state["generated_code"]))

# Define the edges between nodes
frontend_graph.add_edge(START , "search_documentation")
frontend_graph.add_edge("search_documentation","generate_code")
frontend_graph.add_edge("generate_code", "test_code")
frontend_graph.add_edge("test_code", END)




FrontendTeam_graph=frontend_graph.compile()

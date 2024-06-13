from langgraph.graph import END, StateGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from Agents.supervisor_agent import supervisor_agent
from graphs.frontend_graph import frontend_graph
from graphs.backend_graph import backend_graph
from graphs.database_graph import database_graph
from helpers.agent_helpers import create_team_supervisor
from typing import TypedDict, List, Annotated
import operator


# Define the state structure for the top-level supervisor
class State(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: str
    next: str


def get_last_message(state: State) -> dict:
    return {
        "messages": state["messages"],
        "team_members": state["team_members"],
        "next": state["next"]
    }


def join_graph(response: dict):
    return {
        "messages": response.get("messages", []),
        "team_members": response.get("team_members", ""),
        "next": response.get("next", "")
    }


# Initialize the language model
llm = ChatOpenAI(model="gpt-4o")

# Define the top-level supervisor agent with a suitable prompt template
supervisor_prompt = (
    "You are a supervisor tasked with managing a conversation between the following teams: FrontendTeam, BackendTeam, DatabaseTeam. "
    "Given the following user stories and files related to them, respond with the team to act next. Each team will perform a task and respond with their results and status. "
    "each team will take the file that related to his role in software development so you will need to pass the correct file to the suitable team to work on "
    "When finished, respond with FINISH.")
supervisor_agent = create_team_supervisor(
    llm, supervisor_prompt, ["FrontendTeam", "BackendTeam", "DatabaseTeam"])

# Initialize the top-level graph
super_graph = StateGraph(State)

# Add nodes to the top-level graph
super_graph.add_node("FrontendTeam",
                     get_last_message | frontend_graph.compile() | join_graph)
super_graph.add_node("BackendTeam",
                     get_last_message | backend_graph.compile() | join_graph)
super_graph.add_node("DatabaseTeam",
                     get_last_message | database_graph.compile() | join_graph)
super_graph.add_node("supervisor", supervisor_agent)

# Define the edges between nodes
super_graph.add_edge("FrontendTeam", "supervisor")
super_graph.add_edge("BackendTeam", "supervisor")
super_graph.add_edge("DatabaseTeam", "supervisor")

# Add conditional edges for routing
super_graph.add_conditional_edges(
    "supervisor", lambda x: x["next"], {
        "FrontendTeam": "FrontendTeam",
        "BackendTeam": "BackendTeam",
        "DatabaseTeam": "DatabaseTeam",
        "FINISH": END,
    })

# Set the entry point
super_graph.set_entry_point("supervisor")

# Compile the top-level graph
super_graph = super_graph.compile()

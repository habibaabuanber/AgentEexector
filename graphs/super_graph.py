from langgraph.graph import END, StateGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from Agents_langgrapg.supervisor_agent import supervisor_agent,supervisor_prompt
from graphs.frontend_graph import frontend_graph
from graphs.backend_graph import backend_graph
from graphs.database_graph import database_graph
from helpers.agent_helpers import create_team_supervisor
from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver  # Using AsyncSqliteSaver
import asyncio
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
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the top-level supervisor agent with a suitable prompt template
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

# super_graph.py

async def compile_and_run(user_story: str, file_name: str):
    # Create the async checkpointer
    async with AsyncSqliteSaver.from_conn_string(":memory:") as checkpointer:
        # Compile the top-level graph with the checkpointer
        async_super_graph = super_graph.compile(checkpointer=checkpointer)
        
        # Define the input message and configuration
        input_message = HumanMessage(content=f"{user_story}\nFile: {file_name}")
        config = {"configurable": {"thread_id": "1"}}
        
        # Stream the events asynchronously
        async for event in async_super_graph.astream_events({"messages": [input_message]}, config, stream_mode="values", version="v1"):
            print("Received event:", event)  # Debugging: Print the entire event
            if "data" in event and event["data"] is not None:
                output = event["data"].get("output")
                if output is not None and isinstance(output, dict) and "messages" in output:
                    output["messages"][-1].pretty_print()
                else:
                    print("No 'messages' key in event['data']['output']")
            else:
                print("No 'data' key in event")


# Call the async function
if __name__ == "__main__":
    asyncio.run(compile_and_run())
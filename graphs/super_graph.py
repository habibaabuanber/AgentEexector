from langgraph.graph import END, StateGraph , START
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from Agents_langgrapg.supervisor_agent import supervisor_agent,supervisor_prompt
from graphs.frontend_graph import FrontendTeam_graph , frontend_team_state
from graphs.backend_graph import BackendTeam_graph ,backend_team_state
from graphs.database_graph import DatabaseTeam_graph, database_team_state
from helpers.agent_helpers import create_team_supervisor
from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver  # Using AsyncSqliteSaver
import asyncio
from typing import TypedDict, List, Annotated
import operator
import re
# Define the state structure for the top-level supervisor

class UserStory(TypedDict):
    title: str
    description: str
    file_name: str

class HighSupervisorState(TypedDict):
    user_stories: List[UserStory]
    assigned_files: List[str]

def get_last_message(state: HighSupervisorState) -> dict:
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


llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the top-level supervisor agent with a suitable prompt template
supervisor_agent = create_team_supervisor(
 llm, supervisor_prompt, ["FrontendTeam", "BackendTeam", "DatabaseTeam"])

# Initialize the top-level graph
super_graph = StateGraph(HighSupervisorState)

# Add nodes to the top-level graph
super_graph.add_node("FrontendTeam",
                     get_last_message | FrontendTeam_graph | join_graph)
super_graph.add_node("BackendTeam", 
                     get_last_message | BackendTeam_graph| join_graph)
super_graph.add_node("DatabaseTeam",
                     get_last_message | DatabaseTeam_graph | join_graph)
super_graph.add_node("supervisor", supervisor_agent)

# Define the edges between nodes
super_graph.add_edge(START, "supervisor")
super_graph.add_edge("FrontendTeam", "supervisor")
super_graph.add_edge("BackendTeam", "supervisor")
super_graph.add_edge("DatabaseTeam", "supervisor")
super_graph.add_edge("supervisor",END)

# Add conditional edges for routing
super_graph.add_conditional_edges(
    "supervisor", lambda x: x["next"], {
        "FrontendTeam": "FrontendTeam",
        "BackendTeam": "BackendTeam",
        "DatabaseTeam": "DatabaseTeam",
        "FINISH": END,})

# Set the entry point

# supervisor=super_graph.compile()
# super_graph.py

async def compile_and_run(user_story:str, file_name: list):
    # Create the async checkpointerf"HDB
    async with AsyncSqliteSaver.from_conn_string(f"{file_name[1]}.sqlite") as checkpointer:
        # Compile the top-level graph with the checkpointer
        supervisor = super_graph.compile(checkpointer=checkpointer)
        
        # Define the input message and configuration
        input_message = HumanMessage(content=f"{user_story}\nFile: {file_name}")
        config = {"configurable": {"thread_id": "0"}}
       
        # Stream the events asynchronously
        async for event in supervisor.astream_events({"messages": [input_message]}, config, stream_mode="updates", version="v1"):
       
           
        # print("Received event:", event)  # Debugging: Print the entire event
            print (event["data"])
           
            # print (,re.split("AI message",event,1))
            if "data" in event and event["data"] is not None:
                output = event["data"].get("output")
                if output is not None and isinstance(output, dict) and "messages" in output:
                    
                    
                    output["messages"][-1].pretty_print()
                    
                # else:
                #     print("No 'messages' key in event['data']['output']")
            else:
                print("No 'data' key in event")


# Call the async function
if __name__ == "__main__":
    asyncio.run(compile_and_run())
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from helpers.agent_helpers import create_team_supervisor
import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the top-level supervisor agent with a suitable prompt template
supervisor_prompt = (
    "You are a supervisor tasked with managing a conversation between the following teams: FrontendTeam, BackendTeam, DatabaseTeam. "
    "Given the following user stories and list of related files to them, respond with the team to act next. Each team will perform a task and respond with their results and status."
    "make sure that each team will take the file that is related to his role in software development so you will need to pass the correct file to the suitable team to work on only if the file related to the techonolgy used by the team "
    "pass the first file to the proper team and get the full code of this file,then pass another file of the list to another team respponsible for it , and so on . till you generate all the project files with full code ."
    "if you pass frontend/backend/database file to one team don't pass it to other teams only one team work only the relevant file to the team functionallity"
    "make sure that the team responded with the full code of the file passed to them"
    "Make sure using Markdown formatting to display the output "
    "When finished, respond with FINISH.")
supervisor_agent = create_team_supervisor(
    llm, supervisor_prompt, ["FrontendTeam", "BackendTeam", "DatabaseTeam"])

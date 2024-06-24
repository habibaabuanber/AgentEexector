from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from tools.documentation_searcher_React import tavily_tool, scrape_webpages
from tools.code_tester import web_code_tester
from helpers.agent_helpers import create_agent, create_team_supervisor
#from tools.process_img import process_image_file
from typing import List
# Initialize the language model
llm = ChatOpenAI(model="gpt-4o")

# Define the frontend agent with a suitable prompt template
frontend_prompt = (
    "You are an expert frontend developer. Generate code for the provided user story and each file related to the user story. "
    "I need the code generated for the UI to be fancy and awesome with full functionality and interactivity with the right colors and theme.\n"
    "Work autonomously according to your specialty, using the tools available to you. "
    "Do not ask for clarification. Your other team members (and other teams) will collaborate "
    "fill it with the necessary and suitable data to make it rich and realistic for using"
    "with you with their own specialties. You are chosen for a reason!")

# Create the frontend agent with the tavily_tool, scrape_webpages, and web_code_tester tools
frontend_agent = create_agent(llm,
                              [tavily_tool, scrape_webpages, web_code_tester],
                              frontend_prompt)

# Define the frontend supervisor
frontend_supervisor_prompt = (
    "You are a supervisor tasked with managing a conversation between the following workers: CodeGenerator, DocumentationSearcher, CodeTester. "
    "Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. "
    "The CodeGenerator tool will generate code for the frontend, the DocumentationSearcher tool will search for the documentation of React.js official documentation, "
    "and the CodeTester tool will ensure the code is working as expected. When finished, respond with FINISH."
    #"and the ImageProcessor tool will process image file paths to extract UI components."
)

frontend_supervisor = create_team_supervisor(
    llm, frontend_supervisor_prompt,
    ["CodeGenerator", "DocumentationSearcher", "CodeTester"])


# Example function to simulate a user story being processed by the agent
def process_user_story(
    user_story: str,
    related_files: List[str],
):
    # This function simulates the processing of a user story by the frontend agent
    # Initialize the state with the user story and related files
    state = {
        "messages": [HumanMessage(content=user_story)],
        "related_files": related_files,
    }
    #if image_file_path:
    #state["messages"].append(
    #HumanMessage(
    #content=
    #f"Please process the image at {image_file_path} to extract the UI components."

    # Define the entry point for the supervisor
    entry_point = "supervisor"

    # Initialize the AgentExecutor with the frontend supervisor
    executor = AgentExecutor(agent=frontend_supervisor, tools=[frontend_agent])

    # Execute the agent with the initial state
    result = executor.invoke(state)

    # Print the result
    print(result)

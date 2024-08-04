from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from tools.code_tester import web_code_tester
from helpers.agent_helpers import create_agent, create_team_supervisor
# from tools import documentation_searcher_mysql,documentation_searcher_express,documentation_searcher_React
from tools.documentation_searcher_mysql import tavily_tool, scrape_webpages


# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the database agent with a suitable prompt template
database_prompt = (
    "You are an expert database developer. Generate code for the provided user story.\n"
    "Work autonomously according to your specialty, using the tools available to you. "
    "Do not ask for clarification. Your other team members (and other teams) will collaborate "
    "with you with their own specialties. You are chosen for a reason!")
database_agent = create_agent(llm,[tavily_tool, scrape_webpages, web_code_tester],
                         database_prompt)

# Define the database supervisor
database_supervisor_prompt = (
    "You are a supervisor tasked with managing a conversation between the following workers: CodeGenerator, DocumentationSearcher, CodeTester. "
    "Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. "
    "the code generator tool code will be generated for the Database and the documentation searcher tool will be used to search for the documentation of mysql official documentation and the code tester tool will be ensure the code is working as expected"
    "When finished, respond with FINISH.")
database_supervisor = create_team_supervisor(
    llm, database_supervisor_prompt,
    ["DocumentationSearcher","CodeGenerator",  "CodeTester"])

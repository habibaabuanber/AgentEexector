from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from tools.documentation_searcher_express import tavily_tool, scrape_webpages
from tools.code_tester import web_code_tester
from helpers.agent_helpers import create_agent, create_team_supervisor

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the backend agent with a suitable prompt template
backend_prompt = (
    "You are an expert backend developer. Generate code for the provided user story.\n"
    "Work autonomously according to your specialty, using the tools available to you. "
    "Do not ask for clarification. Your other team members (and other teams) will collaborate "
    "with you with their own specialties. You are chosen for a reason!")
backend_agent = create_agent(llm, [tavily_tool, scrape_webpages, web_code_tester],
                             backend_prompt)

# Define the backend supervisor
backend_supervisor_prompt = (
    "You are a supervisor tasked with managing a conversation between the following workers: CodeGenerator, DocumentationSearcher, CodeTester. "
    "Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. "
    "the code generator code tool will be generated for the Backend and the documentation searcher tool will be used to search for the documentation of Express js official documentation and the code tester tool will be ensure the code is working as expected"
    "When finished, respond with FINISH.")
backend_supervisor = create_team_supervisor(
    llm, backend_supervisor_prompt,
    ["CodeGenerator", "DocumentationSearcher", "CodeTester"])

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from tools.documentation_searcher_express import tavily_tool, scrape_webpages
from tools.code_tester import test_code
from helpers.agent_helpers import create_agent, create_team_supervisor
#from tools import documentation_searcher_mysql,documentation_searcher_express,documentation_searcher_React


# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the backend agent with a suitable prompt template
backend_prompt = (
    "As a backend developer, your role in this project is to generate the code that is responsible for designing, developing, and maintaining the server-side components of the application. "
"Read the user story to Understand the goal and reason behind the feature."
"understand the detailed requirements and acceptance criteria."
"Define routes to map endpoints to controller functions."
"Validate incoming data using libraries like Joi."
"Write efficient database queries and use indexing where necessary."
"Use caching strategies to enhance performance (e.g., Redis)."
"Generate your code of your file paths that passed to you ."
)
backend_agent = create_agent(llm, [tavily_tool, scrape_webpages, test_code],
                             backend_prompt)



def generate_code(guidelines: str, templates: str) -> dict:
    # Initialize OpenAI agent
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = [
        {"role": "system", "content":
          f"You are an expert backend developer."
    "Take your template , files and guidelines from the documentationsearcher."
    "Work autonomously according to your specialty in backend developement , using the tools available to you. "
    "Generate code for the provided template in the specified files according to the documentationsearcher "
    "with you with their own specialties. You are chosen for a reason!"
    "Pass you final code to the CodeTester team member to test your code ."}]
    
    response = llm.invoke(prompt)
    
    # Extract generated code
    generated_code = response.content if hasattr(response, 'content') else 'Default code'
    
    return {"generated_code": generated_code}





# Define the backend supervisor
backend_supervisor_prompt = (
    "You are a supervisor tasked with managing a conversation between the following workers: CodeGenerator, DocumentationSearcher, CodeTester. "
    "Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. "
    "the code generator code tool will be generated for the Backend and the documentation searcher tool will be used to search for the documentation of Express js official documentation and the code tester tool will be ensure the code is working as expected"
    "When finished, respond with FINISH.")
backend_supervisor = create_team_supervisor(
    llm, backend_supervisor_prompt,
    ["search_documentation", "CodeGenerator",  "CodeTester"])


from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from tools.code_tester import test_code
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
database_agent = create_agent(llm,[tavily_tool, scrape_webpages, test_code],
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

# creating documentationsearcher agent
DocumentationSearcher_prompt=(
    "You are a worker in out database team ,As a DocumentationSearcher you play a crucial role in the software team ."
    "Start by thoroughly reading the provided user story to understand the goal and reason behind the feature. Discuss with the supervisor or product owner to clarify any ambiguities and understand the acceptance criteria."
    "You are tasked with providing right templates and guidelines for the CodeGenerator . "
    "The guidelines should be precice and clear for the code generator to start implementing their code depending on your guidelines."
    "Pass your code to the CodeGenerator ."
) 

DocumentationSearcher =create_agent(llm,[tavily_tool, scrape_webpages], DocumentationSearcher_prompt )

# codegenerator agent
def generate_code(guidelines: str, templates: str) -> dict:
    # Initialize OpenAI agent
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = [
        {"role": "system", "content":
          f"You are an expert database developer."
    "Take your template , files and guidelines from the documentationsearcher."
    "Work autonomously according to your specialty, using the tools available to you. "
    "Generate code for the provided template in the specified files according to the documentationsearcher "
    "with you with their own specialties. You are chosen for a reason!"
"Pass you final code to the CodeTester team member to test your code ." }]
    
    response = llm.invoke(prompt)
    
    # Extract generated code
    generated_code = response.content if hasattr(response, 'content') else 'Default code'
    
    return {"generated_code": generated_code}





# Codetester agent
CodeTester_prompt=(
    "You are a worker in our database team ,As a CodeTester you play a crucial in our software developement team."
    "Your primary responsibility is to test the code generated from the CodeGenerator."
    "Take the code Generated "
    "Test it and make sure it has no errors , and if not ; Rewrite the code solving these errors. "
    "Generate the final code with brief of what was the errors and what did you do to solve them."
                   )

CodeTester=create_agent(llm,[tavily_tool,scrape_webpages],CodeTester_prompt)



# def database_supervisor(state: dict) -> dict:
#     """Supervises the database agent workflow."""
#     messages = state["messages"]

#     # Start with DocumentationSearcher
#     if len(messages) == 1: 
#         return {"next": "DocumentationSearcher"}

#     # Move to CodeGenerator after DocumentationSearcher
#     elif state.get("next") == "DocumentationSearcher":
#         return {"next": "CodeGenerator"}

#     # Finally to CodeTester, then FINISH
#     elif state.get("next") == "CodeGenerator":
#         return {"next": "CodeTester"}
    
#     else:
#         return {"next": "FINISH"}
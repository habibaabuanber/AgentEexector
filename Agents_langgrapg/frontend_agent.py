from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from tools.code_tester import web_code_tester
from helpers.agent_helpers import create_agent, create_team_supervisor
#from tools import documentation_searcher_mysql,documentation_searcher_express,documentation_searcher_React
from typing import List
from tools.documentation_searcher_React import tavily_tool, scrape_webpages

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the frontend agent with a suitable prompt template
frontend_prompt = ("As a frontend developer, you play a crucial role in the software development team. Your primary responsibility is to create the visual and interactive aspects of the application, ensuring a seamless user experience."
"Start by thoroughly reading the provided user story to understand the goal and reason behind the feature. Discuss with the supervisor or product owner to clarify any ambiguities and understand the acceptance criteria."
"Ensure your project structure is well-organized with separate folders for HTML, CSS, JavaScript, and assets. Determine the appropriate file path for the new feature components."
"Create the structure of the page using HTML. Style the page using CSS, ensuring the design aligns with the approved mockups and branding guidelines. Add interactivity using JavaScript, making use of the available frameworks and libraries (e.g., React, Vue.js, Angular)."
"Use JavaScript to fetch data from the backend API and dynamically update the DOM with the received data. Write unit tests for your components to ensure they function correctly. Test the feature across different browsers and devices to ensure compatibility."
"Minify CSS and JavaScript files, optimize images, and use lazy loading where necessary. Use tools like Lighthouse to audit performance and make improvements."
"Submit your code for peer review to get feedback and catch any potential issues. Make necessary changes based on feedback to improve code quality. Use Git to commit your changes with meaningful messages."
"Combine the previous steps to produce well performance code necessary to create the project. Ensure the UI is visually appealing, responsive, and fully functional, with a focus on delivering an exceptional user experience."
"I need the code generated for the UI to be fancy and awesome with full functionality and interactivity with the right colors and theme.fill it with the necessary and suitable data to make it rich and realistic for using"
"Remember, you are an expert frontend developer, and you have the autonomy to use your skills and expertise to generate high performance with all possible fuctionalities and themes code. Work confidently and effectively, collaborating with your team members as needed to deliver a successful project."
    )

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
    ["DocumentationSearcher","CodeGenerator",  "CodeTester"])


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

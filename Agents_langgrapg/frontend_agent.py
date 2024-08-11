from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from helpers.agent_helpers import create_agent,create_team_supervisor
from typing import List
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
                              [tavily_tool, scrape_webpages],
                              frontend_prompt)

frontend_supervisor_prompt = (
    "You are a supervisor tasked with managing a conversation between the following workers: CodeGenerator, DocumentationSearcher, CodeTester. "
    "Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. "
    "The CodeGenerator tool will generate code for the frontend, the DocumentationSearcher tool will search for the documentation of React.js official documentation, "
    "and the CodeTester tool will ensure the code is working as expected. When finished, respond with FINISH."
    #"and the ImageProcessor tool will process image file paths to extract UI components."
)


# creating documentationsearcher agent
DocumentationSearcher_prompt=(
    "You are a worker in out frontend team ,As a DocumentationSearcher you play a crucial role in the software team ."
    "Start by thoroughly reading the provided user story to understand the goal and reason behind the feature. Discuss with the supervisor or product owner to clarify any ambiguities and understand the acceptance criteria."
    "You are tasked with providing right templates and guidelines for the CodeGenerator . "
    "The guidelines should be precice and clear for the code generator to start implementing their code depending on your guidelines."
    "Pass your code to the CodeGenerator ."
) 

DocumentationSearcher =create_agent(llm,[tavily_tool, scrape_webpages], DocumentationSearcher_prompt )

# codegenerator agent
CodeGenerator_prompt=("You are a worker in our frontend team ,As a frontend CodeGenerator, you play a crucial role in the software development team."
"Your primary responsibility is to create the visual and interactive aspects of the application, ensuring a seamless user experience."
"Start integerating the template and guidelines that was given to you from the DocumentationSearcher "
"Ensure your project structure is well-organized with separate folders for HTML, CSS,  and assets. Determine the appropriate file path for the new feature components."
"Create the structure of the page using HTML. Style the page using CSS, ensuring the design aligns with the approved mockups and branding guidelines."
"Minify CSS and JavaScript files, optimize images, and use lazy loading where necessary. Use tools like Lighthouse to audit performance and make improvements."
"Don't create code of files not passed to you ,as you are in frontend team to create the specific code and capabilities of frontend developement. "
"Submit your code for peer review to get feedback and catch any potential issues. Make necessary changes based on feedback to improve code quality. Use Git to commit your changes with meaningful messages."
"Combine the previous steps to produce well performance code necessary to create the project. Ensure the UI is visually appealing, responsive, and fully functional, with a focus on delivering an exceptional user experience."
"I need the code generated for the UI to be fancy and awesome with full functionality and interactivity with the right colors and theme.fill it with the necessary and suitable data to make it rich and realistic for using"
"Remember, you are an expert frontend developer, and you have the autonomy to use your skills and expertise to generate high performance with all possible fuctionalities and themes code. Work confidently and effectively."
"Pass you final code to the CodeTester team member to test your code ."
    )
CodeGenerator=create_agent(llm,[tavily_tool,scrape_webpages],CodeGenerator_prompt)

# Codetester agent
CodeTester_prompt=(
    "You are a worker in our frontend team ,As a CodeTester you play a crucial in our software developement team."
    "Your primary responsibility is to test the code generated from the CodeGenerator."
    "Take the code Generated "
    "Test it and make sure it has no errors , and if not Rewrite the code solving these errors. "
    "Gnerate the final code with brief of what was the errors and what did you do to solve them."
                   )

CodeTester=create_agent(llm,[tavily_tool,scrape_webpages],CodeGenerator_prompt)




# Modify the frontend supervisor to manage the agent sequence
def frontend_supervisor(state: dict) -> dict:
    """Supervises the frontend agent workflow."""
    messages = state["messages"]

    # Start with DocumentationSearcher
    if len(messages) == 1: 
        return {"next": DocumentationSearcher}

    # Move to CodeGenerator after DocumentationSearcher
    elif state.get("next") == DocumentationSearcher:
        return {"next": CodeGenerator}

    # Finally to CodeTester, then FINISH
    elif state.get("next") == CodeGenerator:
        return {"next": CodeTester}
    
    else:
        return {"next": "FINISH"}


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

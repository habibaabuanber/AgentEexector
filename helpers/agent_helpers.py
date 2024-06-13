from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from typing import List


def create_agent(llm: ChatOpenAI, tools: List[BaseTool],
                 system_prompt: str) -> AgentExecutor:
    """
        Create a function-calling agent with the provided tools and system prompt.
        """
    system_prompt += "\nWork autonomously according to your specialty, using the tools available to you. "
    system_prompt += "Do not ask for clarification. Your other team members (and other teams) will collaborate "
    system_prompt += "with you with their own specialties. You are chosen for a reason!"

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


def create_team_supervisor(llm: ChatOpenAI, system_prompt: str,
                           members: List[str]) -> AgentExecutor:
    """
        Create a function-calling supervisor agent to manage team members.
        """
    options = ["FINISH"] + members
    function_def = {
        "name": "route",
        "description": "Select the next role.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [{
                        "enum": options
                    }],
                },
            },
            "required": ["next"],
        },
    }

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system",
         "Given the conversation above, who should act next? Or should we FINISH? Select one of: {options}"
         ),
    ]).partial(options=str(options), team_members=", ".join(members))

    return (prompt
            | llm.bind_functions(functions=[function_def],
                                 function_call="route")
            | JsonOutputFunctionsParser())

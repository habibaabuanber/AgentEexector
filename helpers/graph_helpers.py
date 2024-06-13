from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain.agents import AgentExecutor
from typing import Dict, Any


def agent_node(agent: AgentExecutor, name: str):
               """
    A helper function to invoke an agent and format its response.
    """

               def node(state: Dict[str, Any]) -> Dict[str, Any]:
                              result = agent.invoke(state)
                              # Determine the type of message based on the agent's response
                              message_type = "ai"  # Assuming the agent's response should be an AI message
                              return {
                                  "messages": [
                                      AIMessage(content=result["output"],
                                                name=name,
                                                type=message_type)
                                  ]
                              }

               return node

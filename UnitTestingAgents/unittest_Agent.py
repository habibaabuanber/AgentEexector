from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import os 

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

llm = ChatOpenAI(model="gpt-3.5-turbo")


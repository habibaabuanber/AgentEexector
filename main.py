# main.py
from graphs.super_graph import compile_and_run  # Import the async function
import os
import asyncio

# Entry point to run the multi-agent system

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TAVILY_API_KEY = os.environ['TAVILY_API_KEY']

def get_user_input():
    user_story = "login and signup in website"
    file_name = "user_auth.py"
    return user_story, file_name

if __name__ == "__main__":
    user_story, file_name = get_user_input()
    asyncio.run(compile_and_run(user_story, file_name))

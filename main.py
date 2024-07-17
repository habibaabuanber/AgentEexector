# main.py
from graphs.super_graph import compile_and_run  # Import the async function
import os
import asyncio
import requests

# Entry point to run the multi-agent system

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TAVILY_API_KEY = os.environ['TAVILY_API_KEY']

def get_user_input():
    user_story = "login and signup in website"
    file_name = "user_auth.py"
    return user_story, file_name

def get_description(file_name):
    url = f'http://localhost:8000/api/descriptions/{file_name}/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['description']
    else:
        return "Description not found."

if __name__ == "__main__":
    user_story, file_name = get_user_input()
    description = get_description(file_name)
    print(f"File: {file_name}\nDescription: {description}")
    #asyncio.run(compile_and_run(user_story, file_name))

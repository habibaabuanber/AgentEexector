# main.py
from graphs.super_graph import compile_and_run  # Import the async function
import os
import asyncio
import numpy as np
# Entry point to run the multi-agent system

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TAVILY_API_KEY = os.environ['TAVILY_API_KEY']

def get_user_input():
    
    # user_story = "login and signup for website called Obelion "
    # file_name = ["user_auth.html","user_auth.js"]


    user_story ="As a new user, I want to provide my basic information during registration,such as name and date of birth, so that I can personalize my profile.passing to frontend team (Register.html) file to create registeration page,and passing to backend team (Register.js) file to implement the the registeration information and to improve the functionality of saving information.   "
    file_name =   ["Register.js" ,"Register.html"]
    return user_story, file_name


if __name__ == "__main__":
    
    user_story, file_name = get_user_input()
    
    asyncio.run(compile_and_run(user_story, file_name),debug=True)

# import openai
# import json
# from langchain_core.tools import tool
# from typing import Annotated
# import os

# # Set your OpenAI API key
# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']


# @tool
# def web_code_tester(code: Annotated[
#     str, "The web development code (HTML/CSS/JavaScript) to test."]):
#     """
#             Use this tool to test web development code. The code will be validated for syntax and functional correctness.
#             """
#     # Escape the code string to be valid JSON
#     clean_code = code.replace("```jsx", "").replace("```", "").strip()
#     code_json = json.dumps(clean_code)

#     # Prompt to OpenAI to generate test cases and validate the code
#     prompt = f"""
#             You are an expert web developer. I need you to test the following web development code for syntax errors and functional correctness. The code includes HTML, CSS, and JavaScript. Please provide a detailed report on any issues found and ensure the code works as expected

#             Code to test:
#             {code_json}

#             Make sure to:
#             1. Check for syntax errors.
#             2. Validate that the HTML structure is correct.
#             3. Ensure the CSS styles are applied correctly.
#             4. Confirm that the JavaScript functions as intended.
#             5. Provide suggestions for improvement if any.
#             """

#     try:
#         # Generate the result using OpenAI
#         response = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt=prompt,
#             max_tokens=1024,
#             temperature=0.5,
#         )
#         result = response.choices[0].text.strip()
#         return f"Successfully tested:\n{code}\n\nReport:\n{result}"
#     except BaseException as e:
#         return f"Failed to test. Error: {repr(e)}"
from langchain_openai import ChatOpenAI

def test_code(generated_code: str) -> dict:
    # Initialize OpenAI agent
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = [
        {"role": "system", "content": f"Test the following code for syntax and correctness: {generated_code}"}
    ]
    response = llm.invoke(prompt)

    # Extract test results
    is_syntax_correct = response.content if hasattr(response, 'content') else True
    test_results = response.content if hasattr(response, 'content') else 'Default test results'

    return {"is_syntax_correct": is_syntax_correct, "test_results": test_results}

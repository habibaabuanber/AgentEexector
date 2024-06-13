# image_processor.py
from langchain_core.tools import tool
import base64
import json
from langchain_community.llms import OpenAI

file_path = "original-d7a41fa9f9a84dc97d0149616af3843b.jpg"


@tool
def process_image_file(file_path: str) -> str:
    """
    Process the provided image file path to extract UI components and return a description of these components.
    """
    try:
        # Read the image file and convert it to base64 format
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode("utf-8")

        # Construct the prompt
        prompt = (
            f"Extract UI components from the following image: {encoded_string[:50]}... "
            f"(base64 encoded). Describe the UI components and their structure and provide instructions "
            f"to create this UI with colors and functionality.")

        # Use GPT-4o to process the base64-encoded image
        response = OpenAI(model="gpt-4o", prompt=prompt, n=1, size="1024x1024")

        # Ensure the response format is as expected
        if 'data' in response and len(response['data']) > 0:
            ui_description = response['data'][0].get(
                'text', 'No description provided.')
        else:
            raise ValueError("Unexpected response format from OpenAI API")

        return ui_description

    except Exception as e:
        return f"Error processing image file: {str(e)}"

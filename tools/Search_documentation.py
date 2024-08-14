from langchain_openai import ChatOpenAI
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def generate_search_keywords(user_story: str) -> str:
    # Initialize OpenAI agent
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = [
        {"role": "system", "content": "Generate search keywords"},
        {"role": "user", "content": user_story}
    ]
    
    # Use the invoke method to get a response
    response = llm.invoke(prompt)
    
    # Access the content attribute of the AIMessage
    keywords = response.content if hasattr(response, 'content') else 'guidelines templates components'
    
    return keywords

def scrape_web(keywords: str) -> dict:
    # Define search URL using generated keywords
    search_url = f"https://www.google.com/search?q={keywords}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    guidelines = []
    templates = []

    # Limit scraping to the first 3 results
    result_count = 0
    for link in soup.find_all('a', href=True):
        if result_count >= 3:
            break

        href = link['href']
        if href.startswith('/url?q='):
            actual_url = urljoin("https://www.google.com/", href)

            # Skip redirect notices and login pages
            if "google.com/url" in actual_url or "accounts.google.com" in actual_url:
                continue

            try:
                page_response = requests.get(actual_url)
                page_soup = BeautifulSoup(page_response.text, 'html.parser')

                # Extract content (customize this based on the website structure)
                content = page_soup.find('body').text  # Example, replace 'body' with a more specific tag if needed

                if 'guideline' in content.lower():
                    guidelines.append(content)
                if 'template' in content.lower():
                    templates.append(content)

                result_count += 1

            except Exception as e:
                print(f"Error scraping {actual_url}: {e}")

    return {
        "guidelines": guidelines or "Default guidelines",
        "templates": templates or "Default templates"
}


def search_documentation(user_story: str) -> dict:
    # Generate search keywords
    keywords = generate_search_keywords(user_story)

    # Scrape the web for relevant information
    scraped_data = scrape_web(keywords)

    # Initialize OpenAI agent
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = [
        {"role": "system", "content": f"Refine the following data based on the user story: {user_story}. Guidelines: {scraped_data['guidelines']}, Templates: {scraped_data['templates']}"}
    ]
    # Use invoke for consistency
    response = llm.invoke(prompt)

    # Extract refined guidelines and templates
    guidelines = response.content if hasattr(response, 'content') else scraped_data['guidelines']
    templates = response.content if hasattr(response, 'content') else scraped_data['templates']

    return {"guidelines": guidelines, "templates": templates}

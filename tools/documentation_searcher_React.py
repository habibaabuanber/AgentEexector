from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_community.document_loaders import WebBaseLoader
from typing import List
from bs4 import BeautifulSoup

# Initialize the Tavily search tool
tavily_tool = TavilySearchResults(max_results=5)

urls = ["https://react.dev/reference/react"]
@tool
def scrape_webpages(urls: List[str]) -> str:
    """
    Use requests and BeautifulSoup to scrape the provided web pages for detailed information and code snippets.
    """
    loader = WebBaseLoader(urls)
    docs = loader.load()
    extracted_info = []

    for doc in docs:
        soup = BeautifulSoup(doc.page_content, 'html.parser')
        # Extract code snippets
        code_snippets = [code.get_text() for code in soup.find_all('code')]
        # Extract relevant information
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        headers = [
            h.get_text()
            for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        ]

        # Combine extracted information
        combined_info = "\n\n".join(headers + paragraphs + code_snippets)
        extracted_info.append(
            f'<Document name="{doc.metadata.get("title", "")}">\n{combined_info}\n</Document>'
        )

    return "\n\n".join(extracted_info)

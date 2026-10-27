from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the Tavily client for web searches
client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def tavily_search(query):
    """
    Search the web using Tavily and return formatted results with titles, URLs, and snippets.
    """

    # Fetch the top five search results for the given query
    response=client.search(
        query=query,
        max_results=5
    )

    results=[]

    # Extract and format relevant details from each search result
    for i, r in enumerate(response["results"], 1):
        title   = r.get("title", "Unknown")
        url     = r.get("url", "")
        snippet = r.get("content", "").strip()
        # Keep only the first 300 characters to avoid wall-of-text
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        # Store each result with its title, URL, and content snippet
        results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

    # Combine all formatted results into a single string
    return "\n\n".join(results)
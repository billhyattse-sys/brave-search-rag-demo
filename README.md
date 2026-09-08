import os
import requests

def fetch_brave_search_context(query: str):
    """
    Fetches grounded web context snippets from the Brave Search API
    to inject into an LLM context window (RAG pipeline).
    """
    # 1. Set up the endpoint and authentication headers
    # Brave uses 'X-Subscription-Token' for API key authentication
    url = "https://api.search.brave.com/res/v1/llm/context"
    
    api_key = os.getenv("BRAVE_API_KEY", "YOUR_BRAVE_API_KEY")
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    
    # 2. Define request parameters (query, snippet count, etc.)
    params = {
        "q": query,
        "count": 5
    }

    try:
        # 3. Execute GET request
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        # Raise an exception for HTTP errors (4xx, 5xx)
        response.raise_for_status()
        
        # 4. Parse JSON payload
        data = response.json()
        
        # 5. Extract web search results
        web_results = data.get("web", {}).get("results", [])
        
        print(f"--- Top Search Results for: '{query}' ---\n")
        for idx, item in enumerate(web_results, start=1):
            title = item.get("title")
            link = item.get("url")
            # Extract description snippet
            snippet = item.get("description", "No snippet available.")
            
            print(f"[{idx}] {title}")
            print(f"    URL: {link}")
            print(f"    Snippet: {snippet}\n")
            
        return web_results

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err} - Response: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    # Test execution
    search_query = "latest agentic AI frameworks 2026"
    fetch_brave_search_context(search_query)

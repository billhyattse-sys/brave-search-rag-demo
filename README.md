What the Script DoesThis Python script is a lightweight API integration client designed to connect to the Brave Search API (/res/v1/llm/context) and retrieve clean, structured web search data.

How it works under the hood, step by step:

Imports Core Libraries: It imports requests (Python’s standard library for HTTP calls) and os (to securely pull your API key from environment variables).  
Constructs the Request:Endpoint: Targets Brave’s LLM search endpoint ([https://api.search.brave.com/res/v1/llm/context](https://api.search.brave.com/res/v1/llm/context)).
Headers & Authentication: Adds X-Subscription-Token (Brave's required header format) to authenticate the request with your API key.
Parameters: Sets the search query (q) and limits the payload to 5 results (count).
Executes the HTTP GET Call: Sends the GET request to Brave's servers.  

Error Handling & Parsing: Checks for a 200 OK status code. If successful, it parses the JSON response body and extracts the title, URL, and snippet text for each result.  

Output: Prints the formatted results directly to your console screen.



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
    

import os
import requests

def fetch_brave_search_results(query: str):
    # Base Web Search API endpoint
    url = "https://api.search.brave.com/res/v1/web/search"
    api_key = os.getenv("BRAVE_API_KEY")
    
    if not api_key:
        print("Error: BRAVE_API_KEY environment variable not set.")
        return

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    
    params = {
        "q": query,
        "count": 5
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("web", {}).get("results", [])
        print(f"\n--- Top Search Results for: '{query}' ---\n")
        
        for idx, item in enumerate(results, start=1):
            title = item.get("title", "No Title")
            link = item.get("url", "No Link")
            snippet = item.get("description", "No Description")
            print(f"[{idx}] {title}")
            print(f"    URL: {link}")
            print(f"    Snippet: {snippet}\n")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err} - Response: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    fetch_brave_search_results("latest agentic AI frameworks 2026")

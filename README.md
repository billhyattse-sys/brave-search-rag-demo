# Brave Search API: Web Search & Local Mapping (RAG Demo)

A lightweight, enterprise-ready Python implementation demonstrating how to ground Large Language Models (LLMs) and autonomous agents using the **Brave Search API** — covering both the Web Search endpoint (`/res/v1/web/search`) and the Local Search endpoint (`/res/v1/local/place_search`).

This repository provides a clean, language-agnostic proof-of-concept (POC) for enterprise pre-sales engineers, AI architects, and developers evaluating real-time, low-latency web grounding inside Retrieval-Augmented Generation (RAG) pipelines.

---

## Architecture Overview

```
[ User Query ]
      │
      ▼
┌───────────────────────────┐
│  Brave Search API Gateway │ ──> Live, independent web index
└───────────────────────────┘
      │
      ▼
┌───────────────────────────┐
│   Structured JSON Result  │ ──> Titles, URLs, Snippets (Web) or
│                            │     Places, Addresses, Coordinates (Local)
└───────────────────────────┘
      │
      ▼
[ Enterprise LLM / Agent / Map ]
```

### Key Technical Highlights
* **Web Search Endpoint:** `brave_demo.py` queries `/res/v1/web/search` directly — real-time, independent web results, not a Bing or Google reseller.
* **Local Search Endpoint:** `brave_map_demo.py` extends the same API key to `/res/v1/local/place_search` and `/res/v1/local/pois`, finding real-world places and rendering them on an interactive map.
* **Environment-Based Auth:** Both scripts follow security best practices, injecting credentials dynamically via `BRAVE_API_KEY` rather than hardcoding tokens.
* **Production Error Handling:** Explicit HTTP status checks (`raise_for_status()`) with separate handling for HTTP errors versus general exceptions.

---

## Prerequisites

* **Python:** Version `3.8+`
* **Brave API Key:** A free or paid subscription token from the [Brave Search API Dashboard](https://api-dashboard.search.brave.com)
* **Dependencies:** `requests`, `folium` (see `requirements.txt`)

---

## Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/billhyattse-sys/brave-search-rag-demo.git
cd brave-search-rag-demo
```

### 2. Install Dependencies
```bash
python3 -m pip install -r requirements.txt
```

### 3. Set Your API Key Environment Variable
```bash
export BRAVE_API_KEY="your_brave_api_key_here"
```
This must be re-exported every time a new terminal session is opened.

### 4. Run Either Script
```bash
python3 brave_demo.py         # web search
python3 brave_map_demo.py     # local search + interactive map
```

---

## Example Usage & Code Structure

`brave_demo.py` sends a structured request to Brave's Web Search endpoint and prints parsed, RAG-ready results:

```python
import os
import requests

def fetch_brave_search_results(query: str):
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
    params = {"q": query, "count": 5}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("web", {}).get("results", [])

        for idx, item in enumerate(results, start=1):
            title = item.get("title", "No Title")
            link = item.get("url", "No Link")
            snippet = item.get("description", "No Description")
            print(f"[{idx}] {title}\n    URL: {link}\n    Snippet: {snippet}\n")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err} - Response: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")
```

### Sample Output

```text
--- Top Search Results for: 'latest agentic AI frameworks 2026' ---

[1] Agentic AI Frameworks 2026: Production Comparison
    URL: https://uvik.net/blog/agentic-ai-frameworks/
    Snippet: Agentic AI Frameworks in 2026: The Production Comparison...

[2] Latest AI Agent Frameworks in 2026: Ranked + Enterprise Guide
    URL: https://www.ampcome.com/post/latest-ai-agent-frameworks-2026
    Snippet: Compare the latest AI agent frameworks in 2026 — LangGraph, CrewAI...
```

---

## Local Search & Interactive Mapping

`brave_map_demo.py` extends this project to Brave's Local Search API, finding real-world places and rendering them as an interactive map — a second, independent proof-of-concept alongside the web search integration above.

**What it does:**
- Queries Brave's Place Search endpoint (`/local/place_search`) to find businesses near a location
- Enriches results with full details — address, phone, coordinates — via a batched call to `/local/pois`
- Renders the results as a real interactive map using [Folium](https://python-visualization.github.io/folium/) (Python + Leaflet.js + OpenStreetMap tiles)

Generates `brave_places_map.html` in the project folder — open it in any browser to view the map. (Setup and run commands are the same as the Quickstart Guide above — one shared environment covers both scripts.)

---

## Enterprise Use Cases

* **Hallucination Mitigation:** Ground domain-specific enterprise prompts with real-time web context.
* **Agentic Workflows:** Supply autonomous agents with accurate tool-use search capabilities.
* **Cost Optimization:** Reduce token overhead by fetching pre-parsed, concise context chunks rather than raw HTML DOM trees.
* **Local & Geospatial Grounding:** Extend the same pattern to real-world places, addresses, and mapping use cases.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

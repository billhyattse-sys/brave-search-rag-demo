# Brave Search API: LLM Context Integration (RAG Demo)

A lightweight, enterprise-ready Python implementation demonstrating how to ground Large Language Models (LLMs) and autonomous agents using the **Brave Search LLM Context API** (`/res/v1/llm/context`).

This repository provides a clean, language-agnostic proof-of-concept (POC) for enterprise pre-sales engineers, AI architects, and developers evaluating real-time, low-latency web grounding inside Retrieval-Augmented Generation (RAG) pipelines.

---

## Architecture Overview

```
[ User Query / Prompt ] 
          │
          ▼
┌───────────────────────────┐
│  Brave Search API Gateway │ ──> Grounded Search & Context Parsing
└───────────────────────────┘
          │
          ▼
┌───────────────────────────┐
│ Context-Augmented Payload │ ──> Clean JSON Data (Titles, URLs, Snippets)
└───────────────────────────┘
          │
          ▼
[ Enterprise LLM / Agent ]
```

### Key Technical Highlights
* **Direct Grounding Endpoint:** Interacts with Brave's specialized `/res/v1/llm/context` API designed specifically to feed noise-free web context into LLMs.
* **Environment-Based Auth:** Follows security best practices by injecting credentials dynamically via `BRAVE_API_KEY` rather than hardcoding tokens.
* **Production Error Handling:** Implements explicit HTTP status checks (`raise_for_status()`) and handles authorization or rate-limiting exceptions gracefully.

---

## Prerequisites

* **Python:** Version `3.8+`
* **Brave API Key:** A free or paid subscription token from [Brave Search API Portal](https://api.search.brave.com/)
* **Dependencies:** `requests` library

---

## Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/billhyattse-sys/brave-search-rag-demo.git
cd brave-search-rag-demo
```

### 2. Install Required Dependencies
```bash
pip3 install requests
```

### 3. Set Your API Key Environment Variable
Export your Brave API key into your terminal session:

```bash
export BRAVE_API_KEY="your_brave_api_key_here"
```

### 4. Run the Script
Execute the script to test live RAG context retrieval:

```bash
python3 brave_demo.py
```

---

## Example Usage & Code Structure

The script sends a structured request to the Brave LLM Context endpoint and outputs parsed results optimized for RAG injection:

```python
import os
import requests

def fetch_brave_search_context(query: str):
    url = "https://api.search.brave.com/res/v1/llm/context"
    api_key = os.getenv("BRAVE_API_KEY")
    
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    
    params = {"q": query, "count": 5}
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
```

### Sample Output

```text
--- Top Grounded Search Results for: 'latest agentic AI frameworks 2026' ---

[1] Agentic AI Frameworks 2026: Production Comparison
    URL: https://uvik.net/blog/agentic-ai-frameworks/
    Snippet: Agentic AI Frameworks in 2026: The Production Comparison...

[2] Latest AI Agent Frameworks in 2026: Ranked + Enterprise Guide
    URL: https://www.ampcome.com/post/latest-ai-agent-frameworks-2026
    Snippet: Compare the latest AI agent frameworks in 2026 — LangGraph, CrewAI...
```

---

## Enterprise Use Cases

* **Hallucination Mitigation:** Ground domain-specific enterprise prompts with real-time web context.
* **Agentic Workflows:** Supply autonomous agents with accurate tool-use search capabilities.
* **Cost Optimization:** Reduce token overhead by fetching pre-parsed, concise context chunks rather than raw HTML DOM trees.

---


## Local Search & Interactive Mapping

`brave_map_demo.py` extends this project to Brave's Local Search API, finding real-world places and rendering them as an interactive map — a second, independent proof-of-concept alongside the web search integration above.

**What it does:**
- Queries Brave's Place Search endpoint (`/local/place_search`) to find businesses near a location
- Enriches results with full details — address, phone, coordinates — via a batched call to `/local/pois`
- Renders the results as a real interactive map using [Folium](https://python-visualization.github.io/folium/) (Python + Leaflet.js + OpenStreetMap tiles)

**Setup:**
```bash
python3 -m pip install -r requirements.txt
```

**Run it:**
```bash
export BRAVE_API_KEY="your_api_key_here"
python3 brave_map_demo.py
```

Generates `brave_places_map.html` in the project folder — open it in any browser to view the map.






## License

This project is licensed under the MIT License - see the LICENSE file for details.




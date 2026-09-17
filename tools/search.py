"""
    This file is for anything related to searching. Search is handled by Tavily's search API.

import os
import requests
from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()
TAVILY_CLIENT = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
"""

SEARCH_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search for the internet for current or real-time information not in your training data (recent facts, current events, contemporary figures, trends)",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "A short, specific search query"}
                },
                "required": ["query"]
            }
        }
    }
]

def search_for_info(query):
    return "HERE IS YOUR QUERY: " + query

search_dispatch = {
    "web_search": search_for_info
}
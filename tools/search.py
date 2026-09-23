"""
    This file is for anything related to searching. Search is handled by Tavily's search API.
"""

import os
import requests
from abc import ABC, abstractmethod
import requests
from dotenv import load_dotenv
"""
from tavily import TavilyClient
"""

# Because this search query is likely the one I will expand upon the most (general info, weather, news, etc.), I want to abstract it so I only have to implement
# the logic for a search and formatting flow. Every subclass of this class will just serve
class SearchQuery(ABC):
    def search(self, query):
        try: 
            response = self._execute(query)
            return self._format(response)
        except requests.exceptions.Timeout:
            return "Search request timed out."
        except requests.exceptions.RequestException as e:
            return f"Error with requests: {e}"
    
    @abstractmethod
    def _execute(self, query):
        # To be inherited: each API has a different request body shape so each method needs a different implementation.
        ...

    @abstractmethod
    def _format(self, response):
        # To be inherited: each API returns a different JSON shape so each method needs a different implementation.
        ...

class TavilyProvider(SearchQuery):
    def __init__(self, api_key):
        self.api_key = api_key

    def _execute(self, query):
        return query
        # look up how tavily client works with requests
    
    def _format(self, response):
        print("This is your query: ", response)
        # investigate json shape

# -- instantiate providers here -- 

load_dotenv()

tavily = TavilyProvider(api_key=os.getenv("FILLER_KEY"))

# -- tools format for Jarvis to look at --

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

# -- function defs here -- 

def search_for_info(query):
    return tavily.search(query)

search_dispatch = {
    "web_search": search_for_info
}
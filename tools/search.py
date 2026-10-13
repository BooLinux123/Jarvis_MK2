"""
    This file is for anything related to searching. Search is handled by Tavily's search API.
"""

import os
import requests
from abc import ABC, abstractmethod
import requests
import json
from dotenv import load_dotenv

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

# -- general web search using tavily --
class TavilyProvider(SearchQuery):
    def __init__(self, api_key):
        self.api_key = api_key

    def _execute(self, query):
        """
        requests.post("https://api.tavily.com/search", json={
            "api_key": self.api_key,
            "query": query,
            "max_results": 3 
        })
        """
        return query
        # look up how tavily client works with requests
    
    def _format(self, json):
        print("This is your query: ", json)
        # investigate json shape

# -- specific weather data using open-matteo -- 
class WeatherProvider(SearchQuery):
    def __init__(self):
        pass

    WMO_WEATHER_CODES = weathercodeTable = {
                0: "clear sky",
                1: "mainly clear",
                2: "partly cloudy",
                3: "overcast",
                45: "fog",
                48: "depositing rime fog",
                51: "light drizzle",
                53: "moderate drizzle",
                55: "dense drizzle",
                56: "light freezing drizzle",
                57: "dense freezing drizzle",
                61: "slight rain",
                63: "moderate rain",
                65: "heavy rain",
                66: "light freezing rain",
                67: "heavy freezing rain",
                71: "slight snowfall",
                73: "moderate snowfall",
                75: "heavy snowfall",
                77: "snow grains",
                80: "slight rain showers",
                81: "moderate rain showers",
                82: "violent rain showers",
                85: "slight snow showers",
                86: "heavy snow showers",
                95: "thunderstorm",
                96: "thunderstorm with slight hail",
                97: "heavy thunderstorm",
                99: "thunderstorm with heavy hail"
            }

    # Flow: user inputs location: "What will the weather in X be like today/next week" -> Jarvis calls tool and seaches for the coords of the location -> pass the
    # coords of the best match to the actual weather endpoint -> return response
    def _execute(self, location_name):
        if location_name == "" or location_name == None:
            location_name = "Boston"

        # step one: get coords
        try:
            coordinates = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={
                "name": location_name,
                "count": 1
            }, timeout=10).json()
        except requests.exceptions.JSONDecodeError:
            raise ValueError("Geocoding API returned a non-JSON response")

        if not isinstance(coordinates, dict) or not coordinates.get("results"):
            raise ValueError(f"Could not find any results for '{location_name}'")
        
        match = coordinates["results"][0]
        latitude = match["latitude"]
        longitude = match["longitude"]
        place = ", ".join(filter(None, [match["name"], match.get("admin1"), match.get("country")]))

        # step two: retrieve data based on coords
        try:
            weather_details = requests.get("https://api.open-meteo.com/v1/forecast", params={
                "latitude": latitude, "longitude": longitude, "current_weather": True, "forecast_days": 7, "temperature_unit": "fahrenheit"
            }, timeout=10).json()
        except requests.exceptions.JSONDecodeError:
            raise ValueError("Weather results returned a non-JSON response")

        weather_details["place"] = place

        return weather_details

    # parse API json response from open-meteo
    def _format(self, response):
        values = response['current_weather']
        units = response['current_weather_units']

        relevant_keys = ["temperature", "windspeed", "winddirection"]
        formattedResponse = [f"{key}: {values[key]}{units.get(key, '')}" for key in relevant_keys]

        # add country in case two towns are named the same
        formattedResponse.insert(0, f"location: {response['place']}")

        # add result of the weathercode to indicate conditions
        formattedResponse.append("current weather conditions: " + self.WMO_WEATHER_CODES[values["weathercode"]])

        print(formattedResponse)

        return ", ".join(formattedResponse)

# -- instantiate providers here -- 

load_dotenv()

tavily = TavilyProvider(api_key=os.getenv("FILLER_KEY"))
weather = WeatherProvider()

# -- tools format for Jarvis to look at --

SEARCH_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": ("Search for the internet for current or real-time information not in your training data (recent facts, current events, contemporary figures, trends)."
            "Use this for general questions not fully covered by your training data"),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "A short, specific search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "weather_search",
            "description": ("Get current weather conditions (temperature, wind, forecast) from a specified city or location. Only use this when a user wants to "
            "know the current weather conditions or forecast at a place. If none is given, default to Boston"),
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {"type": "string", "description": "The name of a town or city"}
                },
                "required": ["location_name"]
            }
        }
    }
]

# -- function defs here -- 

def search_for_info(query):
    return tavily.search(query)

def search_for_weather(location_name):
    return weather.search(location_name)

search_dispatch = {
    "web_search": search_for_info,
    "weather_search": search_for_weather
}
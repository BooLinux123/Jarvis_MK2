"""
    This file imports all of the commands form the different files and condenses them into the tools array for Jarvis to use
"""

from tools.lights import LIGHT_TOOLS, light_dispatch
from tools.search import SEARCH_TOOLS, search_dispatch

ALL_TOOLS = LIGHT_TOOLS + SEARCH_TOOLS

DISPATCH_TABLE = {
    **light_dispatch,
    **search_dispatch
}


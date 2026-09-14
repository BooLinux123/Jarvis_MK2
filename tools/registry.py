"""
    This file imports all of the commands form the different files and condenses them into the tools array for Jarvis to use
"""

from lights import LIGHT_TOOLS, light_dispatch

ALL_TOOLS = LIGHT_TOOLS

DISPATCH_TABLE = {
    **light_dispatch
}


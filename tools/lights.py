"""
    Used for controlling lights (turning them on, turning them off, dimming them)
"""

LIGHT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "toggle_lights",
            "description": "Turn the lights on or off",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {"type": "string", "enum": ["on", "off"]}
                },
                "required": ["state"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dim_lights",
            "description": "Set a light's brightness to either an percentage level or a level by name (max/high/medium/low/off)",
            "parameters": {
                "type": "object",
                "properties": {
                    "brightness": {
                        "description": "Brightness can be either a preset name or an exact number",
                        "oneOf": [
                            {"type": "string", "enum": ["max", "high", "medium", "low", "off"]},
                            {"type": "integer", "minimum": 0, "maximum": 100}
                        ]
                    }
                },
                "required": ["brightness"]
            }
        }
    }
]

#one param: state -> determines whether to turn the light on or off
#uses string to enforce idempotency
#REQUIRE THE DEVICE/LIST OF DEVICES IN THE FUTURE
def toggleLights(state: str) -> str:
    if state == "on":
        print("on")
        return "on"
    else: 
        print("off")
        return "off"
    
#Also add device list later for additional params
def dimLights(brightness):
    #vocal brightness command
    if isinstance(brightness, str):
        match brightness: 
            case "max":
                print(brightness, "100")
                return 100
            case "high":
                print(brightness, "75")
                return 75
            case "medium":
                print(brightness, "50")
                return 50
            case "low":
                print(brightness, "25")
                return 25
            case _:
                print(brightness, "0")
                return 0
    #adjust with integers
    else:
        print(brightness)
        return brightness

light_dispatch = {
    "toggle_lights": toggleLights,
    "dim_lights": dimLights
}

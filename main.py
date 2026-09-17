import requests
from tools.registry import ALL_TOOLS, DISPATCH_TABLE

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "Jarvis"

conversation_history = []

def chat(user_message):
    conversation_history.append({"role":"user", "content":user_message})

    response = requests.post(OLLAMA_URL, json = {
        "model": MODEL_NAME,
        "messages": conversation_history,
        "tools": ALL_TOOLS,
        "think": False,
        "stream": False
    })

    data = response.json()

    conversation_history.append(data["message"])

    return data

def handle_response(data):
    print("DATA RECEIVED: ", data)
    message = data["message"]

    if "tool_calls" in message and message["tool_calls"]:
        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            function = DISPATCH_TABLE.get(name)
            if function:
                result = function(**args)
                conversation_history.append({
                    "role":"tool",
                    "content": str(result) if result is not None else " done"
                })
            else:
                conversation_history.append({
                    "role": "tool",
                    "content": f"Error: '{name}' is not a valid tool"
                })
                print("The model tried to use an unknown tool: ", name)
    else:
        print("Jarvis:", message["content"])

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit", "goodbye", "bye"):
            break
        else:
            data = chat(user_input)
            handle_response(data)
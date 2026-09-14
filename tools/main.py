import requests
from registry import ALL_TOOLS, DISPATCH_TABLE

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "Jarvis"

def chat(user_message):
    response = requests.post(OLLAMA_URL, json = {
        "model": MODEL_NAME,
        "messages": [{"role":"user", "content": user_message}],
        "tools": ALL_TOOLS,
        "stream": False
    })

    return response.json()

def handle_response(data):
    print("DATA RECEIVED: ", data)
    message = data["message"]

    if "tool_calls" in message and message["tool_calls"]:
        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            function = DISPATCH_TABLE.get(name)
            if function:
                function(**args)
            else:
                print("The model tried to use an unknown tool: ", name)
    else:
        print("Jarvis ", message["content"])

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit", "goodbye"):
            break
        else:
            data = chat(user_input)
            handle_response(data)
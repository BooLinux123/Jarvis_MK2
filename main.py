import requests
from tools.registry import ALL_TOOLS, DISPATCH_TABLE

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "Jarvis"
MAX_TOOL_ROUNDS = 5
# how many of the most recent user turns to keep in context
MAX_HISTORY_TURNS = 8

conversation_history = []

# Keep the context window from overflowing. We only ever cut at a "user" message so that
# an assistant tool_call never gets separated from its matching tool result - splitting
# that pair makes the API reject the history.
def trim_history():
    user_turns = [i for i, m in enumerate(conversation_history) if m.get("role") == "user"]
    if len(user_turns) > MAX_HISTORY_TURNS:
        del conversation_history[:user_turns[-MAX_HISTORY_TURNS]]

# this method uses the actual api - it's seperated because not every chat needs a new message
def send_to_ollama():
    trim_history()

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

def chat(user_message):
    conversation_history.append({"role": "user", "content": user_message})
    return send_to_ollama()

def handle_response(data):
    #print("DATA RECEIVED: ", data["message"])
    #print("\n")
    message = data["message"]

    if "tool_calls" in message and message["tool_calls"]:
        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            function = DISPATCH_TABLE.get(name)
            if function:
                result = function(**args)
                conversation_history.append({
                    "role": "tool",
                    "content": str(result) if result is not None else " done"
                })
            else:
                conversation_history.append({
                    "role": "tool",
                    "content": f"Error: '{name}' is not a valid tool"
                })
                print("The model tried to use an unknown tool: ", name)
        handle_response(send_to_ollama())
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
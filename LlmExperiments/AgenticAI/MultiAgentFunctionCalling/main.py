import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define available functions
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

def get_weather(city: str) -> str:
    """Get mock weather information for a city."""
    # Mock implementation
    return f"The weather in {city} is sunny with 25°C."

# Function mapping
available_functions = {
    "add_numbers": add_numbers,
    "get_weather": get_weather,
}

# Tools available to the subagent
subagent_tools = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "First number"},
                    "b": {"type": "integer", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather information for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
        },
    },
]

# List of tools for the coordinator agent; it only delegates to the subagent
tools = [
    {
        "type": "function",
        "function": {
            "name": "run_subagent",
            "description": "Delegate a task to a subagent that can call available tools",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "The task to delegate to the subagent."},
                },
                "required": ["task"],
            },
        },
    },
]

# Run a tool-driven query through the subagent
def run_tool_call_flow(query: str) -> str:
    messages = [
        {"role": "system", "content": "You are a subagent that can use tools to answer tasks."},
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=subagent_tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    if response_message.tool_calls:
        messages.append(response_message)
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_to_call = available_functions[function_name]
            function_result = function_to_call(**function_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(function_result),
            })

        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return second_response.choices[0].message.content

    return response_message.content

# Subagent delegate function
def run_subagent(task: str) -> str:
    return run_tool_call_flow(task)

# Add the subagent delegate to the function mapping
available_functions["run_subagent"] = run_subagent

def main():
    messages = [
        {"role": "system", "content": "You are a coordinator assistant. Use the run_subagent tool when a task should be delegated to a specialist subagent for tool execution."},
        {"role": "user", "content": "What is 5 + 3? Also, what's the weather in Tokyo?"},
    ]

    # Make the API call with tools
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # Let the model decide when to use tools
    )

    response_message = response.choices[0].message
    messages.append(response_message)

    # Check if the model wants to call functions
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Call the function
            function_to_call = available_functions[function_name]
            function_result = function_to_call(**function_args)

            # Add the function result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(function_result),
            })

        # Make a second API call with the function results
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        print(second_response.choices[0].message.content)
    else:
        print(response_message.content)

if __name__ == "__main__":
    main()
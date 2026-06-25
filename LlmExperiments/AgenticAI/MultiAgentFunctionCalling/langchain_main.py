import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType

# Load environment variables
load_dotenv()

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define tools using LangChain's @tool decorator
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@tool
def get_weather(city: str) -> str:
    """Get mock weather information for a city."""
    # Mock implementation
    return f"The weather in {city} is sunny with 25°C."

# Create a worker subagent that can use the direct tools
worker_agent = initialize_agent(
    tools=[add_numbers, get_weather],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True,
)

@tool
def delegate_to_subagent(task: str) -> str:
    """Delegate a task to the worker subagent."""
    return worker_agent.run(task)

# Create a coordinator agent that uses the subagent delegate tool
coordinator_agent = initialize_agent(
    tools=[delegate_to_subagent],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True,
)

def main():
    # Example query
    query = "What is 5 + 3? Also, what's the weather in Tokyo?"
    
    # Run the coordinator agent
    response = coordinator_agent.run(query)
    
    print(response)

if __name__ == "__main__":
    main()
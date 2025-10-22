from langchain.agents import create_agent
from langchain.messages import AnyMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_agent(
    model="ollama:gpt-oss:20b",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

input = {
    "messages": [
        {"role": "user", "content": "what is the weather in sf"}
    ]
}

response = agent.invoke(input)

print(response)
print(type(response))  # str
ai_message: AnyMessage = response["messages"][-1]
print(ai_message.content)  # It's always sunny in sf!

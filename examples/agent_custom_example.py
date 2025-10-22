from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_ollama.chat_models import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field


class Context(BaseModel):
    """
    Context schema for the agent.

    Attributes:
        user_id (str): The unique identifier for the user.
    """
    user_id: str = Field(
        title="User ID",
        description="The unique identifier for the user"
    )


class ResponseFormat(BaseModel):
    """
    Response format schema for the agent.

    Attributes:
        punny_response (str): A pun-filled response about the weather.
        weather_conditions (str | None): The actual weather conditions, if provided.
    """
    punny_response: str = Field(
        title="Punny Weather Response",
        description="A pun-filled response about the weather"
    )
    weather_conditions: str | None = Field(
        default=None,
        title="Weather Conditions",
        description="The actual weather conditions, if provided"
    )


@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


model = ChatOllama(
    model="gpt-oss:20b",
    temperature=0.3,
    max_tokens=1000
)

checkpointer = InMemorySaver()

SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location.
If you can tell from the question that they mean wherever they are, use the
get_user_location tool to find their location.
"""


agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "what is the weather outside?"}
        ]
    },
    config=config,
    context=Context(user_id="1")
)

print("Response: ", response)

# TODO: ESSE ACESSO A "structured_response" ESTÁ DANDO ERRO!

print("First Structured Response: ", response["messages"]['structured_response'])

# Note that we can continue the conversation using the same `thread_id`.
response = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},
    config=config,
    context=Context(user_id="1")
)

print("Second Structured Response: ", response['structured_response'])

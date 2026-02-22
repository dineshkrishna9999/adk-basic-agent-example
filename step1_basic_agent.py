"""
Basic ADK Agent Example

Demonstrates a simple agent with custom tools and Azure OpenAI integration.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()


def add(a: int, b: int) -> str:
    """Add two numbers and return the result."""
    return f"{a + b}"


def main():
    """Main function to run the basic agent."""
    agent = Agent(
        name="basic_agent",
        model=LiteLlm(model=os.environ["AZURE_MODEL"]),
        instruction="You are a helpful assistant. Reply in one short sentence.",
        description="A helpful assistant that can perform basic calculations.",
        tools=[add],
    )
    
    session_service = InMemorySessionService()

    runner = Runner(
        agent=agent,
        session_service=session_service,
        app_name="basicAgent",
        auto_create_session=True,
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text="Hello, add these numbers: 1 and 2")]
    )

    response = ""
    for event in runner.run(new_message=content, session_id="123", user_id="123"):
        if event.content and event.content.parts:
            response = event.content.parts[0].text

    print(response)


if __name__ == "__main__":
    main()

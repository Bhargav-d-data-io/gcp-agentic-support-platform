import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from support_agent.agent import root_agent


APP_NAME = "support-platform"
USER_ID = "demo-customer"
SESSION_ID = "demo-session-001"


async def send_message(runner, message):
    content = types.Content(
        role="user",
        parts=[types.Part(text=message)],
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print("AGENT:", event.content.parts[0].text)


async def main():
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={"customer_name": "Bhargav"},
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("TURN 1")
    await send_message(
        runner,
        "My name is Bhargav and my laptop arrived damaged.",
    )

    print("\nTURN 2")
    await send_message(
        runner,
        "What was my name and what problem did I tell you about?",
    )


if __name__ == "__main__":
    asyncio.run(main())


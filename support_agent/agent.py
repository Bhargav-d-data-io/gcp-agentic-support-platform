
from google.adk.agents import Agent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from .tools import search_support_knowledge, create_support_ticket


async def save_session_to_memory(ctx):
    """Persist the current conversation to the configured memory service."""
    await ctx.add_session_to_memory()


retrieval_agent = Agent(
    name="retrieval_agent",
    model="gemini-2.5-flash",
    description="Retrieves relevant customer-support policies and knowledge.",
    instruction="""
You are the retrieval specialist in a customer-support system.

Your responsibility is to find factual support information before an answer
is produced.

Use search_support_knowledge when the user asks about refunds, shipping,
password/account access, damaged products, or related support policies.

Return the relevant information clearly and do not invent policies.
""",
    tools=[search_support_knowledge],
)


reasoning_agent = Agent(
    name="reasoning_agent",
    model="gemini-2.5-flash",
    description="Reasons over retrieved support information and determines the next step.",
    instruction="""
You are the reasoning specialist.

Analyze the customer's request and information supplied by the retrieval
agent.

Determine whether:
1. The question can be answered using available support information, or
2. An operational action or escalation is required.

Give a concise customer-support response.
Do not invent company policies.
""",
)


action_agent = Agent(
    name="action_agent",
    model="gemini-2.5-flash",
    description="Performs support actions such as creating escalation tickets.",
    instruction="""
You are the action specialist.

Use create_support_ticket only when the customer's problem requires
escalation or follow-up.

When a ticket is created, clearly return both the ticket ID and correlation ID,
and explain that the issue has been escalated.
""",
    tools=[create_support_ticket],
)


root_agent = Agent(
    name="customer_support_orchestrator",
    model="gemini-2.5-flash",
    description="Orchestrates specialized customer-support agents.",
    instruction="""
You are the customer-support orchestrator.

Route requests to the appropriate specialized agent.

Use retrieval_agent when support knowledge or policy information is needed.
Use reasoning_agent when retrieved information needs interpretation.
Use action_agent when the request requires an operational action or escalation.

Keep responses concise, grounded, and customer friendly.
""",
    sub_agents=[
        retrieval_agent,
        reasoning_agent,
        action_agent,
    ],
    tools=[PreloadMemoryTool()],
    after_agent_callback=save_session_to_memory,
)

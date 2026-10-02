from typing import Dict
import uuid


# Small demo knowledge base for the retrieval agent.
KNOWLEDGE_BASE = {
    "refund": (
        "Refunds can be requested within 30 days of purchase. "
        "Approved refunds are normally returned to the original payment method."
    ),
    "shipping": (
        "Standard shipping normally takes 3-5 business days. "
        "Customers can request order tracking information."
    ),
    "password": (
        "Customers who cannot access their account should use the password-reset "
        "flow. A reset link is sent to the registered email address."
    ),
    "damaged": (
        "Customers reporting damaged products should provide the order number "
        "and a description of the damage. The case can then be escalated."
    ),
}


def search_support_knowledge(query: str) -> Dict[str, str]:
    """Search the demo customer-support knowledge base."""
    query_lower = query.lower()

    for topic, answer in KNOWLEDGE_BASE.items():
        if topic in query_lower:
            return {
                "status": "found",
                "topic": topic,
                "content": answer,
            }

    return {
        "status": "not_found",
        "topic": "unknown",
        "content": "No matching support policy was found.",
    }


def create_support_ticket(issue: str, customer_id: str = "demo-customer") -> Dict[str, str]:
    """Create a simulated support ticket for issues requiring action."""
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"

    return {
        "status": "created",
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "issue": issue,
    }

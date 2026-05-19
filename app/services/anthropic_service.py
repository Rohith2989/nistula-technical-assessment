import anthropic
import json
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def get_ai_draft(message: str, guest_name: str, context: str):
    # We use "tools" to force Claude to return a structured object
    tools = [{
        "name": "draft_concierge_reply",
        "description": "Classifies intent and drafts a response for a luxury villa guest.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query_type": {
                    "type": "string",
                    "enum": ["pre_sales_availability", "pre_sales_pricing", "post_sales_checkin", "special_request", "complaint", "general_enquiry"]
                },
                "drafted_reply": {"type": "string"}
            },
            "required": ["query_type", "drafted_reply"]
        }
    }]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=f"You are the Nistula AI. Context: {context}",
        tools=tools,
        tool_choice={"type": "tool", "name": "draft_concierge_reply"},
        messages=[{"role": "user", "content": f"Guest: {guest_name}. Message: {message}"}]
    )

    # Extract the tool input
    for block in response.content:
        if block.type == "tool_use":
            return block.input
    return None
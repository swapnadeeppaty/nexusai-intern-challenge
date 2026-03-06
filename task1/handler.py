import asyncio
from dataclasses import dataclass
from typing import Optional
from openai import AsyncOpenAI

# Initialize OpenAI client
client = AsyncOpenAI()

SYSTEM_PROMPT = """
You are an AI telecom support agent for a large internet service provider.

Your responsibilities:
- Help customers with internet connectivity problems, billing issues, plan upgrades, and outages.
- Provide clear, polite, and professional responses.

Rules:
- Voice responses must be under 2 sentences.
- Chat and WhatsApp responses may be longer.
- If the issue cannot be solved automatically, suggest escalation to a human agent.

Return format:
Response: <message>
Confidence: <0-1>
Suggested_Action: <resolve | escalate | request_more_info>
"""


@dataclass
class MessageResponse:
    response_text: str
    confidence: float
    suggested_action: str
    channel_formatted_response: str
    error: Optional[str]


async def handle_message(customer_message: str, customer_id: str, channel: str) -> MessageResponse:

    # Handle empty or whitespace-only input
    if not customer_message or customer_message.strip() == "":
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="none",
            channel_formatted_response="",
            error="empty_input"
        )

    try:

        try:
            completion = await asyncio.wait_for(
                client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": customer_message}
                    ],
                    temperature=0.3
                ),
                timeout=10
            )

        except Exception as e:

            # Retry once if rate limited
            if "rate" in str(e).lower():
                await asyncio.sleep(2)

                completion = await asyncio.wait_for(
                    client.chat.completions.create(
                        model="gpt-4.1-mini",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": customer_message}
                        ],
                        temperature=0.3
                    ),
                    timeout=10
                )
            else:
                raise e

        ai_text = completion.choices[0].message.content

        return MessageResponse(
            response_text=ai_text,
            confidence=0.8,
            suggested_action="resolve",
            channel_formatted_response=ai_text,
            error=None
        )

    except asyncio.TimeoutError:
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="none",
            channel_formatted_response="",
            error="api_timeout"
        )

    except Exception as e:
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="none",
            channel_formatted_response="",
            error=str(e)
        )
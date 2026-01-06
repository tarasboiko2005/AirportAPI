import os
import datetime
import logging
from django.conf import settings
from google import genai
from google.genai.types import GenerateContentConfig, AutomaticFunctionCallingConfig
from .tools import search_flights, get_ticket_details, get_user_orders

logger = logging.getLogger("assistant")

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.txt")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    BASE_PROMPT = f.read()

def get_client():
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")
    return genai.Client(api_key=api_key)

class AIService:
    def __init__(self, user):
        today = datetime.date.today().strftime("%Y-%m-%d")
        weekday = datetime.date.today().strftime("%A")

        time_context = (
            f"\nSYSTEM CONTEXT:\n"
            f"Today is {weekday}, {today}.\n"
            f"When user says 'next week' or 'tomorrow', calculate dates based on today.\n"
        )

        username = getattr(user, "username", "guest")
        email = getattr(user, "email", "guest@example.com")

        user_context = (
            "\n--- CURRENT USER CONTEXT ---\n"
            f"Username: {username}\n"
            f"Email: {email}\n"
            "------------------------------\n"
        )

        system_instruction = BASE_PROMPT + time_context + user_context

        self.client = get_client()
        self.config = GenerateContentConfig(
            tools=[search_flights, get_ticket_details, get_user_orders],
            automatic_function_calling=AutomaticFunctionCallingConfig(
                disable=False,
                maximum_remote_calls=3,
            ),
            system_instruction=system_instruction,
        )
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config=self.config,
        )

    def get_response(self, user_message: str) -> str:
        try:
            response = self.chat.send_message(user_message)
            return response.text
        except Exception:
            logger.exception("LLM error")
            return "<p>LLM service temporarily unavailable.</p>"

def stream_response(prompt: str):
    client = get_client()
    response = client.models.generate_content_stream(
        model="models/gemini-flash-latest",
        contents=prompt,
    )

    for chunk in response:
        try:
            for candidate in chunk.candidates or []:
                for part in candidate.content.parts or []:
                    if hasattr(part, "text") and part.text:
                        yield part.text
        except Exception:
            logger.exception("Stream chunk parse failed")
            continue
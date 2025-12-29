import os
import logging
from typing import Dict, Any
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMClientError(Exception):
    pass

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "")
        if not self.api_key:
            logger.warning("LLM_API_KEY is not set. Using simulation mode.")

    def extract_intent(self, prompt: str, lang: str = "en") -> Dict[str, Any]:
        """
        Extracts intent from a natural language prompt.
        Returns a JSON-like dict with keys:
          - action: str
          - filters: dict
          - fields: list[str]
          - limit: int
          - sort: dict
          - errors: list[str]
        """
        if not self.api_key:
            return self._simulate_intent(prompt, lang)

        try:
            # TODO: Replace with actual API call to your LLM provider
            return self._simulate_intent(prompt, lang)
        except Exception as e:
            logger.exception("LLM intent extraction failed")
            raise LLMClientError(str(e))

    def _simulate_intent(self, prompt: str, lang: str) -> Dict[str, Any]:
        lower = prompt.lower()
        date_str = None

        match_en = re.search(r"on (\w+) (\d{1,2})", lower)
        if match_en:
            month_name = match_en.group(1).capitalize()
            day = int(match_en.group(2))
            try:
                dt = datetime.strptime(f"{day} {month_name} 2025", "%d %B %Y")
                date_str = dt.strftime("%Y-%m-%d")
            except Exception:
                pass

        if "flight" in lower or "flights" in lower:
            return {
                "action": "search_flights",
                "filters": {"date": date_str} if date_str else {},
                "fields": [],
                "limit": 20,
                "sort": {"by": "departure_time", "order": "asc"},
                "errors": []
            }

        if "countries" in lower or "country" in lower:
            return {
                "action": "search_countries_from_origin",
                "filters": {"origin": "LWO", **({"date": date_str} if date_str else {})},
                "fields": ["country_name", "country_code"],
                "limit": 20,
                "sort": {"by": None, "order": None},
                "errors": []
            }

        if "airlines" in lower or "airline" in lower:
            return {
                "action": "search_airlines_from_airport",
                "filters": {"origin": "LWO", **({"date": date_str} if date_str else {})},
                "fields": ["airline_name", "airline_code"],
                "limit": 20,
                "sort": {"by": None, "order": None},
                "errors": []
            }

        if "tickets" in lower or "ticket" in lower:
            return {
                "action": "search_tickets",
                "filters": {},
                "fields": ["seat_number", "status", "price"],
                "limit": 20,
                "sort": {"by": None, "order": None},
                "errors": []
            }

        if "available" in lower:
            return {
                "action": "search_available_tickets",
                "filters": {},
                "fields": ["seat_number", "price"],
                "limit": 20,
                "sort": {"by": None, "order": None},
                "errors": []
            }

        if "booked" in lower:
            return {
                "action": "search_booked_tickets",
                "filters": {},
                "fields": ["seat_number", "price", "order_id"],
                "limit": 20,
                "sort": {"by": None, "order": None},
                "errors": []
            }

        return {
            "action": "unknown",
            "filters": {},
            "fields": [],
            "limit": 20,
            "sort": {"by": None, "order": None},
            "errors": ["Could not infer intent"]
        }
import re
from typing import Dict, Any, Tuple
from datetime import date, timedelta

def map_intent(intent: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    action = intent.get("action", "unknown")
    filters = intent.get("filters", {}) or {}
    fields = intent.get("fields", []) or []
    sort = intent.get("sort", {"by": None, "order": None}) or {"by": None, "order": None}
    limit = intent.get("limit", 20)

    params = {
        "filters": filters,
        "fields": fields,
        "sort": sort,
        "limit": limit,
    }

    prompt_text = intent.get("prompt", "").lower()

    match = re.search(r"from ([a-zA-Z\s]+?) to ([a-zA-Z\s]+?)(?:\s|$)", prompt_text)
    if match:
        origin, destination = match.groups()
        destination = destination.replace("tomorrow", "").replace("today", "").strip()
        origin = origin.replace("tomorrow", "").replace("today", "").strip()
        params["filters"]["origin"] = origin.title()
        params["filters"]["destination"] = destination.title()

    if "tomorrow" in prompt_text:
        params["filters"]["date"] = (date.today() + timedelta(days=1)).isoformat()
    elif "today" in prompt_text:
        params["filters"]["date"] = date.today().isoformat()

    if ("заброньован" in prompt_text and "квит" in prompt_text) or ("booked" in prompt_text and "ticket" in prompt_text):
        return "search_booked_tickets", params
    if ("вільн" in prompt_text and "квит" in prompt_text) or ("available" in prompt_text and "ticket" in prompt_text):
        return "search_available_tickets", params
    if "квит" in prompt_text or "ticket" in prompt_text:
        return "search_tickets", params
    if "рейс" in prompt_text or "flight" in prompt_text or "flights" in prompt_text:
        return "search_flights", params
    if "країн" in prompt_text or "country" in prompt_text or "countries" in prompt_text:
        return "search_countries_from_origin", params
    if "авіакомпан" in prompt_text or "airline" in prompt_text or "airlines" in prompt_text:
        return "search_airlines_from_airport", params
    if action in [
        "search_flights",
        "search_countries_from_origin",
        "search_airlines_from_airport",
        "search_tickets",
        "search_available_tickets",
        "search_booked_tickets",
    ]:
        return action, params

    return "unknown", params
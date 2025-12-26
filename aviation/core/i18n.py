def detect_lang(text: str) -> str:
    """
    Naive language detection: if Ukrainian letters are present → 'ua', else 'en'.
    """
    uk_letters = set("іїєґ")
    return "ua" if any(ch in text.lower() for ch in uk_letters) else "en"

def t(key: str, lang: str = "en") -> str:
    """
    Translation dictionary for system messages.
    """
    messages = {
        "ua": {
            "intent_unknown": "Не вдалося зрозуміти запит. Уточніть, будь ласка.",
            "no_results": "Нічого не знайдено за вашим запитом.",
        },
        "en": {
            "intent_unknown": "Unable to understand the query. Please clarify.",
            "no_results": "No results found for your query.",
        }
    }
    return messages.get(lang, messages["en"]).get(key, key)
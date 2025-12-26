import json
from google import genai
from django.conf import settings
import logging

class RoadmapGenerator:
    MODEL_NAME = "models/gemini-flash-latest"

    PROMPT_TEMPLATE = """
    You are a strict JSON generator. Your ONLY task is to return a valid JSON object
    that follows the schema below.

    Schema:
    {
        "skills": [
            {
                "title": "Skill Name",
                "category": "Category Name",
                "difficulty": 1,
                "description": "Short description"
            }
        ],
        "dependencies": [
            {
                "from": "Skill Name",
                "to": "Skill Name",
                "type": "hard"
            }
        ]
    }

    Strict rules:
    1. Keys MUST be exactly "skills" and "dependencies".
    2. Values must be in the same language as the topic (Ukrainian → Ukrainian values, English → English values).
    3. "difficulty" must be an integer 1–4.
    4. "type" must be "hard" or "soft".
    5. Generate 7–10 skills.
    6. All dependencies must reference existing skills.
    7. Output must be valid JSON parsable by Python's json.loads().
    8. No text, comments, or formatting outside the JSON.
    """

    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing")
        self.client = genai.Client(api_key=api_key)

    def generate(self, topic: str) -> dict:
        prompt = self.PROMPT_TEMPLATE + f"\nTopic: {topic}\nIMPORTANT: Your output MUST start directly with '{{' and end with '}}'. Do not include any text before or after the JSON."

        response = self.client.models.generate_content(
            model=self.MODEL_NAME,
            contents=prompt
        )

        text = response.text or ""
        logger = logging.getLogger("llm")
        logger.warning("🔍 Gemini raw response:\n%s", text)

        start = text.find("{")
        end = text.rfind("}") + 1
        cleaned = text[start:end].strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error("JSON decode failed: %s", e)
            logger.error("Raw text was:\n%s", text)
            raise ValueError(f"Gemini returned invalid JSON: {e}")

        if not isinstance(data.get("skills"), list):
            data["skills"] = [{
                "title": "Placeholder Skill",
                "category": "General",
                "difficulty": 1,
                "description": "Auto-generated fallback"
            }]
        if not isinstance(data.get("dependencies"), list):
            data["dependencies"] = []

        self._validate_schema(data)
        return {
            "skills": data["skills"],
            "dependencies": data["dependencies"]
        }

    def _validate_schema(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise ValueError("Roadmap must be a JSON object")

        skills = data.get("skills", [])
        deps = data.get("dependencies", [])

        if not (7 <= len(skills) <= 10):
            raise ValueError("Skills count must be between 7 and 10")

        titles = set()
        for s in skills:
            if not all(k in s for k in ("title", "category", "difficulty", "description")):
                raise ValueError("Skill item missing required fields")
            if not isinstance(s["difficulty"], int) or not (1 <= s["difficulty"] <= 4):
                raise ValueError("difficulty must be integer 1-4")
            titles.add(s["title"])

        for d in deps:
            if not all(k in d for k in ("from", "to", "type")):
                raise ValueError("Dependency item missing required fields")
            if d["type"] not in ("hard", "soft"):
                raise ValueError("Dependency type must be 'hard' or 'soft'")
            if d["from"] not in titles or d["to"] not in titles:
                raise ValueError("Dependencies must reference existing skills")
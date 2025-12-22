import os
import sys
import django
import json
import re
from google import genai

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aviation.settings")
sys.path.append("/app/aviation")
django.setup()

from django.conf import settings

def main():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    print("Available models:")
    for model in client.models.list():
        print("-", model.name)

    model_name = "models/gemini-flash-latest"

    prompt = "Назви 7 навичок для теми: Авіаційна безпека. Поверни JSON."

    print("\nSending prompt to:", model_name)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    text = response.text or ""
    print("\n🔍 RAW Gemini response:\n", text)

    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        data = json.loads(cleaned)
        print("\nParsed JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print("\nJSON parsing failed:", e)
        print("Raw text:\n", text)

if __name__ == "__main__":
    main()
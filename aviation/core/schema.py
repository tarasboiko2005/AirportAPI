from typing import Any, Dict, List, Optional

def ok(data: Any, message: Optional[str] = None, lang: str = "en") -> Dict[str, Any]:
    return {
        "status": "ok",
        "message": message or ("Success" if lang == "en" else "Успішно"),
        "data": data,
    }

def fail(message: str, errors: Optional[List[str]] = None, lang: str = "en") -> Dict[str, Any]:
    return {
        "status": "error",
        "message": message,
        "errors": errors or [],
        "data": None,
    }
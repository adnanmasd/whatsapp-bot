# app/lang/__init__.py
from app.lang import en, ar

LANG_MAP = {"en": en.TEXT, "ar": ar.TEXT}

def get_text(key: str, lang: str = "en") -> str:
    return LANG_MAP.get(lang, en.TEXT).get(key, f"[{key}]")

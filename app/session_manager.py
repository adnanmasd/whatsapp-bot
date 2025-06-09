# app/session_manager.py

from typing import Dict

# Keyed by sender or conversationId
sessions: Dict[str, Dict] = {}

def get_session(user_id: str) -> Dict:
    if user_id not in sessions:
        sessions[user_id] = {"step": "choose_lang", "data": {}, "lang": None}
    return sessions[user_id]

def update_session(user_id: str, key: str, value):
    session = get_session(user_id)
    session[key] = value

def reset_session(user_id: str) -> Dict:
    if user_id in sessions:
        sessions[user_id] = {"step": "choose_lang", "data": {}, "lang": None}
    return sessions[user_id]

def clear_session(user_id: str):
    sessions.pop(user_id, None)

def get_lang(user_id: str) -> str:
    return sessions.get(user_id, {}).get("lang", "en")

def set_lang(user_id: str, lang: str):
    update_session(user_id, "lang", lang)

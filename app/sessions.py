# app/sessions.py

# Example: session state dictionary (in-memory)
sessions = {}

def get_session(conversation_id: str):
    return sessions.get(conversation_id)

def set_session(conversation_id: str, data: dict):
    sessions[conversation_id] = data

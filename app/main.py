# app/main.py
from fastapi import FastAPI
from app.handlers import process_message
from app.session_manager import sessions


app = FastAPI(title="WhatsApp Chatbot API")

@app.get("/")
async def health_check():
    return {"status": "OK", "message": "WhatsApp Chatbot API Running"}

# Example POST endpoint for webhook messages (UltraMsg)
@app.post("/webhook")
async def webhook_handler(payload: dict):
    response = await process_message(payload)
    return response

@app.get("/sessions")
def get_all_sessions():
    # ⚠️ Expose ONLY in dev/test environments
    return sessions

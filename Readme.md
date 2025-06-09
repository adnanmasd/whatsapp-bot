# README.md
# WhatsApp Chatbot using FastAPI + UltraMsg

## Features
- Multi-language (English, Arabic)
- Session-based state management
- Nested menus
- Form data collection
- UltraMsg API integration

## Run the Bot

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Use Ngrok to expose port 8000 to WhatsApp Webhook.

Run ngrok first. Then update the URL in Ultramsg webhook. Then just fire the server up and send messages
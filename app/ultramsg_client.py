# app/ultramsg_client.py
import os
from typing import Any, Dict
import httpx
from dotenv import load_dotenv

load_dotenv()  # Load env vars from .env file

ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")
ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
BASE_URL = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"

class UltraMsgClient:
    def __init__(self):
        if not ULTRAMSG_TOKEN or not ULTRAMSG_INSTANCE_ID:
            raise ValueError("ULTRAMSG_TOKEN and ULTRAMSG_INSTANCE_ID must be set in environment")

        self.token = ULTRAMSG_TOKEN
        self.base_url = BASE_URL
        self.client = httpx.AsyncClient()

    async def send_text(self, to: str, message: str, name:str ="") -> Dict[str, Any]:
        """
        Send a WhatsApp text message via UltraMsg API.
        :param to: recipient phone number with country code, e.g. '1234567890'
        :param message: text message content
        :return: UltraMsg API response as dict
        """

        async with httpx.AsyncClient() as client:
            payload = { "token": self.token, "to": to, "body": message}
            await client.post(self.base_url, data=payload)
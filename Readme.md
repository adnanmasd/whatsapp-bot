# README.md
# WhatsApp Chatbot using FastAPI + UltraMsg

## Features
- Multi-language (English, Arabic)
- Session-based state management
- Nested menus
- Form data collection
- UltraMsg API integration


## PIP Install

🧩 1. Download Python Installer
Go to the official Python site:

🔗 https://www.python.org/downloads/windows/

Click the latest Python 3.x.x under Windows installer (64-bit).

Save the .exe file (e.g., python-3.12.3-amd64.exe).

⚙️ 2. Run the Installer Properly
VERY IMPORTANT:
When running the installer:

✅ Check “Add Python to PATH” at the bottom of the installer window.

Then click:

➡️ Customize installation
➡️ Keep all defaults, click Next
➡️ On the next screen, make sure to check:

✅ "Install pip"

✅ "Add Python to environment variables"

✅ "Install for all users" (optional but recommended)

Then click Install.

🧪 3. Verify Installation
After install completes, open Command Prompt and run:
```bash
python --version
```

Then check for pip:
```bash
pip --version
```

You should see output like:
```bash
pip 23.x.x from C:\Python312\Lib\site-packages\pip (python 3.12)
```

If so, you're done. ✅

## Run the Bot

Navigate to project folder and run the following command to install all project dependencies.

```bash
pip install -r requirements.txt
```

Run the project locally:
```bash
uvicorn app.main:app --reload
```

For Testing you need nGrok.

Use Ngrok to expose port 8000 to WhatsApp Webhook.

Run ngrok first. Then update the URL in Ultramsg webhook. Then just fire the server up and send messages.

http://localhost:8000/sessions for sessions
http://127.0.0.1:4040/inspect/http for nGrok logs
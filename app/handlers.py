# app/handlers.py
import httpx
import asyncio
from app.ultramsg_client import UltraMsgClient
from app.session_manager import get_session,update_session,reset_session, get_lang, set_lang
from app.lang import get_text
from app.flow_manager import validate_input, get_prompt, get_next_step, is_form_step, get_form_field, get_actions

ultramsg_client = UltraMsgClient()

async def execute_actions(sender, lang, actions, session_data):
    for action in actions:
        action_type = action.get("type")

        if action_type == "post_data":
            url = action.get("url")
            method = action.get("method", "POST").upper()
            payload_map = action.get("payload_map", {})
            payload = {k: session_data.get(v, "") for k, v in payload_map.items()}

            async with httpx.AsyncClient() as client:
                try:
                    if method == "POST":
                        await client.post(url, json=payload, timeout=10)
                    elif method == "GET":
                        await client.get(url, params=payload, timeout=10)
                except Exception as e:
                    print(f"Error posting data: {e}")

        elif action_type == "send_message":
            message = action.get("message", {})
            text = message.get(lang, next(iter(message.values()), ""))
            if text:
                await ultramsg_client.send_text(sender, text)

async def process_message(payload: dict):
    """
    Process incoming webhook payload from UltraMsg,
    extract sender and message, then reply.
    """
    # Sample UltraMsg webhook payload structure example:
    # {
    #   "from": "1234567890",
    #   "body": "Hello chatbot"
    #   "id": "message_id"
    #   ... other fields
    # }
    #print(payload)

    if payload.get("fromMe", False):
        return {"status": "ignored", "reason": "outgoing message"}

    sender = payload["data"]["from"]
    mobile = sender.split("@")[0]
    name = payload["data"]["pushname"]
    text = payload["data"]["body"].strip()
    session = get_session(sender)
    step = session.get("step", "choose_lang")
    lang = get_lang(sender)

    # Restart flow on 'restart' or 'hi'
    if text.lower() in ["restart", "hi", "/start"]:
        if step != "choose_lang": reset_session(sender)
        reply = get_prompt("choose_lang", "en")
        await ultramsg_client.send_text(sender, reply)
        return {"status": "restart"}

    # Language selection step
    if step == "choose_lang":
        if text in ["1", "2"]:
            set_lang(sender, "en" if text == "1" else "ar")
            lang = get_lang(sender)
            next_step = "main_menu_" + lang
            update_session(sender, "step", next_step)
            reply = get_prompt(next_step, lang)
        else:
            reply = get_prompt(step, lang)
        await ultramsg_client.send_text(sender, reply)
        return {"status": "lang_selected"}
    
    # Handle form inputs
    if is_form_step(step):
        valid, error_msg = validate_input(step, text)
        if not valid:
            reply = (error_msg or "Invalid input.") + "\n" + get_prompt(step, lang)
            await ultramsg_client.send_text(sender, reply)
            return {"status": "validation_failed"}
        
        # Save the valid input in session
        session["data"][get_form_field(step)] = text
        field = get_form_field(step)
        
        # Save form data
        session["data"][field] = text
        next_step = get_next_step(step)
        update_session(sender, "step", next_step)
        update_session(sender, "data", session["data"])
        reply = get_prompt(next_step, lang)
        await ultramsg_client.send_text(sender, reply)
        # Run post-step actions async
        actions = get_actions(next_step)
        if actions:
            asyncio.create_task(execute_actions(sender, lang, actions, session["data"]))
        return {"status": "form_step"}

    # Handle regular menu navigation
    next_step = get_next_step(step, text.lower())
    if next_step:
        update_session(sender, "step", next_step)
        reply = get_prompt(next_step, lang)
    else:
        reply = get_prompt(step, lang)

    # Send reply
    await ultramsg_client.send_text(to=mobile, name=name, message=reply)

    actions = get_actions(next_step if next_step else step)
    if actions:
        asyncio.create_task(execute_actions(sender, lang, actions, session.get("data", {})))

    return {"status": "ok"}
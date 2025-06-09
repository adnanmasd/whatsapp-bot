import json
import re

with open("flows/menus.json", encoding="utf-8") as f:
    FLOWS = json.load(f)

def get_prompt(step, lang="en"):
    step_data = FLOWS.get(step, {})
    return step_data.get("prompt", {}).get(lang, "[No prompt available]")

def get_next_step(step, user_input=None):
    step_data = FLOWS.get(step, {})
    next_map = step_data.get("next", {})
    if user_input is None:
        # For form steps, next is string
        return next_map if isinstance(next_map, str) else None
    return next_map.get(user_input, next_map.get("*", None))

def is_form_step(step):
    step_data = FLOWS.get(step, {})
    return "form_field" in step_data

def get_form_field(step):
    step_data = FLOWS.get(step, {})
    return step_data.get("form_field")

def get_actions(step):
    step_data = FLOWS.get(step, {})
    return step_data.get("actions", [])

def validate_input(step, user_input):
    step_data = FLOWS.get(step, {})
    validation = step_data.get("validation")
    if not validation:
        return True, None

    vtype = validation.get("type")

    if vtype == "email":
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, user_input):
            return False, "Invalid email format."

    elif vtype == "phone":
        pattern = r"^\+?\d{7,15}$"
        if not re.match(pattern, user_input):
            return False, "Invalid phone number format."

    elif vtype == "numeric":
        if not user_input.isdigit():
            return False, "Input must be numeric."

    elif vtype == "regex":
        pattern = validation.get("pattern")
        if pattern and not re.match(pattern, user_input):
            return False, validation.get("error_msg", "Invalid input.")

    # Add more types if needed

    return True, None
import streamlit as st
import json
import os
from datetime import datetime, time
import pandas as pd

CHECKLIST_FILE = "trading_checklist.json"

DEFAULT_ITEMS = [
    "Are market conditions (volatility, trend) right for this trade?",
    "Are there major news events that may occur during the trade?",
    "Correct entry point based on strategy?",
    "Is the stop loss reasonable for the potential reward?",
    "How am I getting out of this trade? (Describe)",
    "Is my position size correct?",
    "Am I violating any of my Trading Plan rules?",
    "Am I allowed to trade? (Not on a forced break due to recent losses)",
    "Am I placing this order in the correct hours/my established trading time?",
    "Is it within my max number of positions I can hold at one time?",
    "Is it within my leverage tolerance?",
    "Did I find this trade through the proper means? (Not a 'tip' but from my own research)",
    "What should I remember during the trade? (Key point you've struggled with recently)",
    "Am I in the right mind frame for this trade?",
    "My expectations are realistic",
    "I have a probability-tested edge",
    "Trading aligns with my 'ideal self'",
    "No one is influencing me",
    "My entry criteria is clear, now I wait",
    "I am self-aware of my impulses",
    "Sleep was great, exercise was great",
    "My brain and belly have been fed",
    "Trades must meet my criteria",
    "I completely accept my defined risk",
    "Position size is in-line with my process",
    "Good habits are forming in my trading",
    "I am calm, relaxed, and focused"
]

def load_checklist():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r") as f:
            return json.load(f)
    else:
        # Build checklist as list of dicts with position
        return {
            "items": [
                {"position": i+1, "text": text}
                for i, text in enumerate(DEFAULT_ITEMS)
            ],
            "checked": []
        }

def save_checklist(data):
    with open(CHECKLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)

def renumber(items):
    """Ensures position is always sequential."""
    for idx, item in enumerate(items):
        item["position"] = idx + 1
    return items

def ensure_positions(items):
    # Add position if missing, then re-number all
    for idx, item in enumerate(items):
        if "position" not in item:
            item["position"] = idx + 1
    return renumber(items)
def load_checklist():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r") as f:
            return json.load(f)
    else:
        # Build checklist as list of dicts with position
        return {
            "items": [
                {"position": i+1, "text": text}
                for i, text in enumerate(DEFAULT_ITEMS)
            ],
            "checked": []
        }

def migrate_items(items):
    """Convert a list of strings to a list of dicts with 'text' and 'position'."""
    if not items:
        return []
    if isinstance(items[0], dict):
        # Already migrated
        return items
    # Legacy list of strings; migrate!
    return [{"position": i + 1, "text": txt} for i, txt in enumerate(items)]

# ...rest of your code...


st.title("📝 Daily Trading Checklist")
data = load_checklist()
# MIGRATE legacy: If list of strings, convert to list of dicts
items = migrate_items(data.get("items", []))
items = ensure_positions(items)
data["items"] = items


# Now sort using the fixed key
items = sorted(items, key=lambda x: x.get("position", 9999))
checked = set(data.get("checked", []))

# 1. Add new checklist item
with st.form(key="add_item_form"):
    new_item = st.text_input("Add a new checklist item", "")
    submitted = st.form

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

st.title("📝 Daily Trading Checklist")

data = load_checklist()
items = sorted(data.get("items", []), key=lambda x: x["position"])
checked = set(data.get("checked", []))

# 1. Add new checklist item
with st.form(key="add_item_form"):
    new_item = st.text_input("Add a new checklist item", "")
    submitted = st.form_submit_button("Add")
    if submitted and new_item.strip():
        items.append({"position": len(items)+1, "text": new_item.strip()})
        items = renumber(items)
        st.success(f"Added: {new_item.strip()}")

# 2. Move checklist items (drag-and-drop)
st.write("### Reorder your checklist")
df = pd.DataFrame([{"#": item["position"], "Checklist": item["text"]} for item in items])
edited_df = st.data_editor(
    df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "#": st.column_config.Column(
            "#", required=True, width="small"
        ),
        "Checklist": st.column_config.Column(
            "Checklist Item",
            required=True,
            width="large"
        )
    },
    num_rows="dynamic",
    key="editor",
    disabled=["#", "Checklist"] # disables text editing, allows moving
)

# Save reordering
if st.button("Save New Order"):
    # Use row order in edited_df to update items
    new_order_texts = edited_df["Checklist"].tolist()
    items_dict = {item["text"]: item for item in items}
    items = [{"position": i+1, "text": txt} for i, txt in enumerate(new_order_texts) if txt in items_dict]
    items = renumber(items)
    data["items"] = items
    save_checklist(data)
    st.success("Checklist order saved!")

# 3. Checklist with checkboxes and numbering
st.write("### Daily checklist (tick as you go)")
checked_today = []
for item in items:
    label = f"{item['position']}. {item['text']}"
    checked_state = st.checkbox(label, key=f"item_{item['position']}", value=(item["text"] in checked))
    if checked_state:
        checked_today.append(item["text"])

# 4. Remove checklist item
st.write("### Remove Items")
to_delete = st.multiselect("Select checklist items to remove", options=[item["text"] for item in items])
if st.button("Delete selected"):
    items = [item for item in items if item["text"] not in to_delete]
    items = renumber(items)
    checked = [item for item in checked if item not in to_delete]
    st.success(f"Deleted: {', '.join(to_delete)}")

# 5. Save checklist state (checked/unchecked and order)
data = {"items": items, "checked": checked_today}
save_checklist(data)

# 6. Reminder: Must complete before 9 am
now = datetime.now()
cutoff = time(9, 0)
if now.time() < cutoff:
    st.info(f"⏰ Please complete this checklist before **9:00 am**! ({now.strftime('%H:%M')})")
else:
    if len(checked_today) == len(items) and items:
        st.success("✅ All checklist items completed for today!")
    else:
        st.warning("⚠️ You haven't completed all checklist items today.")

st.write("---")
st.caption("Tip: Drag to reorder, add/remove items as needed. Numbers update automatically to reflect order.")

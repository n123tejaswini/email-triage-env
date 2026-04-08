# env/graders.py
from typing import Dict, Any

def grade_easy(action_label: str, correct_label: str) -> float:
    """Binary: right or wrong."""
    return 1.0 if action_label.lower() == correct_label.lower() else 0.0


def grade_medium(action_label: str, action_priority: int,
                 correct_label: str, correct_priority: int) -> tuple[float, Dict]:
    """Partial credit: label (60%) + priority closeness (40%)."""
    label_score = 1.0 if action_label.lower() == correct_label.lower() else 0.0

    # Priority: full credit if exact, partial if ±1, zero if ±2+
    priority_diff = abs(action_priority - correct_priority)
    if priority_diff == 0:
        priority_score = 1.0
    elif priority_diff == 1:
        priority_score = 0.5
    else:
        priority_score = 0.0

    total = (label_score * 0.6) + (priority_score * 0.4)
    breakdown = {"label": label_score, "priority": priority_score}
    return round(total, 2), breakdown


def grade_hard(action: Dict, email: Dict) -> tuple[float, Dict]:
    """Three components: label (40%) + priority (30%) + reply (30%)."""
    action_label = action.get("label", "").lower()
    action_priority = action.get("priority", 3)
    reply_draft = action.get("reply_draft", "") or ""

    correct_label = email["correct_label"]
    correct_priority = email["correct_priority"]
    requires_reply = email.get("requires_reply", False)
    ideal_keywords = email.get("ideal_reply_keywords", [])

    # Label score
    label_score = 1.0 if action_label == correct_label else 0.0

    # Priority score
    priority_diff = abs(action_priority - correct_priority)
    priority_score = max(0.0, 1.0 - (priority_diff * 0.5))

    # Reply score
    if not requires_reply:
        reply_score = 1.0  # Full credit — no reply needed
    elif not reply_draft:
        reply_score = 0.0  # Reply needed but not given
    else:
        # Check how many ideal keywords appear
        hits = sum(1 for kw in ideal_keywords
                   if kw.lower() in reply_draft.lower())
        reply_score = min(hits / max(len(ideal_keywords), 1), 1.0)

    total = (label_score * 0.4) + (priority_score * 0.3) + (reply_score * 0.3)
    breakdown = {
        "label": label_score,
        "priority": priority_score,
        "reply": reply_score
    }
    return round(total, 2), breakdown
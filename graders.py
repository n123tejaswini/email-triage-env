# env/graders.py
from typing import Dict

def _clamp(score: float) -> float:
    """Ensure score is strictly between 0 and 1 (exclusive)."""
    return min(max(round(score, 4), 0.001), 0.999)


def grade_easy(action_label: str, correct_label: str) -> tuple[float, Dict]:
    """Binary: right or wrong."""
    score = 0.999 if action_label.lower() == correct_label.lower() else 0.001
    return score, {"label": score}


def grade_medium(action_label: str, action_priority: int,
                 correct_label: str, correct_priority: int) -> tuple[float, Dict]:
    """Partial credit: label (60%) + priority closeness (40%)."""
    label_score = 0.999 if action_label.lower() == correct_label.lower() else 0.001

    priority_diff = abs(action_priority - correct_priority)
    if priority_diff == 0:
        priority_score = 0.999
    elif priority_diff == 1:
        priority_score = 0.5
    else:
        priority_score = 0.001

    total = _clamp((label_score * 0.6) + (priority_score * 0.4))
    breakdown = {"label": label_score, "priority": priority_score}
    return total, breakdown


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
    label_score = 0.999 if action_label == correct_label else 0.001

    # Priority score
    priority_diff = abs(action_priority - correct_priority)
    priority_score = _clamp(0.999 - (priority_diff * 0.499))

    # Reply score
    if not requires_reply:
        reply_score = 0.999
    elif not reply_draft:
        reply_score = 0.001
    else:
        hits = sum(1 for kw in ideal_keywords
                   if kw.lower() in reply_draft.lower())
        raw = hits / max(len(ideal_keywords), 1)
        reply_score = _clamp(raw * 0.998 + 0.001)  # maps [0,1] to (0.001, 0.999)

    total = _clamp((label_score * 0.4) + (priority_score * 0.3) + (reply_score * 0.3))

    breakdown = {
        "label": label_score,
        "priority": priority_score,
        "reply": reply_score
    }
    return total, breakdown

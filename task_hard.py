# tasks/task_hard.py
TASK_ID = "full_triage"
INSTRUCTIONS = (
    "For each email: (1) label as 'spam', 'phishing', 'urgent', 'normal', or 'low'. "
    "(2) assign priority 1-3. "
    "(3) for urgent/normal emails, provide a brief professional reply_draft. "
    "Partial credit for each component."
)
MAX_STEPS = 6

EMAILS = [
    {
        "id": 1,
        "from": "security@paypa1.com",   # Note: fake domain
        "subject": "Your account has been suspended",
        "body": "Click here to verify your identity or your account will be closed permanently.",
        "correct_label": "phishing",
        "correct_priority": 1,
        "requires_reply": False
    },
    {
        "id": 2,
        "from": "cto@yourcompany.com",
        "subject": "Architecture review tomorrow 10am",
        "body": "I need you to present the new API design tomorrow. Please confirm.",
        "correct_label": "urgent",
        "correct_priority": 1,
        "requires_reply": True,
        "ideal_reply_keywords": ["confirm", "tomorrow", "10am", "ready", "present"]
    },
    {
        "id": 3,
        "from": "offers@random-store.net",
        "subject": "Flash sale 90% off everything!",
        "body": "One day only. Shop now before it's too late!",
        "correct_label": "spam",
        "correct_priority": 3,
        "requires_reply": False
    },
    {
        "id": 4,
        "from": "legal@yourcompany.com",
        "subject": "NDA needs signature by EOD",
        "body": "Please sign the attached NDA and return it before 5pm today.",
        "correct_label": "urgent",
        "correct_priority": 1,
        "requires_reply": True,
        "ideal_reply_keywords": ["sign", "today", "attached", "confirm", "return"]
    },
    {
        "id": 5,
        "from": "dev@yourcompany.com",
        "subject": "PR review when you get a chance",
        "body": "No rush, but could you review PR #142 this week?",
        "correct_label": "normal",
        "correct_priority": 2,
        "requires_reply": True,
        "ideal_reply_keywords": ["review", "week", "PR", "look", "check"]
    },
    {
        "id": 6,
        "from": "noreply@fakemicrosoft-support.com",
        "subject": "Windows license expiring - act now",
        "body": "Your Windows license has expired. Pay $49 to reactivate immediately.",
        "correct_label": "phishing",
        "correct_priority": 1,
        "requires_reply": False
    },
]
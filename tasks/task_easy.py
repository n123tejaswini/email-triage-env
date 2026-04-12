# tasks/task_easy.py
TASK_ID = "spam_detection"
INSTRUCTIONS = "Label each email as 'spam' or 'not_spam'."
MAX_STEPS = 5

EMAILS = [
    {
        "id": 1,
        "from": "noreply@lottery-winner.biz",
        "subject": "You won $1,000,000!!!",
        "body": "Click here to claim your prize now. Limited time offer!",
        "correct_label": "spam"
    },
    {
        "id": 2,
        "from": "manager@yourcompany.com",
        "subject": "Q3 Report Review",
        "body": "Please review the attached Q3 report before Thursday's meeting.",
        "correct_label": "not_spam"
    },
    {
        "id": 3,
        "from": "deals@shop-cheap-pills.ru",
        "subject": "Buy cheap meds online no prescription",
        "body": "Best prices guaranteed. Ships worldwide.",
        "correct_label": "spam"
    },
    {
        "id": 4,
        "from": "hr@yourcompany.com",
        "subject": "Updated Leave Policy",
        "body": "Please read the updated leave policy attached to this email.",
        "correct_label": "not_spam"
    },
    {
        "id": 5,
        "from": "friend@gmail.com",
        "subject": "Lunch tomorrow?",
        "body": "Hey, are you free for lunch tomorrow at 1pm?",
        "correct_label": "not_spam"
    },
]
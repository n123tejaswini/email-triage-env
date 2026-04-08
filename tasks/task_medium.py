# tasks/task_medium.py
TASK_ID = "priority_sorting"
INSTRUCTIONS = (
    "Label each email as 'urgent', 'normal', or 'low'. "
    "Also assign a priority number 1 (highest) to 3 (lowest). "
    "Partial credit given for close answers."
)
MAX_STEPS = 8

EMAILS = [
    {
        "id": 1,
        "from": "ceo@yourcompany.com",
        "subject": "URGENT: Server is down",
        "body": "Production is completely down. All hands needed NOW.",
        "correct_label": "urgent",
        "correct_priority": 1
    },
    {
        "id": 2,
        "from": "newsletter@medium.com",
        "subject": "Your weekly digest",
        "body": "Here are the top stories this week...",
        "correct_label": "low",
        "correct_priority": 3
    },
    {
        "id": 3,
        "from": "client@bigcorp.com",
        "subject": "Contract renewal - deadline Friday",
        "body": "We need the signed contract by end of week or we'll go elsewhere.",
        "correct_label": "urgent",
        "correct_priority": 1
    },
    {
        "id": 4,
        "from": "it@yourcompany.com",
        "subject": "Scheduled maintenance Sunday 2am",
        "body": "Reminder: planned downtime this Sunday 2-4am.",
        "correct_label": "normal",
        "correct_priority": 2
    },
    {
        "id": 5,
        "from": "team@yourcompany.com",
        "subject": "Team lunch Friday",
        "body": "We're ordering from the Italian place. Reply with your order.",
        "correct_label": "low",
        "correct_priority": 3
    },
    {
        "id": 6,
        "from": "support@stripe.com",
        "subject": "Payment failed for your subscription",
        "body": "Your payment method was declined. Update it within 24 hours.",
        "correct_label": "urgent",
        "correct_priority": 1
    },
    {
        "id": 7,
        "from": "colleague@yourcompany.com",
        "subject": "Slides for next week's meeting",
        "body": "Here are the slides I'll use next Tuesday. Feedback welcome.",
        "correct_label": "normal",
        "correct_priority": 2
    },
    {
        "id": 8,
        "from": "noreply@linkedin.com",
        "subject": "You have 3 new connection requests",
        "body": "John, Sarah, and Mike want to connect with you.",
        "correct_label": "low",
        "correct_priority": 3
    },
]
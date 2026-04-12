# inference.py
import os
import requests
from typing import List, Optional
from openai import OpenAI

# ── Required env vars ──────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN     = os.getenv("HF_TOKEN", "")
ENV_URL      = os.getenv("ENV_URL", "http://localhost:7860")

TASKS = ["spam_detection", "priority_sorting", "full_triage"]
MAX_STEPS = 10
SUCCESS_THRESHOLD = 0.5

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

# ── Clamp helper ───────────────────────────────────────────────
def clamp(value: float) -> float:
    """Ensure value is strictly between 0 and 1 (exclusive)."""
    return min(max(round(float(value), 4), 0.001), 0.999)

# ── Mandatory log functions ────────────────────────────────────
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    err = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.4f} "
          f"done={str(done).lower()} error={err}", flush=True)

def log_end(success, steps, score, rewards):
    rstr = ",".join(f"{r:.4f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} "
          f"score={score:.4f} rewards={rstr}", flush=True)

# ── LLM decision function ──────────────────────────────────────
def ask_llm(task_id: str, observation: dict) -> dict:
    email = observation.get("current_email", {})
    instructions = observation.get("instructions", "")

    system = (
        "You are an expert email triage assistant. "
        "Read each email carefully and respond with a JSON action. "
        "For task spam_detection: {\"label\": \"spam\" or \"not_spam\"} "
        "For task priority_sorting: {\"label\": \"urgent\"|\"normal\"|\"low\", \"priority\": 1|2|3} "
        "For task full_triage: {\"label\": \"spam\"|\"phishing\"|\"urgent\"|\"normal\"|\"low\", "
        "\"priority\": 1|2|3, \"reply_draft\": \"<reply text or null>\"} "
        "Reply ONLY with valid JSON, no explanation."
    )

    user = (
        f"Task: {task_id}\n"
        f"Instructions: {instructions}\n"
        f"Email from: {email.get('from', '')}\n"
        f"Subject: {email.get('subject', '')}\n"
        f"Body: {email.get('body', '')}\n\n"
        f"Respond with your JSON action."
    )

    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            temperature=0.1,
            max_tokens=200,
        )
        import json
        text = resp.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"[DEBUG] LLM error: {e}", flush=True)
        return {"label": "normal", "priority": 2}

# ── Run one task episode ───────────────────────────────────────
def run_task(task_id: str):
    rewards: List[float] = []
    steps_taken = 0
    score = 0.001
    success = False

    log_start(task=task_id, env="email-triage-env", model=MODEL_NAME)

    try:
        # Reset
        obs_resp = requests.post(f"{ENV_URL}/reset?task_id={task_id}", timeout=15)
        observation = obs_resp.json()

        for step in range(1, MAX_STEPS + 1):
            if observation.get("emails_remaining", 0) == 0:
                break

            # Get LLM action
            action_dict = ask_llm(task_id, observation)
            action_str = str(action_dict)

            # Step the environment
            step_resp = requests.post(
                f"{ENV_URL}/step?task_id={task_id}",
                json=action_dict,
                timeout=15
            )
            result = step_resp.json()

            # Clamp reward strictly between 0 and 1
            raw_reward = result.get("reward", 0.001)
            reward = clamp(raw_reward)

            done  = result.get("done", False)
            error = None

            rewards.append(reward)
            steps_taken = step
            observation = result.get("observation", observation)

            log_step(step=step, action=action_str, reward=reward,
                     done=done, error=error)

            if done:
                break

        # Clamp all rewards and compute score
        rewards = [clamp(r) for r in rewards]
        score = sum(rewards) / len(rewards) if rewards else 0.001
        score = clamp(score)
        success = score >= SUCCESS_THRESHOLD

    except Exception as e:
        print(f"[DEBUG] Task error: {e}", flush=True)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return score

# ── Main: run all 3 tasks ──────────────────────────────────────
if __name__ == "__main__":
    print(f"[DEBUG] Running against {ENV_URL} with model {MODEL_NAME}", flush=True)
    for task in TASKS:
        run_task(task)
        print("---", flush=True)

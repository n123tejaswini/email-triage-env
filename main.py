# main.py
from fastapi import FastAPI, HTTPException
from models.schemas import Action, StepResult, Observation, EnvState
from env.environment import EmailTriageEnv
from typing import Dict
import uvicorn

app = FastAPI(title="Email Triage OpenEnv", version="1.0.0")

# One env instance per task_id stored in memory
# (For production, use session IDs — this is fine for hackathon)
_envs: Dict[str, EmailTriageEnv] = {}

def get_env(task_id: str = "spam_detection") -> EmailTriageEnv:
    if task_id not in _envs:
        _envs[task_id] = EmailTriageEnv(task_id=task_id)
    return _envs[task_id]


@app.post("/reset", response_model=Observation)
def reset(task_id: str = "spam_detection"):
    env = get_env(task_id)
    return env.reset()


@app.post("/step", response_model=StepResult)
def step(action: Action, task_id: str = "spam_detection"):
    env = get_env(task_id)
    try:
        return env.step(action)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state", response_model=EnvState)
def state(task_id: str = "spam_detection"):
    env = get_env(task_id)
    return env.state()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {"id": "spam_detection", "difficulty": "easy"},
            {"id": "priority_sorting", "difficulty": "medium"},
            {"id": "full_triage", "difficulty": "hard"},
        ]
    }
def root():
    return {
        "name": "Email Triage OpenEnv",
        "version": "1.0.0",
        "docs": "/docs",
        "tasks": "/tasks",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=False)
    
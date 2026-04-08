# models/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

# What the agent SEES each step
class Observation(BaseModel):
    task_id: str
    step: int
    current_email: Dict[str, Any]      # The email to triage
    emails_remaining: int
    instructions: str                   # What the agent is asked to do

# What the agent DOES each step
class Action(BaseModel):
    label: str          # e.g. "spam", "urgent", "normal", "phishing"
    priority: Optional[int] = None      # 1-5 for medium/hard tasks
    reply_draft: Optional[str] = None   # For hard task only

# The reward returned after each step
class Reward(BaseModel):
    value: float = Field(ge=0.0, le=1.0)
    breakdown: Dict[str, float] = {}    # e.g. {"label": 0.5, "priority": 0.3}
    feedback: str = ""

# Full response from step()
class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any] = {}

# Full response from state()
class EnvState(BaseModel):
    task_id: str
    step: int
    total_steps: int
    cumulative_reward: float
    done: bool
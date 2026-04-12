# models/schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any, Dict

# What the agent SEES each step
class Observation(BaseModel):
    task_id: str
    step: int
    current_email: Dict[str, Any]
    emails_remaining: int
    instructions: str

# What the agent DOES each step
class Action(BaseModel):
    label: str
    priority: Optional[int] = None
    reply_draft: Optional[str] = None

# The reward returned after each step
class Reward(BaseModel):
    value: float = Field(gt=0.0, lt=1.0)  # strictly exclusive
    breakdown: Dict[str, float] = {}
    feedback: str = ""

# Full response from step()
class StepResult(BaseModel):
    observation: Observation
    reward: float = Field(gt=0.0, lt=1.0)  # strictly exclusive
    done: bool
    info: Dict[str, Any] = {}

    @field_validator('reward')
    @classmethod
    def reward_must_be_exclusive(cls, v):
        """Clamp reward to strictly (0, 1) exclusive."""
        return min(max(round(v, 4), 0.001), 0.999)

# Full response from state()
class EnvState(BaseModel):
    task_id: str
    step: int
    total_steps: int
    cumulative_reward: float
    done: bool
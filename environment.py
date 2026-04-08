# env/environment.py
from typing import Optional, Dict, Any
from models.schemas import Observation, Action, StepResult, EnvState
from tasks import task_easy, task_medium, task_hard
from env.graders import grade_easy, grade_medium, grade_hard

TASK_MAP = {
    "spam_detection": task_easy,
    "priority_sorting": task_medium,
    "full_triage": task_hard,
}

class EmailTriageEnv:
    def __init__(self, task_id: str = "spam_detection"):
        if task_id not in TASK_MAP:
            raise ValueError(f"Unknown task: {task_id}. Choose from {list(TASK_MAP)}")
        self.task_id = task_id
        self.task_module = TASK_MAP[task_id]
        self._step = 0
        self._cumulative_reward = 0.0
        self._done = False
        self._emails = []
        self._current_index = 0

    def reset(self) -> Observation:
        self._step = 0
        self._cumulative_reward = 0.0
        self._done = False
        self._emails = self.task_module.EMAILS.copy()
        self._current_index = 0
        return self._make_observation()

    def step(self, action: Action) -> StepResult:
        if self._done:
            raise RuntimeError("Episode is done. Call reset() first.")

        email = self._emails[self._current_index]

        # Grade the action
        reward, breakdown = self._grade(action, email)
        self._cumulative_reward += reward
        self._step += 1
        self._current_index += 1

        # Check if episode is over
        if self._current_index >= len(self._emails):
            self._done = True

        obs = self._make_observation() if not self._done else self._final_observation()

        return StepResult(
            observation=obs,
            reward=reward,
            done=self._done,
            info={"breakdown": breakdown, "correct_label": email.get("correct_label")}
        )

    def state(self) -> EnvState:
        return EnvState(
            task_id=self.task_id,
            step=self._step,
            total_steps=len(self._emails),
            cumulative_reward=self._cumulative_reward,
            done=self._done
        )

    def _make_observation(self) -> Observation:
        if self._current_index >= len(self._emails):
            return self._final_observation()
        email = self._emails[self._current_index]
        return Observation(
            task_id=self.task_id,
            step=self._step,
            current_email=email,
            emails_remaining=len(self._emails) - self._current_index,
            instructions=self.task_module.INSTRUCTIONS
        )

    def _final_observation(self) -> Observation:
        return Observation(
            task_id=self.task_id,
            step=self._step,
            current_email={},
            emails_remaining=0,
            instructions="Episode complete."
        )

    def _grade(self, action: Action, email: Dict) -> tuple[float, Dict]:
        if self.task_id == "spam_detection":
            score = grade_easy(action.label, email["correct_label"])
            return score, {"label": score}
        elif self.task_id == "priority_sorting":
            return grade_medium(
                action.label, action.priority or 2,
                email["correct_label"], email["correct_priority"]
            )
        else:  # full_triage
            return grade_hard(action.model_dump(), email)
from langchain_core.messages.base import BaseMessage
from pydantic import BaseModel,Field
from typing import Optional, Dict, Any, Union
from uuid import uuid4

class AgentState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    consecutive_failures: int = 0
    # --- FIX: Allow result to be None and default to None ---
    result: Optional[str] = None
    error: Optional[str] = None
    agent_data: 'AgentData' = None
    messages: list[BaseMessage] =  Field(default_factory=list)
    previous_observation: Optional[str] = None
    query:Optional[str]=None

    def is_done(self):
        return self.agent_data is not None and self.agent_data.action and self.agent_data.action.name == 'Done Tool'

    def init_state(self, query: str, messages: list[BaseMessage]):
        """Initializes the state for a new invocation."""
        self.query = query
        self.messages = messages
        self.consecutive_failures = 0
        self.result = None
        self.error = None
        self.previous_observation = "No Action"

    def update_state(self, agent_data: 'AgentData' = None, observation: str = None, result: str = None, messages: list[BaseMessage] = None):
        if result is not None:
            self.result = result
        if observation is not None:
            self.previous_observation = observation
        if agent_data is not None:
            self.agent_data = agent_data
        if messages:
            self.messages.extend(messages)

class AgentStep(BaseModel):
    step_number: int=0
    max_steps: int

    def is_last_step(self):
        return self.step_number >= self.max_steps-1

    def increment_step(self):
        self.step_number += 1

class AgentResult(BaseModel):
    is_done:bool|None=False
    content:str|None=None
    error:str|None=None

class Action(BaseModel):
    name:str
    params: Union[Dict[str, Any], str, None] = {}

class AgentData(BaseModel):
    evaluate: Optional[str]=None
    memory: Optional[str]=None
    thought: Optional[str]=None
    action: Optional[Action]=None

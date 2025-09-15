from pydantic import BaseModel,Field
from typing import Optional
    
class AgentResult(BaseModel):
    content:str|None=None
    error:str|None=None

class Action(BaseModel):
    name:str
    params: dict=Field(default_factory=dict)

class AgentData(BaseModel):
    evaluate: str
    memory: str
    plan: str
    thought: str
    action: Action

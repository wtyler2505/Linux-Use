from langchain_core.messages.base import BaseMessage
from linux_use.agent.views import AgentData
from typing import TypedDict,Annotated
from operator import add

class AgentState(TypedDict):
    steps: int
    max_steps: int
    input:str
    output:str
    error:str
    agent_data:AgentData|None
    consecutive_failures: int
    max_consecutive_failures: int
    messages:Annotated[list[BaseMessage],add]
    previous_observation: str|None
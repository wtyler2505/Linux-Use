"""Agent Manager Service"""

import asyncio
from typing import Optional, Callable
from dataclasses import dataclass
import time

@dataclass
class AgentStatus:
    """Agent status information"""
    state: str  # 'idle', 'active', 'paused', 'error'
    current_task: str
    steps_completed: int
    start_time: float
    
class AgentManager:
    """Manage Linux-Use agent lifecycle"""
    
    def __init__(self, status_callback: Optional[Callable] = None):
        self.status_callback = status_callback
        self.agent = None
        self.status = AgentStatus(
            state='idle',
            current_task='',
            steps_completed=0,
            start_time=time.time()
        )
        self.is_running = False
    
    def _update_status(self, state: str, task: str = ""):
        """Update agent status"""
        self.status.state = state
        if task:
            self.status.current_task = task
        
        if self.status_callback:
            self.status_callback(self.status)
    
    async def initialize_agent(self, config: dict) -> bool:
        """Initialize the Linux-Use agent"""
        try:
            self._update_status('initializing', 'Loading agent...')
            
            # Import agent (lazy loading)
            from linux_use.agent.service import Agent
            from linux_use.agent.desktop.views import Browser
            from langchain_anthropic import ChatAnthropic
            
            # Create LLM
            api_key = config.get('api_key')
            if not api_key:
                raise ValueError("API key required")
            
            llm = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                api_key=api_key,
                timeout=60
            )
            
            # Create agent
            self.agent = Agent(
                instructions=config.get('instructions', ["You are a helpful Linux automation assistant"]),
                browser=Browser.FIREFOX,
                llm=llm,
                max_steps=config.get('max_steps', 25),
                max_consecutive_failures=config.get('max_failures', 3),
                use_vision=config.get('use_vision', False),
                auto_minimize=config.get('auto_minimize', False)
            )
            
            self._update_status('idle', 'Agent ready')
            return True
            
        except Exception as e:
            self._update_status('error', f'Initialization failed: {e}')
            return False
    
    async def execute_task(self, task: str) -> dict:
        """Execute an automation task"""
        if not self.agent:
            return {'success': False, 'error': 'Agent not initialized'}
        
        try:
            self._update_status('active', task)
            self.is_running = True
            
            # Execute task
            result = await asyncio.to_thread(self.agent.print_response, task)
            
            self.status.steps_completed += 1
            self._update_status('idle', 'Task completed')
            self.is_running = False
            
            return {'success': True, 'result': result}
            
        except Exception as e:
            self._update_status('error', f'Task failed: {e}')
            self.is_running = False
            return {'success': False, 'error': str(e)}
    
    def pause_agent(self):
        """Pause agent execution"""
        if self.is_running:
            self._update_status('paused', 'Paused by user')
    
    def stop_agent(self):
        """Stop agent execution"""
        self.is_running = False
        self._update_status('idle', 'Stopped by user')
    
    def get_status(self) -> AgentStatus:
        """Get current agent status"""
        return self.status

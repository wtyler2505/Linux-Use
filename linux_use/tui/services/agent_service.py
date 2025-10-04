"""Agent service for TUI integration"""

import asyncio
import os
from typing import Optional, Callable
from pathlib import Path

# Agent imports
from linux_use.agent.service import LinuxAgent


class AgentService:
    """Manages the Linux-Use automation agent"""
    
    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None):
        self.agent: Optional[LinuxAgent] = None
        self.is_running = False
        self.progress_callback = progress_callback
        self.current_task: Optional[str] = None
        self.task_result: Optional[str] = None
    
    def _log(self, message: str):
        """Log progress"""
        if self.progress_callback:
            self.progress_callback(message)
    
    async def initialize_agent(self) -> bool:
        """Initialize the agent with API key"""
        try:
            # Check for API key
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            if not api_key:
                self._log("❌ No ANTHROPIC_API_KEY found in environment")
                self._log("Please set it in Configuration screen")
                return False
            
            self._log("🚀 Initializing Linux-Use agent...")
            
            # Create agent instance
            self.agent = LinuxAgent()
            
            self._log("✅ Agent initialized successfully")
            self._log(f"🤖 Model: Claude (Sonnet)")
            self._log(f"🖥️  Desktop automation ready")
            
            return True
            
        except Exception as e:
            self._log(f"❌ Agent initialization failed: {e}")
            return False
    
    async def execute_task(self, task: str) -> bool:
        """Execute an automation task"""
        if not self.agent:
            success = await self.initialize_agent()
            if not success:
                return False
        
        self.current_task = task
        self.is_running = True
        self.task_result = None
        
        try:
            self._log(f"▶ Executing task: {task}")
            self._log("=" * 50)
            
            # Run the agent
            # Note: This is simplified - actual execution would use the agent's run method
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                self.agent.run,
                task
            )
            
            self.task_result = str(result)
            self._log("=" * 50)
            self._log(f"✅ Task completed")
            self._log(f"Result: {self.task_result[:200]}")
            
            return True
            
        except Exception as e:
            self._log(f"❌ Task execution failed: {e}")
            self.task_result = f"Error: {e}"
            return False
        
        finally:
            self.is_running = False
    
    async def pause_agent(self):
        """Pause the running agent"""
        if self.is_running:
            self._log("⏸ Agent paused")
            self.is_running = False
    
    async def stop_agent(self):
        """Stop the agent"""
        self._log("■ Agent stopped")
        self.is_running = False
        self.current_task = None
    
    def get_status(self) -> dict:
        """Get current agent status"""
        return {
            "initialized": self.agent is not None,
            "running": self.is_running,
            "current_task": self.current_task,
            "result": self.task_result
        }
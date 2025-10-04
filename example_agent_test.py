"""Example: Test agent integration with TUI"""

import asyncio
import os
from linux_use.tui.services.agent_service import AgentService


async def test_agent():
    """Test agent service"""
    
    def progress_callback(msg: str):
        print(f"[AGENT] {msg}")
    
    # Create agent service
    agent_service = AgentService(progress_callback=progress_callback)
    
    # Initialize
    print("Initializing agent...")
    success = await agent_service.initialize_agent()
    
    if success:
        print("\n✅ Agent initialized successfully!")
        print(f"Status: {agent_service.get_status()}")
        
        # Execute a simple task
        print("\nExecuting test task...")
        await agent_service.execute_task("Open Firefox browser")
        
    else:
        print("\n❌ Agent initialization failed")
        print("Make sure ANTHROPIC_API_KEY is set in /app/.env")


if __name__ == "__main__":
    # Ensure API key is set
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("⚠️  Warning: ANTHROPIC_API_KEY not found in environment")
        print("Loading from /app/.env if available...")
        
        env_file = "/app/.env"
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.startswith('ANTHROPIC_API_KEY='):
                        key = line.split('=', 1)[1].strip()
                        os.environ['ANTHROPIC_API_KEY'] = key
                        print("✅ API key loaded from .env")
                        break
    
    # Run test
    asyncio.run(test_agent())
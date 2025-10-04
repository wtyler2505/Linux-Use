#!/usr/bin/env python3
"""
Linux-Use Agent - Example Usage
Demonstrates various automation capabilities
"""

import os
from langchain_anthropic import ChatAnthropic
from linux_use.agent.service import Agent
from linux_use.agent.desktop.views import Browser

def load_env():
    """Load environment variables from .env file"""
    try:
        with open('/app/.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        print("⚠️ .env file not found. Make sure ANTHROPIC_API_KEY is set.")

def create_agent():
    """Initialize the Linux-Use agent"""
    load_env()
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")
    
    # Initialize LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        api_key=api_key,
        timeout=60
    )
    
    # Create agent with custom instructions
    agent = Agent(
        instructions=[
            "You are a helpful Linux automation assistant",
            "Always explain what you're about to do before doing it",
            "Be careful with system operations",
            "If unsure, ask for confirmation"
        ],
        browser=Browser.FIREFOX,
        llm=llm,
        max_steps=15,
        max_consecutive_failures=3,
        use_vision=False,
        auto_minimize=False
    )
    
    return agent

def example_1_system_info():
    """Example 1: Get System Information"""
    print("\n" + "="*60)
    print("EXAMPLE 1: System Information")
    print("="*60)
    
    agent = create_agent()
    
    task = """
    Please provide the following system information:
    1. Current Linux distribution and version
    2. Screen resolution
    3. Currently open windows (if any)
    4. Desktop environment
    """
    
    print(f"\n📋 Task: {task.strip()}")
    print("\n🤖 Agent executing...\n")
    
    result = agent.print_response(task)
    return result

def example_2_shell_operations():
    """Example 2: Shell Command Execution"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Shell Operations")
    print("="*60)
    
    agent = create_agent()
    
    task = """
    Execute the following shell commands and report results:
    1. Show the current directory path
    2. List the files in /tmp
    3. Check disk space usage
    """
    
    print(f"\n📋 Task: {task.strip()}")
    print("\n🤖 Agent executing...\n")
    
    result = agent.print_response(task)
    return result

def example_3_file_management():
    """Example 3: File Management"""
    print("\n" + "="*60)
    print("EXAMPLE 3: File Management")
    print("="*60)
    
    agent = create_agent()
    
    task = """
    Create a test file with the following steps:
    1. Create a directory called 'linux_use_demo' in /tmp
    2. Create a text file called 'demo.txt' inside it
    3. Write 'Hello from Linux-Use Agent!' to the file
    4. Verify the file was created and show its contents
    """
    
    print(f"\n📋 Task: {task.strip()}")
    print("\n🤖 Agent executing...\n")
    
    result = agent.print_response(task)
    return result

def example_4_custom_task():
    """Example 4: Custom Interactive Task"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Task (Interactive)")
    print("="*60)
    
    agent = create_agent()
    
    # Get custom task from user
    print("\n💬 Enter your automation task (or press Enter for default):")
    user_task = input(">>> ").strip()
    
    if not user_task:
        user_task = "Check if Firefox is installed and tell me its version"
    
    print(f"\n📋 Task: {user_task}")
    print("\n🤖 Agent executing...\n")
    
    result = agent.print_response(user_task)
    return result

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("🐧 LINUX-USE AGENT - EXAMPLE USAGE")
    print("="*60)
    print("\nThis script demonstrates various automation capabilities")
    print("of the Linux-Use agent.\n")
    
    # Menu
    examples = {
        '1': ("System Information", example_1_system_info),
        '2': ("Shell Operations", example_2_shell_operations),
        '3': ("File Management", example_3_file_management),
        '4': ("Custom Task", example_4_custom_task),
    }
    
    print("Select an example to run:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  q. Quit\n")
    
    choice = input("Enter choice (1-4 or q): ").strip()
    
    if choice == 'q':
        print("\n👋 Goodbye!")
        return
    
    if choice in examples:
        try:
            name, func = examples[choice]
            result = func()
            
            print("\n" + "="*60)
            print("✅ EXECUTION COMPLETE")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n❌ Invalid choice")

if __name__ == "__main__":
    # Ensure we're in a proper display environment
    if not os.environ.get('DISPLAY'):
        print("⚠️ Warning: DISPLAY not set. Setting to :99 (Xvfb)")
        os.environ['DISPLAY'] = ':99'
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

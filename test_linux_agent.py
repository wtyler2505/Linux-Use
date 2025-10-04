#!/usr/bin/env python3
"""
Comprehensive test for Linux-Use Agent
Tests: AT-SPI2, Desktop Functions, LLM Integration
"""

import os
import sys
from pathlib import Path

# Set DISPLAY for X11
os.environ['DISPLAY'] = ':99'

# Add linux_use to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test 1: Verify all imports work"""
    print("\n" + "="*60)
    print("TEST 1: Import Verification")
    print("="*60)
    
    try:
        from linux_use.agent.desktop.service import Desktop
        from linux_use.agent.tree.service import Tree
        from linux_use.agent.tools.service import click_tool, type_tool, shell_tool
        import pyatspi
        print("✅ All imports successful")
        print(f"   - Desktop service: OK")
        print(f"   - Tree service: OK")
        print(f"   - Tools: OK")
        print(f"   - AT-SPI2 (pyatspi): OK")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_desktop_functions():
    """Test 2: Desktop detection and functions"""
    print("\n" + "="*60)
    print("TEST 2: Desktop Functions")
    print("="*60)
    
    try:
        from linux_use.agent.desktop.service import Desktop
        desktop = Desktop()
        
        # Test distro detection
        distro = desktop.get_linux_distro()
        print(f"✅ Linux Distribution: {distro}")
        
        # Test screen resolution
        resolution = desktop.get_screen_resolution()
        print(f"✅ Screen Resolution: {resolution}")
        
        # Test window enumeration
        windows = desktop.list_windows()
        print(f"✅ Windows detected: {len(windows)}")
        if windows:
            print(f"   Sample windows: {windows[:3]}")
        
        # Test active window
        active = desktop.get_active_window()
        print(f"✅ Active window: {active}")
        
        return True
    except Exception as e:
        print(f"❌ Desktop functions failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_atspi_tree():
    """Test 3: AT-SPI2 UI tree navigation"""
    print("\n" + "="*60)
    print("TEST 3: AT-SPI2 UI Tree Navigation")
    print("="*60)
    
    try:
        from linux_use.agent.desktop.service import Desktop
        from linux_use.agent.tree.service import Tree
        
        desktop = Desktop()
        tree = Tree(desktop)
        
        # Get UI state
        state = tree.get_state()
        
        print(f"✅ AT-SPI2 tree traversal successful")
        print(f"   - Interactive nodes: {len(state.interactive_nodes)}")
        print(f"   - Informative nodes: {len(state.informative_nodes)}")
        print(f"   - Scrollable nodes: {len(state.scrollable_nodes)}")
        
        # Show sample interactive nodes
        if state.interactive_nodes:
            print(f"\n   Sample interactive elements:")
            for node in state.interactive_nodes[:5]:
                print(f"     - {node.control_type}: {node.name} [{node.app_name}]")
        
        return True
    except Exception as e:
        print(f"❌ AT-SPI tree test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tools():
    """Test 4: Tool execution"""
    print("\n" + "="*60)
    print("TEST 4: Tool Execution")
    print("="*60)
    
    try:
        from linux_use.agent.tools.service import shell_tool
        
        # Test shell tool with simple command
        result = shell_tool("echo 'Hello from Linux-Use'")
        print(f"✅ Shell tool execution successful")
        print(f"   Output: {result}")
        
        # Test with ls command
        result = shell_tool("ls -la /tmp | head -5")
        print(f"✅ Shell tool with ls successful")
        
        return True
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_integration():
    """Test 5: Anthropic LLM Integration"""
    print("\n" + "="*60)
    print("TEST 5: LLM Integration (Anthropic)")
    print("="*60)
    
    try:
        from langchain_anthropic import ChatAnthropic
        
        # Check API key
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            return False
        
        print(f"✅ API Key found: {api_key[:20]}...")
        
        # Initialize LLM
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=api_key,
            timeout=30
        )
        
        # Test simple invocation
        response = llm.invoke("What is 2+2? Answer in one word.")
        print(f"✅ LLM invocation successful")
        print(f"   Response: {response.content}")
        
        return True
    except Exception as e:
        print(f"❌ LLM integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_initialization():
    """Test 6: Full Agent Initialization"""
    print("\n" + "="*60)
    print("TEST 6: Agent Initialization")
    print("="*60)
    
    try:
        from linux_use.agent.service import Agent
        from linux_use.agent.desktop.views import Browser
        from langchain_anthropic import ChatAnthropic
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=api_key
        )
        
        agent = Agent(
            instructions=["You are a helpful Linux automation assistant"],
            browser=Browser.FIREFOX,
            llm=llm,
            max_steps=10,
            use_vision=False
        )
        
        print(f"✅ Agent initialized successfully")
        print(f"   Name: {agent.name}")
        print(f"   Description: {agent.description}")
        print(f"   Max steps: {agent.max_steps}")
        print(f"   Tools available: {len(agent.registry.tools)}")
        
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("LINUX-USE AGENT TEST SUITE")
    print("="*60)
    print(f"Display: {os.environ.get('DISPLAY')}")
    print(f"Python: {sys.version}")
    
    results = {
        "Imports": test_imports(),
        "Desktop Functions": test_desktop_functions(),
        "AT-SPI2 Tree": test_atspi_tree(),
        "Tools": test_tools(),
        "LLM Integration": test_llm_integration(),
        "Agent Initialization": test_agent_initialization()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Linux-Use agent is ready.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

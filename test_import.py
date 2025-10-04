#!/usr/bin/env python3
"""
Test Linux-Use imports without requiring X11 display
"""
import os
import sys

# Mock DISPLAY to pass initial imports
os.environ['DISPLAY'] = ':99'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Disable pyautogui's X11 requirement for testing
import pyautogui
pyautogui._pyautogui_x11._display = None

print("🔍 Testing Linux-Use imports...")
print("=" * 50)

try:
    # Test core imports
    from linux_use.agent.desktop.views import Browser, Status, Size, App
    print("✅ Desktop views imported successfully")
    print(f"   Available browsers: {[b.value for b in Browser]}")
    
    from linux_use.agent.views import AgentResult, Action, AgentData
    print("✅ Agent views imported successfully")
    
    from linux_use.agent.state import AgentState
    print("✅ Agent state imported successfully")
    
    from linux_use.agent.tree.views import TreeState, TreeElementNode
    print("✅ Tree views imported successfully")
    
    # Test tool imports
    from linux_use.agent.tools.views import Click, Type, Shell
    print("✅ Tool views imported successfully")
    
    print("\n" + "=" * 50)
    print("✅ All core imports successful!")
    print("\n📝 Note: Full agent functionality requires X11 display")
    print("   This test verifies the codebase structure is correct.")
    
    # Test basic configuration
    print("\n🔧 Configuration Test:")
    print(f"   Firefox: {Browser.FIREFOX.value}")
    print(f"   Chrome: {Browser.CHROME.value}")
    print(f"   Edge: {Browser.EDGE.value}")
    
    # Test Size dataclass
    size = Size(width=1920, height=1080)
    print(f"   Screen Size: {size.to_string()}")
    
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

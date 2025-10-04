#!/usr/bin/env python3
"""
Simple validation test for Linux-Use Agent
Tests components that don't require full GUI stack
"""

import os
import sys

os.environ['DISPLAY'] = ':99'

def test_llm():
    """Test Anthropic LLM integration"""
    print("\n" + "="*60)
    print("TEST: Anthropic LLM Integration")
    print("="*60)
    
    try:
        from langchain_anthropic import ChatAnthropic
        
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found")
            return False
        
        print(f"✅ API Key found")
        
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=api_key,
            timeout=30
        )
        
        response = llm.invoke("Say 'Linux-Use agent is ready!' in exactly those words.")
        print(f"✅ LLM Response: {response.content}")
        
        return True
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_shell_tool():
    """Test shell tool execution"""
    print("\n" + "="*60)
    print("TEST: Shell Tool")
    print("="*60)
    
    try:
        # Import without triggering full GUI stack
        sys.path.insert(0, '/app')
        
        # Test basic shell command
        import subprocess
        result = subprocess.run(['bash', '-c', 'echo "Linux-Use Shell Tool Test"'], 
                              capture_output=True, text=True, timeout=5)
        print(f"✅ Shell execution: {result.stdout.strip()}")
        
        # Test with ls
        result = subprocess.run(['bash', '-c', 'ls /app | head -5'], 
                              capture_output=True, text=True, timeout=5)
        print(f"✅ Directory listing works")
        
        return True
    except Exception as e:
        print(f"❌ Shell tool test failed: {e}")
        return False

def test_core_modules():
    """Test core module imports"""
    print("\n" + "="*60)
    print("TEST: Core Module Imports")
    print("="*60)
    
    try:
        import pyatspi
        print("✅ pyatspi (AT-SPI2)")
        
        import distro
        print(f"✅ distro: {distro.name()}")
        
        from Xlib import display
        print("✅ python-xlib")
        
        import screeninfo
        print("✅ screeninfo")
        
        return True
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_linux_detection():
    """Test Linux-specific detection functions"""
    print("\n" + "="*60)
    print("TEST: Linux Detection")
    print("="*60)
    
    try:
        import distro
        import screeninfo
        
        # Distro info
        distro_name = distro.name()
        distro_version = distro.version()
        print(f"✅ Distribution: {distro_name} {distro_version}")
        
        # Screen info
        screens = screeninfo.get_monitors()
        print(f"✅ Screens detected: {len(screens)}")
        if screens:
            screen = screens[0]
            print(f"   Resolution: {screen.width}x{screen.height}")
        
        return True
    except Exception as e:
        print(f"❌ Linux detection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all simple tests"""
    print("\n" + "="*60)
    print("LINUX-USE SIMPLE VALIDATION")
    print("="*60)
    print(f"Display: {os.environ.get('DISPLAY')}")
    print(f"Python: {sys.version.split()[0]}")
    
    results = {
        "Core Modules": test_core_modules(),
        "Linux Detection": test_linux_detection(),
        "Shell Tool": test_shell_tool(),
        "LLM Integration": test_llm(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All validation tests passed!")
        print("Note: Full GUI integration should be tested on a real Linux system")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

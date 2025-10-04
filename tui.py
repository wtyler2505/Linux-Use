#!/usr/bin/env python3
"""Linux-Use TUI Entry Point"""

import sys
import os

# Add project to path
sys.path.insert(0, '/app')

# Ensure DISPLAY is set
if not os.environ.get('DISPLAY'):
    os.environ['DISPLAY'] = ':99'
    print("⚠️  No DISPLAY set, using :99")

try:
    from linux_use.tui import LinuxUseTUI
    
    if __name__ == "__main__":
        app = LinuxUseTUI()
        app.run()
        
except KeyboardInterrupt:
    print("\n\n⚠️  Interrupted by user")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Fatal error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

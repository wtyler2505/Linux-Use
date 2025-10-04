# 🐧 Linux-Use - Adaptation Summary

## Overview

This document summarizes the complete platform port of **Windows-Use** to **Linux-Use**, adapted specifically for Linux desktop environments with primary focus on Linux Mint 22.2 Cinnamon.

## ✅ Completed Implementation

### Phase 1: Project Restructuring ✅
- **Renamed** `windows_use` → `linux_use` throughout entire codebase
- **Updated** `pyproject.toml` with Linux-specific dependencies
- **Created** `.env` file with Anthropic API key
- **Updated** README.md for Linux users
- **Modified** main.py to use Anthropic Claude instead of Google Gemini

### Phase 2: Core Desktop Service ✅
**File:** `/app/linux_use/agent/desktop/service.py`

Completely rewritten for Linux:
- ✅ `get_linux_distro()` - Uses `distro` package
- ✅ `get_user_account_type()` - Checks LDAP/local accounts via `getent`
- ✅ `get_dpi_scaling()` - Uses `xrandr` or Xlib
- ✅ `get_screen_resolution()` - Uses `screeninfo` package
- ✅ `get_apps()` - Uses `wmctrl -lGpx` for window enumeration
- ✅ `execute_command()` - Uses `/bin/bash` instead of PowerShell
- ✅ `launch_app()` - Uses `gtk-launch` or direct command execution
- ✅ `switch_app()` - Uses `wmctrl -i -a` for window switching
- ✅ `resize_app()` - Uses `wmctrl -i -r -e` for window resizing
- ✅ `auto_minimize()` - Uses `xdotool` for IDE minimization

**Key Changes:**
- Removed Windows-specific `uiautomation` library
- Removed `ctypes.windll` API calls
- Added Linux-specific window management tools (wmctrl, xdotool)
- Graceful fallback when X11 is not available

### Phase 3: Configuration Updates ✅
**Files:**
- `/app/linux_use/agent/desktop/config.py`
- `/app/linux_use/agent/desktop/views.py`

Updates:
- ✅ Browser names without `.exe` extension
- ✅ Cinnamon-specific excluded apps (cinnamon, nemo-desktop, etc.)
- ✅ Updated Browser enum for Linux (Firefox, Chrome, Chromium, Edge, Brave)
- ✅ Added CINNAMON_SYSTEM_WINDOWS set

### Phase 4: Tool Adaptation ✅
**File:** `/app/linux_use/agent/tools/service.py`

Tool Updates:
- ✅ `shell_tool` - Bash command execution instead of PowerShell
- ✅ `app_tool` - Linux app management
- ✅ `click_tool` - Simplified for Linux (removed uiautomation dependency)
- ✅ `scroll_tool` - Uses pyautogui.scroll() instead of uiautomation.WheelUp/Down
- ✅ Updated tool descriptions for Linux context

### Phase 5: UI Tree Navigation ✅
**File:** `/app/linux_use/agent/tree/service.py`

Complete rewrite using AT-SPI2:
- ✅ Implemented `get_nodes_atspi()` using pyatspi2
- ✅ Recursive accessible tree traversal
- ✅ Role mapping (Windows → AT-SPI roles)
- ✅ Fallback mode when AT-SPI is unavailable
- ✅ Interactive element detection
- ✅ Scrollable element detection
- ✅ Text element extraction

AT-SPI Role Mapping:
- Windows ButtonControl → ROLE_PUSH_BUTTON
- Windows EditControl → ROLE_ENTRY/ROLE_TEXT
- Windows MenuItemControl → ROLE_MENU_ITEM
- etc.

### Phase 6: System Prompt Updates ✅
**File:** `/app/linux_use/agent/prompt/system.md`

Updated for Linux:
- ✅ Changed Windows-Use → Linux-Use
- ✅ Updated example applications (LibreOffice instead of Excel)
- ✅ Changed keyboard shortcuts (Super key instead of Win key)
- ✅ Updated shell tool descriptions (bash instead of PowerShell)
- ✅ Added common Linux applications list

### Phase 7: Agent Service Updates ✅
**File:** `/app/linux_use/agent/service.py`

- ✅ Updated agent name and description
- ✅ Changed default browser to Firefox
- ✅ Removed `live-inspect` dependency (requires Python 3.13)
- ✅ Fixed f-string syntax errors

## 📦 Dependencies

### System Packages (Installed)
```bash
python3-xlib       # X11 window management
python3-pyatspi    # AT-SPI2 accessibility
at-spi2-core       # Accessibility core
wmctrl             # Window management commands
xdotool            # X11 automation
python3-gi         # GObject introspection
gir1.2-atspi-2.0   # AT-SPI type library
```

### Python Packages (Installed)
```bash
# Core LLM/Agent Framework
langchain==0.3.27
langchain-anthropic==0.3.21
langgraph==0.6.8
psutil==7.1.0

# Linux-specific
python-xlib==0.15
distro==1.9.0
screeninfo==0.8.1

# GUI Automation
pyautogui==0.9.54
pillow==11.3.0

# Utilities
fuzzywuzzy==0.18.0
python-levenshtein==0.27.1
tabulate==0.9.0
markdownify==1.2.0
humancursor==1.1.5
```

## 🔧 Technical Architecture

### Windows → Linux Component Mapping

| Component | Windows API | Linux Equivalent |
|-----------|-------------|------------------|
| Window Management | Win32 API | wmctrl, xdotool |
| UI Automation | UIAutomation | AT-SPI2 (pyatspi) |
| Screen Info | ctypes.windll.user32 | screeninfo, Xlib |
| Shell | PowerShell | bash |
| DPI Detection | GetDpiForSystem() | xrandr |
| App Launching | Start Menu | gtk-launch |

### Display Server Support

| Feature | X11 | Wayland |
|---------|-----|---------|
| Window Management | ✅ Full Support (wmctrl, xdotool) | ⚠️  Limited |
| Screen Capture | ✅ pyautogui | ✅ pyautogui |
| UI Automation | ✅ AT-SPI2 | ✅ AT-SPI2 |
| Mouse/Keyboard | ✅ pyautogui | ⚠️  Requires permissions |

## 🎯 Testing Status

### ✅ Completed
- Project structure verification
- Import statement updates
- Dependency installation
- Code syntax validation
- Configuration file updates

### ⚠️ Requires X11 Environment
- Full agent execution
- Window management testing
- UI tree traversal
- Screenshot functionality
- Interactive automation

**Note:** The current environment is headless (no X11 display). Full testing requires a Linux desktop with X11 or Wayland display server.

## 🚀 Usage

### Basic Example
```python
from langchain_anthropic import ChatAnthropic
from linux_use.agent import Agent, Browser
from dotenv import load_dotenv

load_dotenv()

# Initialize with Anthropic Claude
llm = ChatAnthropic(
    model='claude-3-5-sonnet-20241022',
    temperature=0.2
)

# Create the agent
agent = Agent(
    llm=llm,
    browser=Browser.FIREFOX,
    use_vision=False,
    auto_minimize=True
)

# Execute a task
agent.print_response("Open Firefox and search for Linux automation")
```

### Running the Agent
```bash
# Set environment variables
export ANTHROPIC_API_KEY=your_key_here

# Run the agent
python main.py
```

## 🐛 Known Limitations

1. **Headless Environment**: Cannot test in containers without X11
2. **AT-SPI Complexity**: Some applications don't expose full accessibility tree
3. **Wayland Support**: Limited compared to X11
4. **App Launching**: May require desktop file configuration for some apps

## 🔄 Migration from Windows-Use

### API Changes
1. `get_windows_version()` → `get_linux_distro()`
2. PowerShell commands → bash commands
3. Win32 window handles → X11 window IDs (hex format)
4. `.exe` extensions removed from browser names

### Behavior Changes
1. App launching uses `gtk-launch` or direct execution
2. Window IDs are hexadecimal (from wmctrl)
3. Shell commands run in bash instead of PowerShell
4. Keyboard shortcuts use Super key instead of Windows key

## 📝 Next Steps for Full Implementation

### MCP Server Integration (Phase 7)
- Create MCP server wrapper
- Implement tool call handlers
- Add configuration files
- Test with MCP protocol

### Enhanced Testing (Phase 8)
- Integration tests on actual Linux Mint 22.2
- Browser automation tests
- File system operation tests
- System settings modification tests
- Multi-app workflow tests

### Optimization (Phase 9)
- Performance profiling
- Memory usage optimization
- AT-SPI tree caching
- Async window management

## 🎓 Development Notes

### Cinnamon Desktop Specific
- Window manager: Muffin (Mutter fork)
- File manager: Nemo
- Settings: cinnamon-settings
- Panel: cinnamon-panel

### Common Linux Applications
- Browser: Firefox, Chrome, Chromium
- File Manager: Nemo, Nautilus, Dolphin
- Text Editor: gedit, nano, vim
- Office: LibreOffice
- Terminal: gnome-terminal, konsole, xterm

## 📜 License

MIT License - See LICENSE file for details.

Original Windows-Use by [Jeomon George](https://github.com/Jeomon)
Linux adaptation by Tyler Wilson

## 🙏 Acknowledgments

This project is a complete platform port of [Windows-Use](https://github.com/CursorTouch/Windows-Use) to Linux, maintaining the same agent architecture while replacing all OS-specific interaction layers.

---

**Status**: Core implementation complete ✅  
**Next Phase**: MCP Integration & Linux Desktop Testing
**Target Platform**: Linux Mint 22.2 Cinnamon (X11)

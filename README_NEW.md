# 🐧 Linux-Use v2.0 🚀

<div align="center">

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/wtyler2505/Linux-Use/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux-blue)
![Status](https://img.shields.io/badge/status-active-success)

**🤖 AI-Powered Desktop Automation Agent for Linux**  
**🎨 Now with Interactive TUI Command Center!**

</div>

---

## 🌟 What is Linux-Use?

**Linux-Use** is a next-generation AI automation framework that transforms how you interact with Linux desktops. Using cutting-edge LLM technology and native Linux accessibility APIs, it provides intelligent automation that feels natural and powerful.

### ⚡ Key Highlights

- **🤖 LLM-Powered Intelligence**: Leverages Anthropic Claude for smart task understanding
- **🖥️ Interactive TUI**: Beautiful terminal interface with real-time monitoring
- **🌳 Native UI Access**: AT-SPI2 integration for precise element detection
- **🔧 Auto-Installation**: One-click dependency setup across distros
- **📊 Live Diagnostics**: Comprehensive system health monitoring
- **🎯 Multi-Distro**: Works on Ubuntu, Debian, Fedora, Arch, and more

---

## 🎬 Quick Demo

```bash
# Launch the interactive TUI
cd /app
export DISPLAY=:0
python tui.py
```

**Or use the command-line agent:**

```python
from linux_use.agent.service import LinuxAgent

agent = LinuxAgent()
agent.run("Open Firefox and search for 'Linux automation'")
```

---

## 🚀 Features

### 🖱️ Desktop Automation
- Click, type, scroll, drag & drop
- Window management (open, close, resize, switch)
- Keyboard shortcuts
- Mouse movements and gestures

### 🌳 Smart UI Detection
- AT-SPI2 accessibility integration
- UI element tree navigation
- Interactive element identification
- Text and control detection

### 🎮 Interactive TUI
- **Welcome Screen**: System detection & quick setup
- **Dashboard**: Real-time agent control & monitoring
- **Installation Wizard**: Automated dependency management
- **Diagnostics**: Health checks with auto-fix
- **Monitoring**: Live UI tree visualization
- **Configuration**: API keys & settings management

### 💻 Shell Integration
- Execute bash commands
- Script automation
- Process management
- Environment control

### 🔍 Advanced Capabilities
- Vision mode (screenshot-based fallback)
- Multi-step task execution
- Error handling & recovery
- Recording & playback (planned)

---

## 📦 Installation

### Quick Start (TUI Method)

```bash
# 1. Clone and enter directory
cd /app

# 2. Launch TUI
python tui.py

# 3. Use Installation Wizard
# Navigate to "START INSTALLATION" and let it handle everything!
```

### Manual Installation

**System Dependencies:**

```bash
# Debian/Ubuntu/Mint
sudo apt install -y python3-xlib python3-pyatspi at-spi2-core \
                    wmctrl xdotool python3-gi gir1.2-atspi-2.0 \
                    python3-tk dbus-x11

# Fedora/RHEL
sudo dnf install -y python3-xlib python3-pyatspi2 at-spi2-core \
                    wmctrl xdotool python3-gobject dbus-x11

# Arch/Manjaro
sudo pacman -S python-xlib python-atspi at-spi2-core \
               wmctrl xdotool python-gobject dbus
```

**Python Dependencies:**

```bash
pip install -e /app
```

**API Key Setup:**

```bash
# Add to /app/.env
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> /app/.env
```

---

## 🎯 Usage Examples

### Example 1: TUI Dashboard

```bash
# Start TUI
python tui.py

# Navigate to Dashboard
# Enter task: "Open VSCode and create a new file"
# Click EXECUTE
# Watch real-time execution in log panel
```

### Example 2: Python Script

```python
from linux_use.agent.service import LinuxAgent
import asyncio

async def automate():
    agent = LinuxAgent()
    
    # Execute task
    result = agent.run("Open Firefox, navigate to github.com")
    print(f"Result: {result}")

asyncio.run(automate())
```

### Example 3: Multi-Step Workflow

```python
agent = LinuxAgent()

tasks = [
    "Open terminal",
    "Type 'ls -la'",
    "Press enter",
    "Take screenshot"
]

for task in tasks:
    agent.run(task)
```

---

## 🖥️ TUI Guide

### Navigation

- **`q`** - Quit
- **`h`** - Home (Welcome)
- **`i`** - Installation
- **`d`** - Dashboard
- **`m`** - Monitoring
- **`c`** - Configuration
- **`t`** - Diagnostics

### Screens Overview

#### 🏠 Welcome
- System auto-detection
- Dependency status
- Quick navigation

#### 📦 Installation
- One-click dependency install
- Progress tracking
- Multi-distro support

#### 🎮 Dashboard
- Task input & execution
- Real-time logs
- Agent controls (execute, pause, stop)
- System metrics

#### 🔍 Diagnostics
- 8+ system checks
- Auto-fix capabilities
- Color-coded results

#### 📊 Monitoring
- Live UI tree
- Process monitoring
- System stats

#### ⚙️ Configuration
- API key management
- Agent settings
- Advanced options

See **[TUI_USER_GUIDE.md](TUI_USER_GUIDE.md)** for detailed documentation.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Linux-Use Agent                 │
├─────────────────────────────────────────┤
│  LLM Layer (Anthropic Claude)           │
│  ├─ Task Understanding                  │
│  ├─ Action Planning                     │
│  └─ Error Recovery                      │
├─────────────────────────────────────────┤
│  Agent Core                             │
│  ├─ Desktop Service (X11, AT-SPI2)      │
│  ├─ Tools Service (Click, Type, etc.)   │
│  └─ Tree Service (UI Navigation)        │
├─────────────────────────────────────────┤
│  Linux APIs                             │
│  ├─ X11 (python-xlib)                   │
│  ├─ AT-SPI2 (pyatspi)                   │
│  ├─ wmctrl/xdotool                      │
│  └─ D-Bus                               │
├─────────────────────────────────────────┤
│  TUI Layer (Textual)                    │
│  ├─ Interactive Screens                 │
│  ├─ Real-time Monitoring                │
│  └─ Configuration Management            │
└─────────────────────────────────────────┘
```

---

## 🧪 Testing

### Run TUI Integration Tests

```bash
chmod +x run_tui_tests.sh
./run_tui_tests.sh
```

### Run Agent Tests

```bash
python test_simple.py
```

### Run Example Tests

```bash
python example_agent_test.py
```

---

## 🛠️ Troubleshooting

### TUI Won't Launch

```bash
# Ensure DISPLAY is set
echo $DISPLAY

# For headless environments
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
```

### Agent Execution Fails

```bash
# Check API key
cat /app/.env | grep ANTHROPIC_API_KEY

# Verify dependencies
python -c "import pyatspi, Xlib; print('OK')"
```

### AT-SPI2 Issues

```bash
# Start AT-SPI bus
/usr/libexec/at-spi-bus-launcher &

# Check D-Bus
echo $DBUS_SESSION_BUS_ADDRESS
```

### Run Diagnostics

```bash
python tui.py
# Navigate to Diagnostics screen
# Click "RUN DIAGNOSTICS"
# Review and auto-fix issues
```

---

## 📚 Documentation

- **[TUI User Guide](TUI_USER_GUIDE.md)** - Complete TUI documentation
- **[Implementation Status](IMPLEMENTATION_STATUS.md)** - Current progress
- **[Roadmap](ROADMAP.md)** - Future plans
- **[Changelog](CHANGELOG.md)** - Version history
- **[Contributing](CONTRIBUTING.md)** - How to contribute

---

## 🎯 Supported Platforms

### ✅ Fully Supported
- Ubuntu 22.04+, 24.04+
- Linux Mint 22+
- Debian 11+, 12+
- Pop!_OS 22.04+

### 🟡 Tested
- Fedora 38+
- Arch Linux
- Manjaro

### 🟢 Should Work
- Any Linux distro with:
  - X11 display server
  - AT-SPI2 support
  - Python 3.11+

---

## 🤝 Contributing

We welcome contributions! See **[CONTRIBUTING.md](CONTRIBUTING.md)** for guidelines.

**Quick Start:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Credits

**Based on [Windows-Use](https://github.com/CursorTouch/Windows-Use)** by Jeomon George  
**Linux Port & TUI**: Community effort  
**Powered by**: Anthropic Claude, Textual, AT-SPI2, python-xlib

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

## 💬 Community

- **Issues**: [GitHub Issues](https://github.com/wtyler2505/Linux-Use/issues)
- **Discussions**: [GitHub Discussions](https://github.com/wtyler2505/Linux-Use/discussions)

---

<div align="center">

**Made with ❤️ for the Linux community**

[⬆ Back to Top](#-linux-use-v20-)

</div>

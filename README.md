# 🐧 Linux-Use

<div align="center">

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/wtyler2505/Linux-Use/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux-blue)

**AI-powered desktop automation agent for Linux systems**

Forked from [Windows-Use](https://github.com/CursorTouch/Windows-Use) by [Jeomon George](https://github.com/Jeomon)

</div>

---

**Linux-Use** is a powerful automation agent that interacts directly with Linux desktop environments at the GUI layer. It bridges the gap between AI Agents and Linux OS to perform tasks such as opening applications, clicking buttons, typing text, executing shell commands, and capturing UI state—all without relying on traditional computer vision models. Enabling any LLM to perform desktop automation on Linux systems.

## ✨ Features

- 🖱️ **GUI Automation**: Click, type, scroll, drag, and interact with any GUI element
- 🪟 **Window Management**: Launch, switch, resize, and manage application windows
- 🌳 **UI Tree Navigation**: Access Linux accessibility APIs (AT-SPI2) for UI element detection
- 💻 **Shell Integration**: Execute bash commands and scripts
- 🎯 **Smart Element Detection**: Automatically identify interactive elements
- 🔄 **Multi-Desktop Support**: Optimized for Cinnamon, compatible with GNOME, KDE, XFCE

## 🛠️ Installation Guide

### **Prerequisites**

- Python 3.12 or higher
- Linux Mint 22.2+ (Cinnamon) or Ubuntu 24.04+
- X11 display server (Wayland experimental support)

### **System Dependencies**

Install required Linux packages:

```bash
sudo apt install -y \
    python3-xlib \
    python3-pyatspi \
    at-spi2-core \
    wmctrl \
    xdotool \
    python3-gi \
    gir1.2-atspi-2.0
```

### **Python Installation**

Install using pip:

```bash
pip install linux-use
```

Or install from source:

```bash
git clone https://github.com/wtyler2505/Linux-Use.git
cd Linux-Use
pip install -e .
```

## ⚙️ Basic Usage

```python
from langchain_anthropic import ChatAnthropic
from linux_use.agent import Agent, Browser
from dotenv import load_dotenv

load_dotenv()

# Initialize with your preferred LLM
llm = ChatAnthropic(model='claude-3-5-sonnet-20241022')

# Create the agent
agent = Agent(llm=llm, browser=Browser.FIREFOX)

# Execute a task
agent.print_response("Open Firefox and search for Linux automation")
```

## 🤖 Run Agent

You can use the following to run from a script:

```bash
python main.py
```

## 📋 Supported Platforms

| Platform | Desktop Environment | Status |
|----------|-------------------|--------|
| Linux Mint 22.2+ | Cinnamon | ✅ Fully Supported |
| Ubuntu 24.04+ | GNOME | ✅ Supported |
| Ubuntu | KDE Plasma | 🔄 Experimental |
| Debian-based | XFCE/MATE | 🔄 Experimental |

| Display Server | Status |
|---------------|--------|
| X11 | ✅ Fully Supported |
| Wayland | 🔄 Experimental |

## 🎯 Supported Browsers

- Firefox
- Google Chrome / Chromium
- Microsoft Edge (Linux)
- Brave Browser

## 🔧 Configuration

Create a `.env` file in your project root:

```env
ANTHROPIC_API_KEY=your_key_here
# or
OPENAI_API_KEY=your_key_here
# or
GOOGLE_API_KEY=your_key_here
```

## ⚠️ Caution

The agent interacts directly with your Linux desktop at the GUI layer to perform actions. While designed to act intelligently and safely, it can make mistakes that might cause unintended system behavior or changes. **Run the agent in a sandbox environment or virtual machine for testing.**

## 🪪 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This project is a fork of [Windows-Use](https://github.com/CursorTouch/Windows-Use) by [Jeomon George](https://github.com/Jeomon), adapted for Linux desktop environments.

**Original Windows-Use** made with ❤️ by [Jeomon George](https://github.com/Jeomon)

**Linux-Use adaptation** by Tyler Wilson

---

## 🤝 Contributing

Contributions are welcome! Please check the [CONTRIBUTING](CONTRIBUTING.md) file for setup and development workflow.

## Citation

```bibtex
@software{linux_use,
  author       = {Wilson, Tyler and George, Jeomon},
  title        = {Linux-Use: Enable AI to control Linux Desktop Environments},
  year         = {2025},
  publisher    = {GitHub},
  url          = {https://github.com/wtyler2505/Linux-Use}
}
```
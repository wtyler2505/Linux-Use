# 🚀 Linux-Use Quick Start Guide

## For Linux Mint 22.2 Cinnamon Users

This guide will help you get Linux-Use up and running quickly.

---

## 📦 Step 1: Install System Dependencies

Open a terminal and run:

```bash
sudo apt update
sudo apt install -y \
    python3-xlib \
    python3-pyatspi \
    at-spi2-core \
    gir1.2-atspi-2.0 \
    wmctrl \
    xdotool \
    python3-gi \
    python3-tk \
    dbus-x11
```

**What these do:**
- `python3-xlib` - X11 protocol for window management
- `python3-pyatspi` - AT-SPI2 accessibility API for UI element detection
- `wmctrl/xdotool` - Window management utilities
- `dbus-x11` - D-Bus session for accessibility

---

## 🐍 Step 2: Set Up Python Environment

```bash
# Clone the repository
git clone https://github.com/wtyler2505/Linux-Use.git
cd Linux-Use

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -e .
```

**Or install from PyPI:**
```bash
pip install linux-use
```

---

## 🔑 Step 3: Configure API Keys

Create a `.env` file in your project directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
# Choose one LLM provider:
ANTHROPIC_API_KEY=sk-ant-xxxxx
# OR
OPENAI_API_KEY=sk-xxxxx
# OR
GOOGLE_API_KEY=xxxxx
```

**Get API Keys:**
- Anthropic: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/
- Google: https://ai.google.dev/

---

## ✅ Step 4: Run Validation Tests

Verify your installation:

```bash
# Run simple validation
python3 test_simple.py
```

**Expected output:**
```
✅ PASS: Core Modules
✅ PASS: Linux Detection
✅ PASS: Shell Tool
✅ PASS: LLM Integration

Total: 4/4 tests passed
🎉 All validation tests passed!
```

---

## 🎮 Step 5: Run Your First Agent

### Example 1: Simple Task

Create `demo.py`:

```python
from langchain_anthropic import ChatAnthropic
from linux_use.agent import Agent
from linux_use.agent.desktop.views import Browser
import os

# Load API key
api_key = os.environ.get('ANTHROPIC_API_KEY')

# Initialize LLM
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=api_key
)

# Create agent
agent = Agent(
    instructions=["You are a helpful Linux automation assistant"],
    browser=Browser.FIREFOX,
    llm=llm,
    max_steps=10
)

# Run a simple task
print("Running agent...")
result = agent.print_response("What applications are currently open?")
```

Run it:
```bash
export $(cat .env | grep -v '^#' | xargs)
python3 demo.py
```

### Example 2: Web Automation

```python
agent.print_response("Open Firefox and navigate to example.com")
```

### Example 3: File Management

```python
agent.print_response("Create a new folder called 'test_folder' on the Desktop")
```

---

## 🔧 Common Issues & Solutions

### Issue: "pyatspi not found"
**Solution:**
```bash
# Install system package
sudo apt install python3-pyatspi gir1.2-atspi-2.0

# Create symlink to venv (if using virtualenv)
ln -s /usr/lib/python3/dist-packages/pyatspi venv/lib/python3.XX/site-packages/pyatspi
ln -s /usr/lib/python3/dist-packages/gi venv/lib/python3.XX/site-packages/gi
```

### Issue: "Can't open display"
**Solution:**
Make sure you're running on a real X11 display (not SSH without X forwarding):
```bash
echo $DISPLAY  # Should show :0 or similar
```

### Issue: "AT-SPI bus launcher failed"
**Solution:**
```bash
# Start D-Bus session
eval $(dbus-launch --sh-syntax)
export DBUS_SESSION_BUS_ADDRESS
```

### Issue: "No windows detected"
**Solution:**
Make sure you have GUI applications running. The agent works best with actual desktop applications open.

---

## 🎯 Best Practices

1. **Start Simple** - Test with basic tasks first (listing windows, opening apps)
2. **Use Specific Instructions** - Give clear, step-by-step tasks to the agent
3. **Monitor Execution** - Watch what the agent is doing, especially initially
4. **Set max_steps** - Limit steps to prevent runaway execution
5. **Test in VM** - Use a virtual machine for initial testing

---

## 📚 Example Tasks to Try

### Basic Tasks
```python
# List windows
agent.print_response("What windows are currently open?")

# Open application
agent.print_response("Open the Text Editor application")

# Take screenshot
agent.print_response("Take a screenshot and save it to Desktop")
```

### Intermediate Tasks
```python
# File operations
agent.print_response("Create a new text file called 'notes.txt' and write 'Hello from Linux-Use' in it")

# Web browsing
agent.print_response("Open Firefox, go to github.com and search for 'linux automation'")

# System info
agent.print_response("Tell me my screen resolution and Linux distribution")
```

### Advanced Tasks
```python
# Form filling
agent.print_response("Open LibreOffice Calc and create a simple budget spreadsheet with categories")

# Multi-step workflow
agent.print_response("""
1. Open Firefox
2. Navigate to example.com
3. Take a screenshot
4. Save the screenshot to Desktop
""")
```

---

## 🛠️ Configuration Options

### Agent Parameters

```python
agent = Agent(
    instructions=["Custom instructions"],     # Agent guidelines
    browser=Browser.FIREFOX,                  # Default browser
    llm=llm,                                  # Language model
    max_steps=25,                             # Max execution steps
    max_consecutive_failures=3,               # Failure tolerance
    use_vision=False,                         # Vision mode (experimental)
    auto_minimize=False                       # Auto-minimize IDE
)
```

### Supported Browsers
- `Browser.FIREFOX` - Firefox (recommended)
- `Browser.CHROME` - Google Chrome
- `Browser.CHROMIUM` - Chromium
- `Browser.EDGE` - Microsoft Edge
- `Browser.BRAVE` - Brave Browser

---

## 📖 Additional Resources

- **Implementation Status**: See `IMPLEMENTATION_STATUS.md` for detailed component status
- **Linux Adaptation Notes**: See `LINUX_ADAPTATION.md` for porting details
- **API Documentation**: Check the docstrings in the code

---

## 🐛 Reporting Issues

Found a bug? Please report it:
1. Check existing issues: https://github.com/wtyler2505/Linux-Use/issues
2. Create a new issue with:
   - Linux distribution and version
   - Desktop environment
   - Error messages and logs
   - Steps to reproduce

---

## 💡 Tips for Success

1. **Accessibility Must Be Enabled**
   - Cinnamon usually has this on by default
   - Check: System Settings → Accessibility

2. **Run on Primary Display**
   - Multi-monitor setups may have issues
   - Test on primary display first

3. **Use Recent Applications**
   - Modern apps with good accessibility support work best
   - Firefox, Chrome, LibreOffice are well-supported

4. **Start with Vision=False**
   - Vision mode is experimental
   - AT-SPI2 mode is more reliable

---

## ✅ Next Steps

Once you have the basics working:

1. Explore the `linux_use/agent/` directory structure
2. Look at `tools/service.py` for available tools
3. Customize `prompt/system.md` for your use case
4. Build your own automation workflows

**Happy Automating! 🎉**

# ⚡ Linux-Use Quick Start Guide

Get up and running in 5 minutes!

---

## 🎯 Method 1: Interactive TUI (Recommended)

### Step 1: Launch TUI

```bash
cd /app
export DISPLAY=:0  # Or your display number
python tui.py
```

**Headless Environment?**
```bash
# Start virtual display first
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
python tui.py
```

### Step 2: Install Dependencies

1. You'll see the **Welcome Screen**
2. Click `▶ START INSTALLATION`
3. Watch as it installs everything automatically
4. Takes 2-5 minutes depending on your system

### Step 3: Configure API Key

1. Click `◀ BACK` to return to Welcome
2. Click `▶ LAUNCH DASHBOARD`
3. Click `⚙️ Configuration` button
4. Enter your Anthropic API key
5. Click `✓ SAVE CONFIGURATION`

### Step 4: Run Your First Task

1. Return to Dashboard (click `◀ BACK`)
2. In the **TASK INPUT** field, type:
   ```
   Open Firefox browser
   ```
3. Click `▶ EXECUTE`
4. Watch the magic happen in the log panel!

---

## 🎯 Method 2: Command Line Agent

### Quick Setup

```bash
# 1. Set API key
echo "ANTHROPIC_API_KEY=sk-ant-your-key" >> /app/.env

# 2. Test agent
cd /app
python example_agent_test.py
```

### Python Script

```python
from linux_use.agent.service import LinuxAgent

# Create agent
agent = LinuxAgent()

# Run task
result = agent.run("Open terminal and type 'hello world'")
print(result)
```

---

## 🎯 Method 3: Manual Installation

### Install System Dependencies

**Ubuntu/Debian/Mint:**
```bash
sudo apt update
sudo apt install -y python3-xlib python3-pyatspi at-spi2-core \
                    wmctrl xdotool python3-gi gir1.2-atspi-2.0 \
                    python3-tk dbus-x11
```

**Fedora:**
```bash
sudo dnf install -y python3-xlib python3-pyatspi2 at-spi2-core \
                    wmctrl xdotool python3-gobject dbus-x11
```

**Arch:**
```bash
sudo pacman -S python-xlib python-atspi at-spi2-core \
               wmctrl xdotool python-gobject dbus
```

### Install Python Packages

```bash
pip install -e /app
```

### Setup Environment

```bash
# API Key
echo "ANTHROPIC_API_KEY=your-key-here" >> /app/.env

# DISPLAY (if needed)
export DISPLAY=:0

# D-Bus (if needed)
eval $(dbus-launch --sh-syntax)
```

---

## 🔍 Verify Installation

### Check Dependencies

```bash
python tui.py
# Navigate to "RUN DIAGNOSTICS"
```

Or manually:

```bash
# Check Python modules
python -c "import pyatspi, Xlib, distro; print('✓ OK')"

# Check CLI tools
which wmctrl xdotool
```

---

## 🎮 Example Tasks

### Easy Tasks
- "Open Firefox"
- "Open terminal"
- "Minimize all windows"
- "Take a screenshot"

### Medium Tasks
- "Open Firefox and go to google.com"
- "Open calculator and calculate 2+2"
- "Open terminal and list files"
- "Switch to the Firefox window"

### Advanced Tasks
- "Open VSCode, create a new file, and type 'Hello World'"
- "Open terminal, run 'ls -la', and show the output"
- "Search Google for 'Linux automation' and click first result"

---

## 🐛 Troubleshooting

### TUI Won't Start

```bash
# Check DISPLAY
echo $DISPLAY

# If empty, set it
export DISPLAY=:0

# Or start Xvfb
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
```

### Import Errors

```bash
# Install missing packages
pip install textual rich psutil distro langchain langchain-anthropic

# Or reinstall
pip install -e /app --force-reinstall
```

### Agent Won't Execute

```bash
# Check API key
cat /app/.env | grep ANTHROPIC_API_KEY

# Set if missing
export ANTHROPIC_API_KEY="sk-ant-your-key"

# Test connection
python -c "from anthropic import Anthropic; print('✓ OK')"
```

### AT-SPI2 Issues

```bash
# Install packages
sudo apt install python3-pyatspi gir1.2-atspi-2.0 at-spi2-core

# Start AT-SPI bus
/usr/libexec/at-spi-bus-launcher &

# Start D-Bus
eval $(dbus-launch --sh-syntax)
```

---

## 📚 Next Steps

### Learn More
- Read [TUI_USER_GUIDE.md](TUI_USER_GUIDE.md) for detailed TUI documentation
- Check [FEATURES.md](FEATURES.md) for complete feature list
- See [README.md](README.md) for architecture overview

### Advanced Usage
- Explore the Dashboard's Quick Actions
- Try the Monitoring screen to see UI tree
- Customize settings in Configuration
- Write Python scripts with the agent

### Get Help
- Run Diagnostics in TUI for automatic troubleshooting
- Check [GitHub Issues](https://github.com/wtyler2505/Linux-Use/issues)
- Read documentation in `/app/docs/`

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| TUI Launch | 5 seconds |
| Dependency Install | 2-5 minutes |
| First Task Execution | 10-30 seconds |
| Total Setup | 5-10 minutes |

---

## ✅ Success Checklist

- [ ] TUI launches without errors
- [ ] All dependencies installed (green check in Welcome)
- [ ] API key configured
- [ ] First task executes successfully
- [ ] Logs show agent activity
- [ ] No red errors in Diagnostics

---

**You're all set! Start automating! 🚀**

For questions, open an issue on GitHub or check the documentation.
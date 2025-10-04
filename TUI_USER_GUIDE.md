# Linux-Use TUI User Guide

## 🚀 Quick Start

### Launch the TUI

```bash
cd /app
export DISPLAY=:0  # Use your actual display
python tui.py
```

Or for headless environments:

```bash
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
python tui.py
```

---

## 📱 Screen Guide

### 1. Welcome Screen

The entry point showing:
- System detection (distro, desktop environment, display server)
- Dependency status
- Quick navigation buttons

**Actions:**
- `▶ START INSTALLATION` - Install missing dependencies
- `▶ LAUNCH DASHBOARD` - Go to main control center
- `▶ RUN DIAGNOSTICS` - Check system health

### 2. Installation Wizard

Interactive package installer supporting:
- **apt** (Debian, Ubuntu, Mint)
- **yum/dnf** (Fedora, RHEL, CentOS)
- **pacman** (Arch, Manjaro)

**Features:**
- Real-time progress tracking
- Automatic package mapping across distros
- Python package installation
- pyatspi symlink setup

**Actions:**
- `▶ START INSTALLATION` - Begin automated installation
- `◀ BACK` - Return to previous screen
- `✗ CANCEL` - Abort installation

### 3. Dashboard (Command Center)

The main control hub featuring:

**Panels:**
- **Status Panel**: System status, agent state, uptime
- **Metrics Panel**: CPU, RAM, disk usage
- **Control Panel**: Task input and execution controls
- **Log Panel**: Real-time activity feed

**Controls:**
- **Task Input**: Enter natural language automation tasks
- `▶ EXECUTE` - Run the entered task
- `⏸ PAUSE` - Pause agent execution
- `■ STOP` - Stop agent completely

**Quick Actions:**
- `⚡ Run Diagnostics` - System health check
- `📊 System Status` - Display system info
- `🔍 UI Tree View` - Open monitoring screen
- `⚙️ Configuration` - Open settings

**Keyboard Shortcuts:**
- `d` - Open diagnostics
- `m` - Open monitoring
- `c` - Open configuration
- `q` - Quit application

### 4. Diagnostics Screen

Comprehensive system diagnostics:

**Checks:**
- Display server (DISPLAY variable)
- D-Bus session
- AT-SPI2 availability
- X server health
- Dependencies status
- Python environment
- File permissions
- System resources (CPU, RAM, disk)

**Features:**
- `🔄 RUN DIAGNOSTICS` - Run all checks
- `🔧 AUTO-FIX ALL` - Attempt automatic fixes
- Color-coded results (✓ pass, ⚠ warning, ✗ fail)
- Fix suggestions for each issue

### 5. Monitoring Screen

Live system monitoring:

**Features:**
- **UI Tree Visualization**: Real-time AT-SPI2 element tree
- **Activity Log**: System events and metrics
- **Process Monitor**: Running applications

**Actions:**
- `🔄 REFRESH TREE` - Update UI element tree
- `📸 CAPTURE STATE` - Save current state
- Auto-refresh every 5 seconds

### 6. Configuration Screen

Settings management:

**API Keys:**
- Anthropic API Key (for agent LLM)
- Claude Max OAuth (future feature)

**Agent Settings:**
- Max steps per task (default: 25)
- Max consecutive failures (default: 3)
- Vision mode toggle
- Auto-minimize IDE

**Advanced:**
- Enable recording
- Remote monitoring
- Remote port configuration

**Actions:**
- `✓ SAVE CONFIGURATION` - Save to .env file
- `🔄 LOAD DEFAULTS` - Reset to defaults
- `◀ BACK` - Return without saving

---

## 🎮 Usage Examples

### Example 1: Simple Task Execution

1. Launch TUI and go to Dashboard
2. Enter task: "Open Firefox and navigate to google.com"
3. Click `▶ EXECUTE`
4. Watch the log panel for real-time feedback

### Example 2: Installation

1. From Welcome screen, click `▶ START INSTALLATION`
2. Watch progress bar and log output
3. Wait for completion
4. Return to Welcome to verify dependencies

### Example 3: System Diagnostics

1. From Dashboard, click `⚡ Run Diagnostics`
2. Review diagnostic results
3. Click `🔧 AUTO-FIX ALL` for automatic fixes
4. Re-run diagnostics to verify

### Example 4: Configure API Key

1. Open Configuration screen
2. Enter Anthropic API key in password field
3. Adjust agent settings as needed
4. Click `✓ SAVE CONFIGURATION`
5. Restart TUI or agent to apply

---

## 🐛 Troubleshooting

### TUI Won't Launch

**Problem**: Import errors or display connection issues

**Solutions:**
```bash
# Check DISPLAY is set
echo $DISPLAY

# Start Xvfb if headless
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

# Check Python dependencies
pip install textual rich psutil distro

# Verify installation
python -c "import textual; print('OK')"
```

### Agent Execution Fails

**Problem**: "No ANTHROPIC_API_KEY found"

**Solution:**
```bash
# Set in .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." >> /app/.env

# Or export directly
export ANTHROPIC_API_KEY="sk-ant-..."
```

### AT-SPI2 Not Working

**Problem**: UI tree is empty

**Solutions:**
```bash
# Install AT-SPI2 packages
sudo apt install python3-pyatspi gir1.2-atspi-2.0 at-spi2-core

# Start AT-SPI bus launcher
/usr/libexec/at-spi-bus-launcher &

# Check D-Bus session
echo $DBUS_SESSION_BUS_ADDRESS

# Start D-Bus if needed
eval $(dbus-launch --sh-syntax)
```

### High Resource Usage

**Problem**: CPU or RAM usage is high

**Solutions:**
- Close unnecessary applications
- Reduce max steps in configuration
- Disable recording in advanced settings
- Use headless mode if GUI not needed

---

## 🎨 Theme Customization

The TUI uses a cyberpunk theme defined in `theme.tcss`. To customize:

1. Edit `/app/linux_use/tui/theme.tcss`
2. Modify color variables:
   ```css
   $primary: #00ffff;    /* Cyan */
   $secondary: #ff00ff;  /* Magenta */
   $accent: #ffff00;     /* Yellow */
   ```
3. Restart TUI to see changes

---

## ⌨️ Keyboard Shortcuts

**Global:**
- `q` - Quit application
- `?` - Show help (if implemented)
- `h` - Home (Welcome screen)

**Dashboard:**
- `d` - Diagnostics
- `m` - Monitoring
- `c` - Configuration
- `i` - Installation

**Navigation:**
- `Tab` - Next widget
- `Shift+Tab` - Previous widget
- `Enter` - Activate button
- `Esc` - Back/Cancel

---

## 📊 Log Interpretation

**Log Symbols:**
- `SYS` - System message (magenta)
- `✓` - Success (green)
- `✗` - Error (red)
- `⚠` - Warning (yellow)
- `ℹ` - Information (cyan)
- `$` - Command (cyan italic)
- `🤖` - Agent message (blue)

---

## 🔧 Advanced Usage

### Running in Docker

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /app:/app \
  linux-use python /app/tui.py
```

### Remote Access

Enable remote monitoring in Configuration, then:

```bash
# Access from another machine
ssh -L 8888:localhost:8888 user@server
# Navigate to http://localhost:8888
```

### Automation Scripts

```python
from linux_use.tui.services.agent_service import AgentService
import asyncio

async def automate():
    agent = AgentService()
    await agent.initialize_agent()
    await agent.execute_task("Your task here")

asyncio.run(automate())
```

---

## 📚 Further Reading

- [Main README](/app/README.md)
- [Implementation Status](/app/IMPLEMENTATION_STATUS.md)
- [Roadmap](/app/ROADMAP.md)
- [Changelog](/app/CHANGELOG.md)
- [Contributing Guidelines](/app/CONTRIBUTING.md)

---

**Version**: 2.0  
**Last Updated**: 2025-09  
**Support**: Open an issue on GitHub
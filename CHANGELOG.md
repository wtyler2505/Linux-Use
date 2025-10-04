# Changelog

All notable changes to Linux-Use will be documented in this file.

## [2.0.0] - 2025-09-XX

### 🎉 Major Release: Linux-Use v2.0

Complete rewrite of Windows-Use for Linux environments with a comprehensive TUI.

### Added
- **Full Linux Support**
  - X11 integration via python-xlib
  - AT-SPI2 accessibility for UI tree navigation
  - wmctrl and xdotool for window management
  - Support for multiple Linux distros (Debian, Ubuntu, Fedora, Arch, etc.)
  - Desktop environment detection (GNOME, KDE, Cinnamon, XFCE, etc.)
  
- **Interactive TUI (Terminal User Interface)**
  - Welcome screen with system detection
  - Installation wizard with progress tracking
  - Real-time dashboard with agent control
  - Comprehensive diagnostics with auto-fix
  - Live monitoring with UI tree visualization
  - Configuration management screen
  - Cyberpunk-themed styling
  
- **Enhanced Agent Capabilities**
  - Improved error handling
  - Better UI element detection
  - Multi-distro package management
  - Fallback mechanisms for missing dependencies
  
- **Developer Tools**
  - Comprehensive logging system
  - System diagnostics utilities
  - Automated package installer
  - Agent service layer for TUI integration

### Changed
- Migrated from Windows automation to Linux automation
- Replaced uiautomation with AT-SPI2 + Xlib
- Updated all desktop interaction methods for Linux
- Redesigned system detection and configuration

### Fixed
- Headless environment support via Xvfb
- pyatspi import handling in virtual environments
- Cross-distro package name mapping
- Window detection reliability

### Technical Details
- **Languages**: Python 3.11+
- **Frameworks**: Textual (TUI), LangChain, Anthropic API
- **Linux APIs**: X11, AT-SPI2, D-Bus
- **Tools**: wmctrl, xdotool, xrandr, xdpyinfo

---

## [1.0.0] - 2024-XX-XX

### Initial Release (Windows-Use)
- Original Windows desktop automation framework
- UI tree navigation via uiautomation
- LLM-powered task execution
- Screenshot and vision capabilities

---

**Note**: Version 2.0.0 represents a complete platform migration and architectural overhaul.
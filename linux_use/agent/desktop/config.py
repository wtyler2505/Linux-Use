from typing import Set

# Browser process names for Linux (without .exe extension)
BROWSER_NAMES = set([
    'firefox',
    'firefox-esr',
    'chrome',
    'google-chrome',
    'google-chrome-stable',
    'chromium',
    'chromium-browser',
    'microsoft-edge',
    'brave',
    'brave-browser'
])

# Apps to avoid tracking (agent UI, terminals, etc.)
AVOIDED_APPS: Set[str] = set([
    'AgentUI',
    'terminator',
    'gnome-terminal',
    'xterm',
    'konsole'
])

# Excluded system windows (Cinnamon-specific)
EXCLUDED_APPS: Set[str] = set([
    # Desktop and panels
    'Desktop',
    'desktop_window',
    'nemo-desktop',
    'Nemo-desktop',
    
    # Cinnamon window manager and panels
    'cinnamon',
    'Cinnamon',
    'cinnamon-panel',
    'cinnamon-launcher',
    'cinnamon-screensaver',
    'cinnamon-settings-daemon',
    
    # GNOME components (if present)
    'gnome-shell',
    'gnome-panel',
    
    # KDE components (if present)
    'plasmashell',
    'plasma-desktop',
    
    # XFCE components
    'xfce4-panel',
    'xfdesktop',
    
    # Docks and launchers
    'plank',
    'cairo-dock',
    'docky',
    'Conky',
    
    # System trays
    'stalonetray',
    'trayer'
])

# Cinnamon-specific window classes to ignore
CINNAMON_SYSTEM_WINDOWS = set([
    'cinnamon-screensaver',
    'cinnamon-settings-daemon',
    'nemo-desktop',
    'Cinnamon'
])
"""System detection utilities"""

import os
import shutil
import subprocess
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
import distro

@dataclass
class SystemInfo:
    """System information"""
    distro_id: str
    distro_name: str
    distro_version: str
    desktop_environment: Optional[str]
    display_server: str  # X11 or Wayland
    package_manager: Optional[str]
    python_version: str
    has_sudo: bool
    
class SystemDetector:
    """Detect system configuration and requirements"""
    
    PACKAGE_MANAGERS = {
        'apt': ['apt-get', 'apt'],
        'yum': ['yum'],
        'dnf': ['dnf'],
        'pacman': ['pacman'],
        'zypper': ['zypper'],
    }
    
    REQUIRED_SYSTEM_PACKAGES = [
        'python3-xlib',
        'python3-pyatspi',
        'at-spi2-core',
        'gir1.2-atspi-2.0',
        'wmctrl',
        'xdotool',
        'python3-gi',
        'python3-tk',
        'dbus-x11',
    ]
    
    @staticmethod
    def detect() -> SystemInfo:
        """Detect system information"""
        return SystemInfo(
            distro_id=distro.id(),
            distro_name=distro.name(),
            distro_version=distro.version(),
            desktop_environment=SystemDetector._detect_desktop_environment(),
            display_server=SystemDetector._detect_display_server(),
            package_manager=SystemDetector._detect_package_manager(),
            python_version=SystemDetector._get_python_version(),
            has_sudo=SystemDetector._check_sudo(),
        )
    
    @staticmethod
    def _detect_desktop_environment() -> Optional[str]:
        """Detect desktop environment"""
        de = os.environ.get('XDG_CURRENT_DESKTOP')
        if de:
            return de.upper()
        
        # Fallback detection
        for de_var in ['DESKTOP_SESSION', 'GDMSESSION']:
            de = os.environ.get(de_var)
            if de:
                return de.upper()
        
        return None
    
    @staticmethod
    def _detect_display_server() -> str:
        """Detect if using X11 or Wayland"""
        session_type = os.environ.get('XDG_SESSION_TYPE', '')
        if 'wayland' in session_type.lower():
            return 'Wayland'
        elif 'x11' in session_type.lower():
            return 'X11'
        
        # Check DISPLAY
        if os.environ.get('DISPLAY'):
            return 'X11'
        elif os.environ.get('WAYLAND_DISPLAY'):
            return 'Wayland'
        
        return 'Unknown'
    
    @staticmethod
    def _detect_package_manager() -> Optional[str]:
        """Detect available package manager"""
        for pm_name, pm_commands in SystemDetector.PACKAGE_MANAGERS.items():
            for cmd in pm_commands:
                if shutil.which(cmd):
                    return pm_name
        return None
    
    @staticmethod
    def _get_python_version() -> str:
        """Get Python version"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    @staticmethod
    def _check_sudo() -> bool:
        """Check if user has sudo access"""
        try:
            result = subprocess.run(
                ['sudo', '-n', 'true'],
                capture_output=True,
                timeout=1
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @staticmethod
    def check_dependencies() -> Dict[str, bool]:
        """Check which dependencies are installed"""
        dependencies = {}
        
        # Check system packages
        for pkg in SystemDetector.REQUIRED_SYSTEM_PACKAGES:
            dependencies[pkg] = SystemDetector._check_package_installed(pkg)
        
        # Check Python modules
        python_modules = [
            'pyatspi',
            'Xlib',
            'distro',
            'screeninfo',
            'pyautogui',
            'langchain_anthropic',
        ]
        
        for module in python_modules:
            try:
                __import__(module)
                dependencies[f"python:{module}"] = True
            except (ImportError, SystemExit, Exception):
                dependencies[f"python:{module}"] = False
        
        # Check command-line tools
        cli_tools = ['wmctrl', 'xdotool', 'xrandr', 'xdpyinfo']
        for tool in cli_tools:
            dependencies[f"cli:{tool}"] = shutil.which(tool) is not None
        
        return dependencies
    
    @staticmethod
    def _check_package_installed(package: str) -> bool:
        """Check if a system package is installed"""
        pm = SystemDetector._detect_package_manager()
        
        if pm == 'apt':
            try:
                result = subprocess.run(
                    ['dpkg', '-l', package],
                    capture_output=True,
                    timeout=5
                )
                return result.returncode == 0
            except Exception:
                return False
        elif pm == 'yum' or pm == 'dnf':
            try:
                result = subprocess.run(
                    [pm, 'list', 'installed', package],
                    capture_output=True,
                    timeout=5
                )
                return result.returncode == 0
            except Exception:
                return False
        elif pm == 'pacman':
            try:
                result = subprocess.run(
                    ['pacman', '-Q', package],
                    capture_output=True,
                    timeout=5
                )
                return result.returncode == 0
            except Exception:
                return False
        
        return False
    
    @staticmethod
    def get_missing_dependencies() -> List[str]:
        """Get list of missing dependencies"""
        deps = SystemDetector.check_dependencies()
        return [name for name, installed in deps.items() if not installed]

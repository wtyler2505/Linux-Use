"""TUI Screens"""

from .welcome import WelcomeScreen
from .installation import InstallationScreen
from .dashboard import DashboardScreen
from .diagnostics import DiagnosticsScreen
from .monitoring import MonitoringScreen
from .configuration import ConfigurationScreen

__all__ = [
    'WelcomeScreen',
    'InstallationScreen',
    'DashboardScreen',
    'DiagnosticsScreen',
    'MonitoringScreen',
    'ConfigurationScreen',
]

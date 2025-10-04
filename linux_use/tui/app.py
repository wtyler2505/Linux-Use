"""Main TUI Application"""

from textual.app import App
from textual.binding import Binding
from textual.driver import Driver

# Import all screens
from .screens.welcome import WelcomeScreen
from .screens.installation import InstallationScreen
from .screens.dashboard import DashboardScreen
from .screens.diagnostics import DiagnosticsScreen
from .screens.monitoring import MonitoringScreen
from .screens.configuration import ConfigurationScreen

class LinuxUseTUI(App):
    """Linux-Use Terminal User Interface Application"""
    
    TITLE = "LINUX-USE :: DESKTOP AUTOMATION COMMAND CENTER"
    CSS_PATH = "theme.tcss"
    
    SCREENS = {
        "welcome": WelcomeScreen,
        "installation": InstallationScreen,
        "dashboard": DashboardScreen,
        "diagnostics": DiagnosticsScreen,
        "monitoring": MonitoringScreen,
        "configuration": ConfigurationScreen,
    }
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True, priority=True),
        Binding("h", "push_screen('welcome')", "Home", show=False),
        Binding("i", "push_screen('installation')", "Install", show=False),
        Binding("d", "push_screen('dashboard')", "Dashboard", show=False),
        Binding("m", "push_screen('monitoring')", "Monitor", show=False),
        Binding("c", "push_screen('configuration')", "Config", show=False),
        Binding("t", "push_screen('diagnostics')", "Diagnostics", show=False),
        Binding("?", "help", "Help", show=True),
    ]
    
    def on_mount(self) -> None:
        """Called when app starts"""
        # Start with welcome screen
        self.push_screen("welcome")
    
    def action_help(self) -> None:
        """Show help overlay"""
        self.bell()
        # TODO: Implement help overlay

def run_tui():
    """Entry point to run the TUI"""
    app = LinuxUseTUI()
    app.run()

if __name__ == "__main__":
    run_tui()

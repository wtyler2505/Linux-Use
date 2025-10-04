"""Welcome Screen"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal, Center
from textual.widgets import Static, Button, Label
from ..widgets.ascii_banner import ASCIIBanner
from ..utils.system_detector import SystemDetector

class WelcomeScreen(Screen):
    """Initial welcome screen with system detection"""
    
    CSS = """
    WelcomeScreen {
        align: center middle;
    }
    
    #welcome-container {
        width: 80;
        height: auto;
        background: $surface-lighten-1;
        border: heavy $primary;
        padding: 2;
    }
    
    .button-row {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    
    .sys-info {
        width: 100%;
        color: $secondary;
        text-align: center;
        margin-top: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Center():
            with Vertical(id="welcome-container"):
                yield ASCIIBanner()
                
                # System detection
                sys_info = SystemDetector.detect()
                yield Static(
                    f"◆ SYSTEM DETECTED: {sys_info.distro_name} {sys_info.distro_version}",
                    classes="sys-info"
                )
                yield Static(
                    f"◆ DESKTOP: {sys_info.desktop_environment or 'Unknown'} | DISPLAY: {sys_info.display_server}",
                    classes="sys-info"
                )
                yield Static(
                    f"◆ PACKAGE MANAGER: {sys_info.package_manager or 'Not detected'}",
                    classes="sys-info"
                )
                
                # Check dependencies
                missing = SystemDetector.get_missing_dependencies()
                if missing:
                    yield Static(
                        f"\n⚠  {len(missing)} DEPENDENCIES MISSING - INSTALLATION REQUIRED",
                        classes="sys-info"
                    )
                    yield Static(
                        "▶ RECOMMENDATION: Run Installation Wizard",
                        classes="sys-info"
                    )
                else:
                    yield Static(
                        "\n✓ ALL DEPENDENCIES INSTALLED - SYSTEM READY",
                        classes="sys-info"
                    )
                
                # Action buttons
                with Horizontal(classes="button-row"):
                    yield Button("▶ START INSTALLATION", id="btn-install", variant="success")
                    yield Button("▶ LAUNCH DASHBOARD", id="btn-dashboard", variant="primary")
                    yield Button("▶ RUN DIAGNOSTICS", id="btn-diagnostics")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "btn-install":
            self.app.push_screen("installation")
        elif event.button.id == "btn-dashboard":
            self.app.push_screen("dashboard")
        elif event.button.id == "btn-diagnostics":
            self.app.push_screen("diagnostics")

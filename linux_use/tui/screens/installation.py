"""Installation Wizard Screen"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button, ProgressBar, Label
# Worker import not needed - using run_worker instead
from ..widgets.log_viewer import LogViewer
from ..utils.system_detector import SystemDetector
from ..utils.installer import PackageInstaller
import asyncio

class InstallationScreen(Screen):
    """Interactive installation wizard with progress tracking"""
    
    CSS = """
    InstallationScreen {
        background: $surface;
    }
    
    #install-container {
        width: 100%;
        height: 100%;
        background: $surface;
        padding: 1;
    }
    
    #install-header {
        width: 100%;
        height: 3;
        background: $surface-lighten-1;
        border: heavy $primary;
        content-align: center middle;
    }
    
    #install-progress {
        width: 100%;
        height: auto;
        padding: 1;
        background: $surface-lighten-1;
        border: heavy $primary;
        margin-top: 1;
    }
    
    #install-log {
        width: 100%;
        height: 1fr;
        margin-top: 1;
        border: heavy $primary;
    }
    
    #install-actions {
        width: 100%;
        height: auto;
        margin-top: 1;
        align: center middle;
    }
    
    .progress-label {
        color: $secondary;
        text-style: bold;
        margin-bottom: 1;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.installer = None
        self.is_installing = False
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical(id="install-container"):
            yield Static("╔═══ INSTALLATION WIZARD ═══════════════════════════╗", id="install-header")
            
            with Container(id="install-progress"):
                yield Static("▶ INSTALLATION PROGRESS", classes="progress-label")
                yield ProgressBar(total=100, show_eta=True, id="progress-bar")
                yield Static("Ready to begin installation...", id="progress-status")
            
            yield LogViewer(id="install-log", max_lines=500)
            
            with Horizontal(id="install-actions"):
                yield Button("▶ START INSTALLATION", id="btn-start", variant="success")
                yield Button("◀ BACK", id="btn-back")
                yield Button("✗ CANCEL", id="btn-cancel", variant="error")
    
    def on_mount(self) -> None:
        """Called when screen is mounted"""
        log = self.query_one("#install-log", LogViewer)
        log.log_system("Installation wizard initialized")
        log.log_info("System detection complete")
        
        # Show what needs to be installed
        missing = SystemDetector.get_missing_dependencies()
        if missing:
            log.log_warning(f"Found {len(missing)} missing dependencies")
            for dep in missing[:10]:  # Show first 10
                log.log_info(f"  - {dep}")
            if len(missing) > 10:
                log.log_info(f"  ... and {len(missing) - 10} more")
        else:
            log.log_success("All dependencies already installed!")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "btn-start":
            if not self.is_installing:
                self.start_installation()
        elif event.button.id == "btn-back":
            self.app.pop_screen()
        elif event.button.id == "btn-cancel":
            if self.is_installing:
                self.query_one("#install-log", LogViewer).log_warning("Installation cancelled by user")
                self.is_installing = False
            self.app.pop_screen()
    
    @work(exclusive=True)
    async def start_installation(self) -> None:
        """Start the installation process"""
        self.is_installing = True
        log = self.query_one("#install-log", LogViewer)
        progress_bar = self.query_one("#progress-bar", ProgressBar)
        status = self.query_one("#progress-status", Static)
        
        # Disable start button
        self.query_one("#btn-start", Button).disabled = True
        
        log.log_system("═" * 50)
        log.log_system("BEGINNING INSTALLATION SEQUENCE")
        log.log_system("═" * 50)
        
        def progress_callback(message: str):
            """Callback for installation progress"""
            if message.startswith("✅"):
                log.log_success(message)
            elif message.startswith("❌"):
                log.log_error(message)
            elif message.startswith("⚠️"):
                log.log_warning(message)
            else:
                log.log_info(message)
        
        # Create installer
        self.installer = PackageInstaller(progress_callback=progress_callback)
        
        # Update progress
        progress_bar.update(progress=20)
        status.update("⚡ Detecting system configuration...")
        await asyncio.sleep(1)
        
        # Run full installation
        progress_bar.update(progress=40)
        status.update("📦 Installing system packages...")
        
        success = await self.installer.full_installation()
        
        progress_bar.update(progress=100)
        
        if success:
            status.update("✅ Installation complete!")
            log.log_system("═" * 50)
            log.log_success("INSTALLATION COMPLETE - SYSTEM READY")
            log.log_system("═" * 50)
        else:
            status.update("❌ Installation failed - check logs")
            log.log_system("═" * 50)
            log.log_error("INSTALLATION FAILED - MANUAL INTERVENTION REQUIRED")
            log.log_system("═" * 50)
        
        self.is_installing = False
        
        # Re-enable button (change to "Done")
        btn = self.query_one("#btn-start", Button)
        btn.label = "✓ DONE"
        btn.disabled = False
        btn.variant = "success"

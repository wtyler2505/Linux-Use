"""Main Dashboard Screen"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.widgets import Static, Button, Input, Label, TabbedContent, TabPane
from ..widgets.status_panel import StatusPanel
from ..widgets.metrics_display import MetricsDisplay
from ..widgets.log_viewer import LogViewer
from ..services.agent_service import AgentService
import time
import asyncio

class DashboardScreen(Screen):
    """Main control dashboard with live agent monitoring"""
    
    CSS = """
    DashboardScreen {
        background: $surface;
    }
    
    #dashboard-grid {
        grid-size: 3 3;
        grid-gutter: 1;
        padding: 1;
        height: 100%;
    }
    
    #header-panel {
        column-span: 3;
        height: 5;
        background: $surface-lighten-1;
        border: heavy $primary;
        content-align: center middle;
    }
    
    #status-panel {
        row-span: 2;
        background: $surface-lighten-1;
        border: heavy $primary;
        padding: 1;
    }
    
    #metrics-panel {
        row-span: 2;
        background: $surface-lighten-1;
        border: heavy $primary;
        padding: 1;
    }
    
    #control-panel {
        row-span: 2;
        background: $surface-lighten-1;
        border: heavy $secondary;
        padding: 1;
    }
    
    #log-panel {
        column-span: 3;
        background: $surface;
        border: heavy $primary;
    }
    
    .control-section {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    
    .control-title {
        color: $secondary;
        text-style: bold;
        background: $surface;
        padding: 1;
    }
    
    #task-input {
        width: 100%;
        margin-bottom: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "diagnostics", "Diagnostics"),
        ("m", "monitoring", "Monitoring"),
        ("c", "config", "Config"),
    ]
    
    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.agent_service = None
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Grid(id="dashboard-grid"):
            # Header
            yield Static(
                "╔══════════════ LINUX-USE COMMAND CENTER ══════════════╗\\n"
                "║  STATUS: OPERATIONAL | CLEARANCE: LEVEL 5 | ENCRYPTED  ║\\n"
                "╚═══════════════════════════════════════════════════════╝",
                id="header-panel"
            )
            
            # Status panel
            with Container(id="status-panel"):
                yield StatusPanel()
            
            # Metrics panel
            with Container(id="metrics-panel"):
                yield MetricsDisplay()
            
            # Control panel
            with Container(id="control-panel"):
                yield Static("╔══ AGENT CONTROL ═══════════╗", classes="control-title")
                
                with Vertical(classes="control-section"):
                    yield Label("▶ TASK INPUT:", classes="metric-label")
                    yield Input(
                        placeholder="Enter automation task...",
                        id="task-input"
                    )
                    
                    with Horizontal():
                        yield Button("▶ EXECUTE", id="btn-execute", variant="success")
                        yield Button("⏸ PAUSE", id="btn-pause", variant="warning")
                        yield Button("■ STOP", id="btn-stop", variant="error")
                
                yield Static("\\n╔══ QUICK ACTIONS ═══════════╗", classes="control-title")
                
                with Vertical(classes="control-section"):
                    yield Button("⚡ Run Diagnostics", id="btn-quick-diag")
                    yield Button("📊 System Status", id="btn-sys-status")
                    yield Button("🔍 UI Tree View", id="btn-tree-view")
                    yield Button("⚙️  Configuration", id="btn-config")
            
            # Log panel
            with Container(id="log-panel"):
                yield LogViewer(id="main-log", max_lines=1000)
    
    def on_mount(self) -> None:
        """Called when screen is mounted"""
        log = self.query_one("#main-log", LogViewer)
        log.log_system("╔═══════════════════════════════════════════╗")
        log.log_system("║   LINUX-USE AGENT SYSTEM ACTIVATED       ║")
        log.log_system("╚═══════════════════════════════════════════╝")
        log.log_success("Command center online")
        log.log_info("All systems operational")
        log.log_info("Waiting for task input...")
        
        # Start update timer
        self.set_interval(1.0, self.update_dashboard)
    
    def update_dashboard(self) -> None:
        """Update dashboard metrics periodically"""
        try:
            # Update metrics
            metrics = self.query_one(MetricsDisplay)
            metrics.update_metrics()
            
            # Update uptime
            status = self.query_one(StatusPanel)
            uptime = int(time.time() - self.start_time)
            hours = uptime // 3600
            minutes = (uptime % 3600) // 60
            seconds = uptime % 60
            status.query_one("#uptime", Static).update(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        except Exception:
            pass
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        log = self.query_one("#main-log", LogViewer)
        
        if event.button.id == "btn-execute":
            task_input = self.query_one("#task-input", Input)
            task = task_input.value
            if task:
                log.log_command(f"Executing: {task}")
                log.log_warning("Agent execution not yet implemented in TUI")
                task_input.value = ""
        
        elif event.button.id == "btn-pause":
            log.log_warning("Agent paused")
        
        elif event.button.id == "btn-stop":
            log.log_error("Agent stopped")
        
        elif event.button.id == "btn-quick-diag":
            log.log_info("Launching diagnostics...")
            self.app.push_screen("diagnostics")
        
        elif event.button.id == "btn-sys-status":
            log.log_info("System status check initiated")
            from ..utils.system_detector import SystemDetector
            sys_info = SystemDetector.detect()
            log.log_success(f"OS: {sys_info.distro_name} {sys_info.distro_version}")
            log.log_success(f"Desktop: {sys_info.desktop_environment}")
            log.log_success(f"Display: {sys_info.display_server}")
        
        elif event.button.id == "btn-tree-view":
            log.log_info("UI Tree visualization...")
            self.app.push_screen("monitoring")
        
        elif event.button.id == "btn-config":
            log.log_info("Opening configuration...")
            self.app.push_screen("configuration")
    
    def action_diagnostics(self) -> None:
        """Open diagnostics screen"""
        self.app.push_screen("diagnostics")
    
    def action_monitoring(self) -> None:
        """Open monitoring screen"""
        self.app.push_screen("monitoring")
    
    def action_config(self) -> None:
        """Open configuration screen"""
        self.app.push_screen("configuration")
    
    def action_quit(self) -> None:
        """Quit the application"""
        self.app.exit()

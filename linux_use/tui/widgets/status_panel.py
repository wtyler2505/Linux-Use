"""Status Panel Widget"""

from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Container, Vertical


class StatusPanel(Container):
    """Real-time status display panel"""
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical():
            yield Static("╔═══ SYSTEM STATUS ═══════╗", classes="metric-label")
            yield Static("", id="status-content")
            yield Static("", id="agent-state")
            yield Static("", id="uptime")
            yield Static("", id="tasks-completed")
    
    def on_mount(self) -> None:
        """Initialize on mount"""
        self.update_status("STANDBY", "cyan")
        self.query_one("#uptime", Static).update("⏱ Uptime: 00:00:00")
        self.query_one("#tasks-completed", Static).update("✅ Tasks: 0")
    
    def update_status(self, status: str, color: str = "white"):
        """Update status display"""
        status_widget = self.query_one("#status-content", Static)
        
        status_icons = {
            "STANDBY": "⏸",
            "RUNNING": "▶",
            "PAUSED": "⏸",
            "ERROR": "✗",
            "SUCCESS": "✓"
        }
        
        icon = status_icons.get(status, "●")
        status_widget.update(f"{icon} STATUS: [{color}]{status}[/]")
    
    def update_agent_state(self, state: str):
        """Update agent state"""
        self.query_one("#agent-state", Static).update(f"🤖 Agent: {state}")
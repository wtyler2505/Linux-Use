"""Status Panel Widget"""

from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Container, Horizontal, Vertical
from rich.text import Text
import time

class StatusPanel(Container):
    """Real-time agent status panel with cyberpunk styling"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent_status = "IDLE"
        self.last_action = "System initialized"
        self.mission_count = 0
        self.success_rate = 100.0
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical():
            yield Static("╭── AGENT STATUS MONITOR ──────────────────────╮", classes="metric-label")
            
            with Horizontal():
                yield Static("│ STATUS:", classes="metric-label")
                yield Static(self.agent_status, id="agent-status", classes="status-active")
            
            with Horizontal():
                yield Static("│ LAST ACTION:", classes="metric-label")
                yield Static(self.last_action, id="last-action", classes="metric-value")
            
            with Horizontal():
                yield Static("│ MISSIONS:", classes="metric-label")
                yield Static(f"{self.mission_count}", id="mission-count", classes="metric-value")
            
            with Horizontal():
                yield Static("│ SUCCESS RATE:", classes="metric-label")
                yield Static(f"{self.success_rate:.1f}%", id="success-rate", classes="metric-high")
            
            with Horizontal():
                yield Static("│ UPTIME:", classes="metric-label")
                yield Static("00:00:00", id="uptime", classes="metric-value")
            
            yield Static("╰───────────────────────────────────────────────╯", classes="metric-label")
    
    def update_status(self, status: str, action: str = None):
        """Update agent status"""
        self.agent_status = status
        status_widget = self.query_one("#agent-status", Static)
        status_widget.update(status)
        
        if status == "ACTIVE":
            status_widget.remove_class("status-idle", "status-error")
            status_widget.add_class("status-active")
        elif status == "ERROR":
            status_widget.remove_class("status-idle", "status-active")
            status_widget.add_class("status-error")
        else:
            status_widget.remove_class("status-active", "status-error")
            status_widget.add_class("status-idle")
        
        if action:
            self.last_action = action
            self.query_one("#last-action", Static).update(action)

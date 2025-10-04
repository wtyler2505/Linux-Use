"""System Metrics Display Widget"""

from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Container, Horizontal, Vertical
import psutil
import time

class MetricsDisplay(Container):
    """Display system metrics with bar graphs"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = time.time()
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical():
            yield Static("╭── SYSTEM RESOURCES ───────────────────────╮", classes="metric-label")
            
            with Horizontal():
                yield Static("│ CPU:", classes="metric-label")
                yield Static("[█████░░░░░] 50%", id="cpu-bar", classes="metric-value")
            
            with Horizontal():
                yield Static("│ RAM:", classes="metric-label")
                yield Static("[████░░░░░░] 40%", id="mem-bar", classes="metric-value")
            
            with Horizontal():
                yield Static("│ DISK:", classes="metric-label")
                yield Static("[███░░░░░░░] 30%", id="disk-bar", classes="metric-value")
            
            with Horizontal():
                yield Static("│ NET:", classes="metric-label")
                yield Static("↑ 0 KB/s  ↓ 0 KB/s", id="net-speed", classes="metric-value")
            
            yield Static("╰───────────────────────────────────────────╯", classes="metric-label")
    
    def create_bar(self, percentage: float, width: int = 10) -> str:
        """Create ASCII bar graph"""
        filled = int((percentage / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percentage:.0f}%"
    
    def update_metrics(self):
        """Update system metrics"""
        cpu = psutil.cpu_percent(interval=0.1)
        self.query_one("#cpu-bar", Static).update(self.create_bar(cpu))
        
        mem = psutil.virtual_memory()
        self.query_one("#mem-bar", Static).update(self.create_bar(mem.percent))
        
        disk = psutil.disk_usage('/')
        self.query_one("#disk-bar", Static).update(self.create_bar(disk.percent))
        
        net = psutil.net_io_counters()
        self.query_one("#net-speed", Static).update(
            f"↑ {net.bytes_sent / 1024:.0f} KB/s  ↓ {net.bytes_recv / 1024:.0f} KB/s"
        )

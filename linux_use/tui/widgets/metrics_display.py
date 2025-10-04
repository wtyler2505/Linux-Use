"""Metrics Display Widget"""

from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Container, Vertical
import psutil
import time


class MetricsDisplay(Container):
    """Live system metrics display"""
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical():
            yield Static("╔═══ SYSTEM METRICS ══════╗", classes="metric-label")
            yield Static("", id="cpu-metric")
            yield Static("", id="memory-metric")
            yield Static("", id="disk-metric")
            yield Static("", id="network-metric")
            yield Static("", id="timestamp-metric")
    
    def on_mount(self) -> None:
        """Initialize metrics"""
        self.update_metrics()
    
    def update_metrics(self):
        """Update all metrics"""
        try:
            # CPU
            cpu = psutil.cpu_percent(interval=0.1)
            cpu_color = "green" if cpu < 70 else "yellow" if cpu < 90 else "red"
            self.query_one("#cpu-metric", Static).update(
                f"[{cpu_color}]▪ CPU:[/] {cpu:.1f}%"
            )
            
            # Memory
            mem = psutil.virtual_memory()
            mem_color = "green" if mem.percent < 70 else "yellow" if mem.percent < 90 else "red"
            self.query_one("#memory-metric", Static).update(
                f"[{mem_color}]▪ RAM:[/] {mem.percent:.1f}%"
            )
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_color = "green" if disk.percent < 70 else "yellow" if disk.percent < 90 else "red"
            self.query_one("#disk-metric", Static).update(
                f"[{disk_color}]▪ DISK:[/] {disk.percent:.1f}%"
            )
            
            # Network (placeholder)
            self.query_one("#network-metric", Static).update(
                "▪ NET: Active"
            )
            
            # Timestamp
            self.query_one("#timestamp-metric", Static).update(
                f"🕒 {time.strftime('%H:%M:%S')}"
            )
            
        except Exception as e:
            pass
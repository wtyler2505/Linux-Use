"""Enhanced Log Viewer Widget"""

from textual.widgets import RichLog
from rich.text import Text
from datetime import datetime


class LogViewer(RichLog):
    """Cyberpunk-styled log viewer with color coding"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_scroll = True
    
    def log_system(self, message: str):
        """Log system message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append("SYS", style="bold magenta")
        text.append(" │ ", style="dim")
        text.append(message, style="bold white")
        self.write(text)
    
    def log_success(self, message: str):
        """Log success message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append("✓", style="bold green")
        text.append(" │ ", style="dim")
        text.append(message, style="green")
        self.write(text)
    
    def log_error(self, message: str):
        """Log error message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append("✗", style="bold red")
        text.append(" │ ", style="dim")
        text.append(message, style="red")
        self.write(text)
    
    def log_warning(self, message: str):
        """Log warning message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append("⚠", style="bold yellow")
        text.append(" │ ", style="dim")
        text.append(message, style="yellow")
        self.write(text)
    
    def log_info(self, message: str):
        """Log info message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append("ℹ", style="bold cyan")
        text.append(" │ ", style="dim")
        text.append(message, style="white")
        self.write(text)
    
    def log_command(self, message: str):
        """Log command message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append("$", style="bold cyan")
        text.append(" │ ", style="dim")
        text.append(message, style="cyan italic")
        self.write(text)
    
    def log_agent(self, message: str):
        """Log agent message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="dim")
        text.append("🤖", style="bold blue")
        text.append(" │ ", style="dim")
        text.append(message, style="blue")
        self.write(text)
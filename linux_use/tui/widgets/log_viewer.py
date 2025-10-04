"""Log Viewer Widget with Matrix-style scrolling"""

from textual.widgets import RichLog
from rich.text import Text
import time

class LogViewer(RichLog):
    """Cyberpunk-style log viewer"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_lines = kwargs.get('max_lines', 1000)
        self.add_class("matrix-scroll")
    
    def log_info(self, message: str):
        """Log info message"""
        timestamp = time.strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="#00d9ff bold")
        text.append("▶ ", style="#00ff41 bold")
        text.append(message, style="#00ff41")
        self.write(text)
    
    def log_success(self, message: str):
        """Log success message"""
        timestamp = time.strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="#00d9ff bold")
        text.append("✓ ", style="#00ff41 bold")
        text.append(message, style="#00ff41 bold")
        self.write(text)
    
    def log_error(self, message: str):
        """Log error message"""
        timestamp = time.strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="#00d9ff bold")
        text.append("✗ ", style="#ff0051 bold blink")
        text.append(message, style="#ff0051 bold")
        self.write(text)
    
    def log_warning(self, message: str):
        """Log warning message"""
        timestamp = time.strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="#00d9ff bold")
        text.append("⚠ ", style="#ff6b00 bold")
        text.append(message, style="#ff6b00")
        self.write(text)
    
    def log_command(self, command: str):
        """Log command execution"""
        timestamp = time.strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="#00d9ff bold")
        text.append("$ ", style="#8a2be2 bold")
        text.append(command, style="#00d9ff")
        self.write(text)
    
    def log_system(self, message: str):
        """Log system message"""
        timestamp = time.strftime("%H:%M:%S")
        text = Text()
        text.append(f"[{timestamp}] ", style="#00d9ff bold")
        text.append("◆ ", style="#8a2be2 bold")
        text.append(message, style="#8a2be2")
        self.write(text)

"""ASCII Art Banner Widget"""

from textual.app import ComposeResult
from textual.widgets import Static
from rich.text import Text

class ASCIIBanner(Static):
    """Cyberpunk-style ASCII banner"""
    
    BANNER = """
╭────────────────────────────────────────────────────────────────────────╮
│                                                                        │
│  ██╗     ██╗███╗   ██╗██╗██╗   ██╗██╗  ██╗██╗  ██╗██████╗        │
│  ██║     ██║████╗  ██║██║██║   ██║██║  ██║██║ ██╔╝██╔════╝        │
│  ██║     ██║██╔██╗ ██║██║██║   ██║██║  ██║█████╔╝ █████╗          │
│  ██║     ██║██║╚██╗██║██║██║   ██║██║  ██║██╔═██╗╚══██║        │
│  ███████╗██║██║ ╚████║╚██╗╚████╔╝╚████╔╝██║  ██║██████║        │
│  ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═╝ ╚═══╝  ╚═══╝ ╚═╝  ╚═╝╚═════╝        │
│                                                                        │
│  ▶ AI-POWERED DESKTOP AUTOMATION SYSTEM                               │
│  ▶ LINUX MINT 22.2 CINNAMON OPTIMIZED                                │
│  ▶ CLASSIFIED: LEVEL 5 CLEARANCE                                      │
│                                                                        │
╰────────────────────────────────────────────────────────────────────────╯
    """
    
    def __init__(self, **kwargs):
        super().__init__(self.BANNER, **kwargs)
        self.styles.color = "#00ff41"
        self.styles.background = "#0a0e14"
        self.styles.text_style = "bold"

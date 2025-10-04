"""ASCII Banner Widget"""

from textual.app import ComposeResult
from textual.widgets import Static


class ASCIIBanner(Static):
    """Cyberpunk-themed ASCII banner"""
    
    BANNER = """
██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗      ██╗   ██╗███████╗███████╗
██║     ██║████╗  ██║██║   ██║╚██╗██╔╝      ██║   ██║██╔════╝██╔════╝
██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ █████╗██║   ██║███████╗█████╗  
██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ ╚════╝██║   ██║╚════██║██╔══╝  
███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗      ╚██████╔╝███████║███████╗
╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝       ╚═════╝ ╚══════╝╚══════╝
                                                                       
    ▀█▀ █▀▀ █▀█ █▀▄▀█ █ █▄░█ ▄▀█ █░░   █░█ █▀ █▀▀ █▀█   █ █▄░█ ▀█▀ █▀▀ █▀█ █▀▀ ▄▀█ █▀▀ █▀▀
    ░█░ ██▄ █▀▄ █░▀░█ █ █░▀█ █▀█ █▄▄   █▄█ ▄█ ██▄ █▀▄   █ █░▀█ ░█░ ██▄ █▀▄ █▀░ █▀█ █▄▄ ██▄
    
    ╔═══════════════════════════════════════════════════════════════════╗
    ║   DESKTOP AUTOMATION FRAMEWORK v2.0 :: LINUX EDITION             ║
    ║   [POWERED BY ANTHROPIC CLAUDE & AT-SPI2]                        ║
    ╚═══════════════════════════════════════════════════════════════════╝
"""
    
    def __init__(self):
        super().__init__(self.BANNER)
        self.styles.text_align = "center"
        self.styles.color = "cyan"
        self.styles.text_style = "bold"
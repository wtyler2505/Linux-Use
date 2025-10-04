"""TUI Configuration"""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel
import os

class TUIConfig(BaseModel):
    """TUI configuration settings"""
    
    # Paths
    app_dir: Path = Path("/app")
    config_dir: Path = Path.home() / ".linux-use"
    log_dir: Path = Path.home() / ".linux-use" / "logs"
    cache_dir: Path = Path.home() / ".linux-use" / "cache"
    
    # API Settings
    anthropic_api_key: Optional[str] = None
    use_claude_max: bool = False
    
    # Agent Settings
    max_steps: int = 25
    max_consecutive_failures: int = 3
    use_vision: bool = False
    auto_minimize: bool = False
    
    # Monitoring
    refresh_rate: float = 1.0  # seconds
    max_log_lines: int = 1000
    
    # Advanced
    enable_recording: bool = True
    enable_remote_monitoring: bool = False
    remote_port: int = 8888
    
    class Config:
        env_prefix = "LINUX_USE_"
        
    def ensure_dirs(self):
        """Create necessary directories"""
        for dir_path in [self.config_dir, self.log_dir, self.cache_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def load(cls) -> 'TUIConfig':
        """Load configuration from environment and files"""
        config = cls()
        
        # Load from .env if exists
        env_file = config.app_dir / ".env"
        if env_file.exists():
            from dotenv import load_dotenv
            load_dotenv(env_file)
            
        # Override from environment
        config.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        config.ensure_dirs()
        return config

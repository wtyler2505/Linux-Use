"""TUI Configuration"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TUIConfig:
    """Configuration for Linux-Use TUI"""
    
    # API Keys
    anthropic_api_key: str = ""
    use_claude_max: bool = False
    
    # Agent settings
    max_steps: int = 25
    max_consecutive_failures: int = 3
    use_vision: bool = False
    auto_minimize: bool = True
    
    # Recording
    enable_recording: bool = True
    recording_dir: str = "/app/recordings"
    
    # Remote monitoring
    enable_remote_monitoring: bool = False
    remote_port: int = 8888
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "/app/logs/tui.log"
    
    @classmethod
    def load(cls) -> 'TUIConfig':
        """Load configuration from environment"""
        config = cls()
        
        # Load from environment
        config.anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        config.max_steps = int(os.environ.get('LINUX_USE_MAX_STEPS', '25'))
        config.max_consecutive_failures = int(os.environ.get('LINUX_USE_MAX_FAILURES', '3'))
        
        return config
    
    def save(self):
        """Save configuration to .env file"""
        env_file = Path("/app/.env")
        
        # Read existing content
        env_content = {}
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env_content[key] = value
        
        # Update with new values
        env_content['ANTHROPIC_API_KEY'] = self.anthropic_api_key
        env_content['LINUX_USE_MAX_STEPS'] = str(self.max_steps)
        env_content['LINUX_USE_MAX_FAILURES'] = str(self.max_consecutive_failures)
        
        # Write back
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
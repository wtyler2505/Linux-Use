"""Configuration Screen"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button, Input, Label, Switch, Select
from ..widgets.log_viewer import LogViewer
from ..config import TUIConfig
import os

class ConfigurationScreen(Screen):
    """System configuration and API key management"""
    
    CSS = """
    ConfigurationScreen {
        background: $surface;
    }
    
    #config-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    #config-header {
        width: 100%;
        height: 3;
        background: $surface-lighten-1;
        border: heavy $warning;
        content-align: center middle;
    }
    
    #config-content {
        width: 100%;
        height: 1fr;
        margin-top: 1;
    }
    
    #config-form {
        width: 50%;
        height: 100%;
        border: heavy $primary;
        background: $surface-lighten-1;
        padding: 2;
    }
    
    #config-log {
        width: 50%;
        height: 100%;
        border: heavy $primary;
        background: $surface;
    }
    
    .config-section {
        width: 100%;
        margin-bottom: 2;
    }
    
    .config-label {
        color: $secondary;
        text-style: bold;
        margin-bottom: 1;
    }
    
    Input {
        width: 100%;
        margin-bottom: 1;
    }
    
    #config-actions {
        width: 100%;
        height: auto;
        margin-top: 1;
        align: center middle;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical(id="config-container"):
            yield Static(
                "╭─── SYSTEM CONFIGURATION ─────────────────────────╮",
                id="config-header"
            )
            
            with Horizontal(id="config-content"):
                # Configuration form
                with ScrollableContainer(id="config-form"):
                    # API Keys section
                    yield Static("╭─ API KEYS ────────────────╮", classes="config-label")
                    
                    with Vertical(classes="config-section"):
                        yield Label("▶ Anthropic API Key:")
                        yield Input(
                            placeholder="sk-ant-...",
                            password=True,
                            id="input-anthropic-key"
                        )
                        
                        yield Label("▶ Use Claude Max (OAuth):")
                        yield Switch(id="switch-claude-max")
                    
                    # Agent settings
                    yield Static("\n╭─ AGENT SETTINGS ────────────╮", classes="config-label")
                    
                    with Vertical(classes="config-section"):
                        yield Label("▶ Max Steps:")
                        yield Input(placeholder="25", id="input-max-steps")
                        
                        yield Label("▶ Max Consecutive Failures:")
                        yield Input(placeholder="3", id="input-max-failures")
                        
                        yield Label("▶ Use Vision Mode:")
                        yield Switch(id="switch-vision")
                        
                        yield Label("▶ Auto Minimize IDE:")
                        yield Switch(id="switch-auto-minimize")
                    
                    # Advanced settings
                    yield Static("\n╭─ ADVANCED ────────────────╮", classes="config-label")
                    
                    with Vertical(classes="config-section"):
                        yield Label("▶ Enable Recording:")
                        yield Switch(id="switch-recording", value=True)
                        
                        yield Label("▶ Enable Remote Monitoring:")
                        yield Switch(id="switch-remote")
                        
                        yield Label("▶ Remote Port:")
                        yield Input(placeholder="8888", id="input-remote-port")
                
                # Log panel
                with Container(id="config-log"):
                    yield LogViewer(id="config-log-viewer", max_lines=300)
            
            with Horizontal(id="config-actions"):
                yield Button("✓ SAVE CONFIGURATION", id="btn-save", variant="success")
                yield Button("🔄 LOAD DEFAULTS", id="btn-defaults")
                yield Button("◀ BACK", id="btn-back")
    
    def on_mount(self) -> None:
        """Called when screen is mounted"""
        log = self.query_one("#config-log-viewer", LogViewer)
        log.log_system("Configuration panel loaded")
        log.log_info("Update settings and click SAVE")
        
        # Load current configuration
        self.load_config()
    
    def load_config(self) -> None:
        """Load current configuration"""
        log = self.query_one("#config-log-viewer", LogViewer)
        log.log_info("Loading current configuration...")
        
        config = TUIConfig.load()
        
        # Populate form
        if config.anthropic_api_key:
            self.query_one("#input-anthropic-key", Input).value = config.anthropic_api_key
            log.log_success("Anthropic API key loaded")
        
        self.query_one("#switch-claude-max", Switch).value = config.use_claude_max
        self.query_one("#input-max-steps", Input).value = str(config.max_steps)
        self.query_one("#input-max-failures", Input).value = str(config.max_consecutive_failures)
        self.query_one("#switch-vision", Switch).value = config.use_vision
        self.query_one("#switch-auto-minimize", Switch).value = config.auto_minimize
        self.query_one("#switch-recording", Switch).value = config.enable_recording
        self.query_one("#switch-remote", Switch).value = config.enable_remote_monitoring
        self.query_one("#input-remote-port", Input).value = str(config.remote_port)
        
        log.log_success("Configuration loaded successfully")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        log = self.query_one("#config-log-viewer", LogViewer)
        
        if event.button.id == "btn-save":
            log.log_info("Saving configuration...")
            self.save_config()
        
        elif event.button.id == "btn-defaults":
            log.log_warning("Loading default configuration...")
            config = TUIConfig()
            log.log_success("Defaults loaded")
        
        elif event.button.id == "btn-back":
            self.app.pop_screen()
    
    def save_config(self) -> None:
        """Save configuration to .env file"""
        log = self.query_one("#config-log-viewer", LogViewer)
        
        try:
            # Get values from form
            api_key = self.query_one("#input-anthropic-key", Input).value
            
            # Update .env file
            env_file = "/app/.env"
            env_content = ""
            
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    env_content = f.read()
            
            # Update or add API key
            if "ANTHROPIC_API_KEY" in env_content:
                lines = env_content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('ANTHROPIC_API_KEY'):
                        lines[i] = f"ANTHROPIC_API_KEY={api_key}"
                env_content = '\n'.join(lines)
            else:
                env_content += f"\nANTHROPIC_API_KEY={api_key}\n"
            
            # Save
            with open(env_file, 'w') as f:
                f.write(env_content)
            
            log.log_success("✓ Configuration saved to .env")
            log.log_info("Restart agent to apply changes")
            
        except Exception as e:
            log.log_error(f"Failed to save configuration: {e}")

"""Advanced Monitoring Screen"""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Tree, Label
from ..widgets.log_viewer import LogViewer
import psutil
import time

class MonitoringScreen(Screen):
    """Live agent monitoring with UI tree visualization"""
    
    CSS = """
    MonitoringScreen {
        background: $surface;
    }
    
    #mon-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    #mon-header {
        width: 100%;
        height: 3;
        background: $surface-lighten-1;
        border: heavy $secondary;
        content-align: center middle;
    }
    
    #mon-content {
        width: 100%;
        height: 1fr;
        margin-top: 1;
    }
    
    #tree-panel {
        width: 50%;
        height: 100%;
        border: heavy $primary;
        background: $surface-lighten-1;
        padding: 1;
    }
    
    #activity-panel {
        width: 50%;
        height: 100%;
        border: heavy $primary;
        background: $surface;
    }
    
    #mon-actions {
        width: 100%;
        height: auto;
        margin-top: 1;
        align: center middle;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        with Vertical(id="mon-container"):
            yield Static(
                "╭─── LIVE MONITORING STATION ────────────────────────╮",
                id="mon-header"
            )
            
            with Horizontal(id="mon-content"):
                # UI Tree panel
                with Container(id="tree-panel"):
                    yield Static("▶ UI ELEMENT TREE", classes="metric-label")
                    tree = Tree("🖥️ Root")
                    tree.root.expand()
                    yield tree
                
                # Activity log
                with Container(id="activity-panel"):
                    yield LogViewer(id="mon-log", max_lines=500)
            
            with Horizontal(id="mon-actions"):
                yield Button("🔄 REFRESH TREE", id="btn-refresh", variant="primary")
                yield Button("📸 CAPTURE STATE", id="btn-capture")
                yield Button("◀ BACK", id="btn-back")
    
    def on_mount(self) -> None:
        """Called when screen is mounted"""
        log = self.query_one("#mon-log", LogViewer)
        log.log_system("═" * 50)
        log.log_system("MONITORING STATION ONLINE")
        log.log_system("═" * 50)
        log.log_info("Initializing UI tree scanner...")
        
        self.refresh_tree()
        
        # Start monitoring updates
        self.set_interval(5.0, self.update_monitoring)
    
    def refresh_tree(self) -> None:
        """Refresh UI element tree"""
        log = self.query_one("#mon-log", LogViewer)
        tree = self.query_one(Tree)
        
        log.log_info("Scanning for UI elements...")
        
        try:
            # Try to get actual UI tree (requires AT-SPI)
            import pyatspi
            log.log_success("AT-SPI2 available - scanning desktop")
            
            tree.clear()
            root = tree.root
            
            # Get desktop
            desktop = pyatspi.Registry.getDesktop(0)
            
            # Scan applications
            for i in range(min(desktop.childCount, 10)):  # Limit to first 10 apps
                try:
                    app = desktop.getChildAtIndex(i)
                    if app and app.name:
                        app_node = root.add(f"💻 {app.name}")
                        
                        # Add some children
                        for j in range(min(app.childCount, 5)):
                            try:
                                child = app.getChildAtIndex(j)
                                if child:
                                    role = child.getRole()
                                    role_name = role.value_name if hasattr(role, 'value_name') else str(role)
                                    app_node.add(f"▪ {role_name}: {child.name or 'unnamed'}")
                            except Exception:
                                continue
                except Exception:
                    continue
            
            log.log_success(f"Scanned {desktop.childCount} applications")
            
        except ImportError:
            log.log_warning("AT-SPI2 not available - showing system processes")
            
            # Fallback: show system processes
            tree.clear()
            root = tree.root
            
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                try:
                    if proc.info['status'] == 'running':
                        root.add(f"⚙️ {proc.info['name']} (PID: {proc.info['pid']})")
                except Exception:
                    continue
            
            log.log_info("Showing active processes as fallback")
        
        except Exception as e:
            log.log_error(f"Tree scan error: {e}")
    
    def update_monitoring(self) -> None:
        """Update monitoring data periodically"""
        log = self.query_one("#mon-log", LogViewer)
        
        # Log system stats
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        
        log.log_system(f"CPU: {cpu:.1f}% | RAM: {mem.percent:.1f}% | {time.strftime('%H:%M:%S')}")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "btn-refresh":
            log = self.query_one("#mon-log", LogViewer)
            log.log_info("Refreshing UI tree...")
            self.refresh_tree()
        
        elif event.button.id == "btn-capture":
            log = self.query_one("#mon-log", LogViewer)
            log.log_success("State captured (not yet implemented)")
        
        elif event.button.id == "btn-back":
            self.app.pop_screen()

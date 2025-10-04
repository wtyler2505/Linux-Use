from linux_use.agent.desktop.config import EXCLUDED_APPS, AVOIDED_APPS, BROWSER_NAMES
from linux_use.agent.desktop.views import DesktopState, App, Size, Status
from linux_use.agent.tree.service import Tree
from PIL.Image import Image as PILImage
from contextlib import contextmanager
from fuzzywuzzy import process
from typing import Optional
from psutil import Process
from time import sleep
from io import BytesIO
from PIL import Image
import subprocess
import pyautogui
import base64
import distro
import screeninfo
import os

# Try to import X11 libraries
try:
    from Xlib import display, X
    from Xlib.ext import randr
    XLIB_AVAILABLE = True
except ImportError:
    XLIB_AVAILABLE = False
    print("Warning: python-xlib not available. Some features may be limited.")

class Desktop:
    def __init__(self):
        self.encoding = 'utf-8'
        self.desktop_state = None
        if XLIB_AVAILABLE:
            try:
                self.display = display.Display()
                self.screen = self.display.screen()
                self.root = self.screen.root
            except Exception as e:
                print(f"Warning: Could not initialize X11 display: {e}")
                self.display = None
                self.screen = None
                self.root = None
        else:
            self.display = None
            self.screen = None
            self.root = None
        
    def get_state(self, use_vision: bool = False) -> DesktopState:
        tree = Tree(self)
        active_app, apps = self.get_apps()
        tree_state = tree.get_state()
        if use_vision:
            annotated_screenshot = tree.annotated_screenshot(tree_state.interactive_nodes, scale=0.5)
            screenshot = self.screenshot_in_bytes(annotated_screenshot)
        else:
            screenshot = None
        self.desktop_state = DesktopState(
            apps=apps,
            active_app=active_app,
            screenshot=screenshot,
            tree_state=tree_state
        )
        return self.desktop_state
    
    def get_active_app(self, apps: list[App]) -> App | None:
        if len(apps) > 0 and apps[0].status != Status.MINIMIZED:
            return apps[0]
        return None
    
    def get_cursor_location(self) -> tuple[int, int]:
        position = pyautogui.position()
        return (position.x, position.y)
    
    def execute_command(self, command: str) -> tuple[str, int]:
        """Execute bash command and return output with status code."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                executable='/bin/bash',
                capture_output=True,
                text=True,
                timeout=25,
                cwd=os.path.expanduser('~')
            )
            stdout = result.stdout
            stderr = result.stderr
            return (stdout or stderr, result.returncode)
        except subprocess.TimeoutExpired:
            return ('Command execution timed out', 1)
        except Exception as e:
            return (f'Command execution failed: {e}', 1)
    
    def get_linux_distro(self) -> str:
        """Get Linux distribution name and version."""
        try:
            dist_name = distro.name()
            dist_version = distro.version()
            return f"{dist_name} {dist_version}"
        except Exception:
            return "Linux"
    
    def get_user_account_type(self) -> str:
        """Detect local vs LDAP/domain account."""
        try:
            username = os.environ.get('USER', '')
            # Check if user exists in /etc/passwd
            result = subprocess.run(
                ['getent', 'passwd', username],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # Check if it's from LDAP or local
                result_ldap = subprocess.run(
                    ['getent', '-s', 'ldap', 'passwd', username],
                    capture_output=True,
                    text=True
                )
                if result_ldap.returncode == 0:
                    return "LDAP/Domain Account"
                return "Local Account"
            return "Unknown Account Type"
        except Exception:
            return "Local Account"
    
    def get_dpi_scaling(self) -> float:
        """Get DPI scaling factor for HiDPI displays."""
        try:
            # Try using xrandr
            result = subprocess.run(
                ['xrandr', '--current'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # Parse DPI from output
                for line in result.stdout.split('\n'):
                    if 'connected' in line and 'primary' in line:
                        # Default to 1.0 if cannot parse
                        return 1.0
            
            # Fallback: Try to get from Xlib if available
            if XLIB_AVAILABLE and self.screen:
                dpi = (self.screen.width_in_pixels / (self.screen.width_in_mms / 25.4))
                return dpi / 96.0
            
            return 1.0
        except Exception:
            return 1.0
    
    def get_screen_resolution(self) -> Size:
        """Get primary screen resolution."""
        try:
            monitors = screeninfo.get_monitors()
            if monitors:
                primary = monitors[0]
                return Size(width=primary.width, height=primary.height)
        except Exception:
            pass
        
        # Fallback to pyautogui
        try:
            size = pyautogui.size()
            return Size(width=size.width, height=size.height)
        except Exception:
            return Size(width=1920, height=1080)
    
    def get_apps(self) -> tuple[App | None, list[App]]:
        """Enumerate windows using wmctrl."""
        try:
            sleep(0.5)
            # Use wmctrl to list windows
            result = subprocess.run(
                ['wmctrl', '-lGpx'],
                capture_output=True,
                text=True
            )
            
            apps = []
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for depth, line in enumerate(lines):
                    if not line.strip():
                        continue
                    
                    parts = line.split(None, 9)
                    if len(parts) < 10:
                        continue
                    
                    win_id = parts[0]
                    desktop_num = parts[1]
                    pid = parts[2]
                    x = int(parts[3])
                    y = int(parts[4])
                    width = int(parts[5])
                    height = int(parts[6])
                    win_class = parts[7]
                    host = parts[8]
                    title = parts[9] if len(parts) > 9 else ""
                    
                    # Skip excluded windows
                    if win_class in EXCLUDED_APPS or win_class in AVOIDED_APPS:
                        continue
                    
                    # Skip desktop and panels
                    if desktop_num == '-1':
                        continue
                    
                    # Determine status
                    status = Status.NORMAL
                    if width <= 0 or height <= 0:
                        status = Status.HIDDEN
                    elif width < 100 or height < 100:
                        status = Status.MINIMIZED
                    
                    size = Size(width=width, height=height)
                    
                    apps.append(App(
                        name=title,
                        depth=depth,
                        status=status,
                        size=size,
                        handle=int(win_id, 16)  # Convert hex to int
                    ))
            
            active_app = self.get_active_app(apps)
            apps = apps[1:] if len(apps) > 1 else []
            return (active_app, apps)
        except Exception as ex:
            print(f"Error getting windows: {ex}")
            return (None, [])
    
    def is_app_browser(self, node) -> bool:
        """Check if a window/app is a browser."""
        try:
            if hasattr(node, 'ProcessId'):
                process = Process(node.ProcessId)
                return process.name() in BROWSER_NAMES
            return False
        except Exception:
            return False
    
    def get_default_language(self) -> str:
        """Get system default language."""
        try:
            lang = os.environ.get('LANG', 'en_US.UTF-8')
            # Parse language
            if lang:
                lang_code = lang.split('.')[0]
                return lang_code.replace('_', ' ')
            return "English (US)"
        except Exception:
            return "English (US)"
    
    def resize_app(self, size: tuple[int, int] = None, loc: tuple[int, int] = None) -> tuple[str, int]:
        """Resize active application window."""
        active_app = self.desktop_state.active_app
        if active_app is None:
            return "No active app found", 1
        if active_app.status == Status.MINIMIZED:
            return f"{active_app.name} is minimized", 1
        elif active_app.status == Status.MAXIMIZED:
            return f"{active_app.name} is maximized", 1
        else:
            try:
                win_id = hex(active_app.handle)
                if size:
                    width, height = size
                else:
                    width, height = active_app.size.width, active_app.size.height
                
                if loc:
                    x, y = loc
                else:
                    x, y = 0, 0
                
                # Use wmctrl to resize
                result = subprocess.run(
                    ['wmctrl', '-i', '-r', win_id, '-e', f'0,{x},{y},{width},{height}'],
                    capture_output=True
                )
                
                if result.returncode == 0:
                    return (f'{active_app.name} resized to {width}x{height} at {x},{y}.', 0)
                return ('Failed to resize window.', 1)
            except Exception as e:
                return (f'Error resizing window: {e}', 1)
    
    def is_app_running(self, name: str) -> bool:
        """Check if an app is currently running."""
        apps = {app.name: app for app in [self.desktop_state.active_app] + self.desktop_state.apps if app is not None}
        return process.extractOne(name, list(apps.keys()), score_cutoff=60) is not None
    
    def launch_app(self, name: str) -> tuple[str, int]:
        """Launch an application."""
        try:
            # Try with gtk-launch first
            result = subprocess.run(
                ['gtk-launch', name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                sleep(1.5)
                return f'{name.title()} launched.', 0
            
            # Fallback: try direct command
            result = subprocess.run(
                [name],
                capture_output=True,
                text=True,
                start_new_session=True
            )
            
            if result.returncode == 0 or result.returncode is None:
                sleep(1.5)
                return f'{name.title()} launched.', 0
            
            return f'Failed to launch {name.title()}.', 1
        except Exception as e:
            return f'Error launching {name}: {e}', 1
    
    def switch_app(self, name: str) -> tuple[str, int]:
        """Switch to a specific application window."""
        apps = {app.name: app for app in [self.desktop_state.active_app] + self.desktop_state.apps if app is not None}
        matched_app: Optional[tuple[str, float]] = process.extractOne(name, list(apps.keys()), score_cutoff=70)
        
        if matched_app is None:
            return (f'Application {name.title()} not found.', 1)
        
        app_name, _ = matched_app
        app = apps.get(app_name)
        
        try:
            win_id = hex(app.handle)
            result = subprocess.run(
                ['wmctrl', '-i', '-a', win_id],
                capture_output=True
            )
            
            if result.returncode == 0:
                return (f'Switched to {app_name.title()} window.', 0)
            return (f'Failed to switch to {app_name.title()}.', 1)
        except Exception as e:
            return (f'Error switching to {app_name}: {e}', 1)
    
    def screenshot_in_bytes(self, screenshot: PILImage) -> bytes:
        """Convert PIL Image to base64 data URI."""
        buffer = BytesIO()
        screenshot.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        data_uri = f"data:image/png;base64,{img_base64}"
        return data_uri
    
    def get_screenshot(self, scale: float = 0.7) -> Image.Image:
        """Capture screenshot of the desktop."""
        screenshot = pyautogui.screenshot()
        size = (int(screenshot.width * scale), int(screenshot.height * scale))
        screenshot.thumbnail(size=size, resample=Image.Resampling.LANCZOS)
        return screenshot
    
    @contextmanager
    def auto_minimize(self):
        """Auto-minimize the current window (IDE) while agent works."""
        try:
            # Get current active window
            result = subprocess.run(
                ['xdotool', 'getactivewindow'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                win_id = result.stdout.strip()
                # Minimize it
                subprocess.run(['xdotool', 'windowminimize', win_id])
                yield
            else:
                yield
        except Exception:
            yield
        finally:
            # Restore window
            try:
                if win_id:
                    subprocess.run(['xdotool', 'windowactivate', win_id])
            except Exception:
                pass
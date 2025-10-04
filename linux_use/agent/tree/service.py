from linux_use.agent.tree.config import INTERACTIVE_CONTROL_TYPE_NAMES, INFORMATIVE_CONTROL_TYPE_NAMES
from linux_use.agent.tree.views import TreeElementNode, TextElementNode, ScrollElementNode, Center, BoundingBox, TreeState
from linux_use.agent.desktop.config import AVOIDED_APPS, EXCLUDED_APPS
from PIL import Image, ImageFont, ImageDraw
from typing import TYPE_CHECKING
from time import sleep
import random

if TYPE_CHECKING:
    from linux_use.agent.desktop.service import Desktop

# Try to import AT-SPI2 libraries
try:
    import pyatspi
    ATSPI_AVAILABLE = True
except ImportError:
    ATSPI_AVAILABLE = False
    print("Warning: pyatspi not available. UI tree functionality will be limited.")

class Tree:
    def __init__(self, desktop: 'Desktop'):
        self.desktop = desktop
        self.screen_resolution = self.desktop.get_screen_resolution()

    def get_state(self) -> TreeState:
        """Get the current UI tree state."""
        sleep(0.1)
        
        if ATSPI_AVAILABLE:
            try:
                interactive_nodes, informative_nodes, scrollable_nodes = self.get_nodes_atspi()
            except Exception as e:
                print(f"AT-SPI error: {e}. Falling back to basic mode.")
                interactive_nodes, informative_nodes, scrollable_nodes = self.get_nodes_fallback()
        else:
            interactive_nodes, informative_nodes, scrollable_nodes = self.get_nodes_fallback()
        
        return TreeState(
            interactive_nodes=interactive_nodes,
            informative_nodes=informative_nodes,
            scrollable_nodes=scrollable_nodes
        )
    
    def get_nodes_fallback(self) -> tuple[list[TreeElementNode], list[TextElementNode], list[ScrollElementNode]]:
        """Fallback method when AT-SPI is not available - returns empty lists."""
        # In fallback mode, we don't have detailed UI tree information
        # The agent will rely more on vision mode or manual coordinate specification
        return ([], [], [])
    
    def get_nodes_atspi(self) -> tuple[list[TreeElementNode], list[TextElementNode], list[ScrollElementNode]]:
        """Get UI nodes using AT-SPI2 accessibility API."""
        interactive_nodes = []
        informative_nodes = []
        scrollable_nodes = []
        
        try:
            # Get the desktop accessibility object
            desktop = pyatspi.Registry.getDesktop(0)
            
            # Iterate through all applications
            for app_index in range(desktop.childCount):
                try:
                    app = desktop.getChildAtIndex(app_index)
                    if not app:
                        continue
                    
                    app_name = app.name
                    
                    # Skip excluded apps
                    if app_name in EXCLUDED_APPS or app_name in AVOIDED_APPS:
                        continue
                    
                    # Recursively traverse the application tree
                    self._traverse_accessible(
                        app, app_name, 
                        interactive_nodes, 
                        informative_nodes, 
                        scrollable_nodes
                    )
                except Exception as e:
                    print(f"Error processing app at index {app_index}: {e}")
                    continue
        except Exception as e:
            print(f"Error accessing AT-SPI desktop: {e}")
        
        return (interactive_nodes, informative_nodes, scrollable_nodes)
    
    def _traverse_accessible(self, accessible, app_name, interactive_nodes, informative_nodes, scrollable_nodes, depth=0, max_depth=20):
        """Recursively traverse accessible tree."""
        if depth > max_depth:
            return
        
        try:
            # Get role and state
            role = accessible.getRole()
            state_set = accessible.getState()
            
            # Skip if not visible or not showing
            if not (state_set.contains(pyatspi.STATE_VISIBLE) and state_set.contains(pyatspi.STATE_SHOWING)):
                return
            
            # Get bounding box
            try:
                component = accessible.queryComponent()
                extents = component.getExtents(pyatspi.DESKTOP_COORDS)
                x, y, width, height = extents.x, extents.y, extents.width, extents.height
                
                # Skip if off-screen or too small
                if width <= 0 or height <= 0 or x < 0 or y < 0:
                    return
                
                center_x = x + width // 2
                center_y = y + height // 2
                
                bounding_box = BoundingBox(
                    left=x, top=y, right=x+width, bottom=y+height,
                    width=width, height=height
                )
                center = Center(x=center_x, y=center_y)
            except Exception:
                # Can't get component interface, skip
                return
            
            # Get name and description
            name = accessible.name or ""
            description = accessible.description or ""
            
            # Check if it's interactive
            is_enabled = state_set.contains(pyatspi.STATE_ENABLED)
            is_focusable = state_set.contains(pyatspi.STATE_FOCUSABLE)
            
            # Determine node type based on role
            role_name = role.value_name if hasattr(role, 'value_name') else str(role)
            
            # Interactive elements
            if self._is_interactive_role(role) and is_enabled:
                # Get value if available
                value = ""
                try:
                    value_iface = accessible.queryValue()
                    value = str(value_iface.currentValue)
                except Exception:
                    pass
                
                interactive_nodes.append(TreeElementNode(
                    name=name or role_name,
                    control_type=role_name.replace('ROLE_', '').title(),
                    value=value,
                    shortcut="",
                    bounding_box=bounding_box,
                    center=center,
                    app_name=app_name
                ))
            
            # Text/informative elements
            elif self._is_text_role(role):
                if name or accessible.text:
                    try:
                        text_content = accessible.queryText()
                        text = text_content.getText(0, text_content.characterCount) if text_content else name
                    except Exception:
                        text = name
                    
                    if text.strip():
                        informative_nodes.append(TextElementNode(
                            name=text.strip(),
                            app_name=app_name
                        ))
            
            # Scrollable elements
            if self._is_scrollable(accessible):
                scrollable_nodes.append(ScrollElementNode(
                    name=name or role_name,
                    app_name=app_name,
                    control_type=role_name.replace('ROLE_', '').title(),
                    bounding_box=bounding_box,
                    center=center,
                    horizontal_scrollable=False,  # Would need more detailed detection
                    horizontal_scroll_percent=0,
                    vertical_scrollable=True,
                    vertical_scroll_percent=50,  # Default to middle
                    is_focused=state_set.contains(pyatspi.STATE_FOCUSED)
                ))
            
            # Recursively process children
            for i in range(accessible.childCount):
                try:
                    child = accessible.getChildAtIndex(i)
                    if child:
                        self._traverse_accessible(
                            child, app_name, 
                            interactive_nodes, informative_nodes, scrollable_nodes,
                            depth + 1, max_depth
                        )
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"Error traversing accessible at depth {depth}: {e}")
    
    def _is_interactive_role(self, role) -> bool:
        """Check if role is interactive."""
        interactive_roles = [
            pyatspi.ROLE_PUSH_BUTTON,
            pyatspi.ROLE_TOGGLE_BUTTON,
            pyatspi.ROLE_CHECK_BOX,
            pyatspi.ROLE_RADIO_BUTTON,
            pyatspi.ROLE_MENU_ITEM,
            pyatspi.ROLE_CHECK_MENU_ITEM,
            pyatspi.ROLE_RADIO_MENU_ITEM,
            pyatspi.ROLE_TEXT,
            pyatspi.ROLE_ENTRY,
            pyatspi.ROLE_PASSWORD_TEXT,
            pyatspi.ROLE_COMBO_BOX,
            pyatspi.ROLE_LINK,
            pyatspi.ROLE_LIST_ITEM,
            pyatspi.ROLE_TAB,
            pyatspi.ROLE_PAGE_TAB,
            pyatspi.ROLE_SLIDER,
            pyatspi.ROLE_SPIN_BUTTON,
        ]
        return role in interactive_roles
    
    def _is_text_role(self, role) -> bool:
        """Check if role is text/informative."""
        text_roles = [
            pyatspi.ROLE_LABEL,
            pyatspi.ROLE_HEADING,
            pyatspi.ROLE_PARAGRAPH,
            pyatspi.ROLE_STATIC,
            pyatspi.ROLE_TEXT,
        ]
        return role in text_roles
    
    def _is_scrollable(self, accessible) -> bool:
        """Check if element is scrollable."""
        try:
            # Check for scroll bar or scrollable component
            role = accessible.getRole()
            if role in [pyatspi.ROLE_SCROLL_PANE, pyatspi.ROLE_VIEWPORT]:
                return True
            # Could also check for scroll interfaces here
            return False
        except Exception:
            return False
    
    def get_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def annotated_screenshot(self, nodes: list[TreeElementNode], scale: float = 0.7) -> Image.Image:
        """Create annotated screenshot with bounding boxes."""
        screenshot = self.desktop.get_screenshot(scale=scale)
        sleep(0.10)
        
        # Add padding
        padding = 20
        width = screenshot.width + (2 * padding)
        height = screenshot.height + (2 * padding)
        padded_screenshot = Image.new("RGB", (width, height), color=(255, 255, 255))
        padded_screenshot.paste(screenshot, (padding, padding))

        draw = ImageDraw.Draw(padded_screenshot)
        font_size = 12
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except IOError:
            font = ImageFont.load_default()

        def draw_annotation(label, node: TreeElementNode):
            box = node.bounding_box
            color = self.get_random_color()

            # Scale and pad the bounding box
            adjusted_box = (
                int(box.left * scale) + padding,
                int(box.top * scale) + padding,
                int(box.right * scale) + padding,
                int(box.bottom * scale) + padding
            )
            # Draw bounding box
            draw.rectangle(adjusted_box, outline=color, width=2)

            # Label dimensions
            label_width = draw.textlength(str(label), font=font)
            label_height = font_size
            left, top, right, bottom = adjusted_box

            # Label position above bounding box
            label_x1 = right - label_width
            label_y1 = top - label_height - 4
            label_x2 = label_x1 + label_width
            label_y2 = label_y1 + label_height + 4

            # Draw label background and text
            draw.rectangle([(label_x1, label_y1), (label_x2, label_y2)], fill=color)
            draw.text((label_x1 + 2, label_y1 + 2), str(label), fill=(255, 255, 255), font=font)

        # Draw annotations
        for idx, node in enumerate(nodes):
            draw_annotation(idx, node)
        
        return padded_screenshot

from pydantic import BaseModel, Field
from typing import Literal, Optional

class SharedBaseModel(BaseModel):
    class Config:
        extra = 'allow'

class App(SharedBaseModel):
    mode: Literal['launch', 'resize', 'switch'] = Field(
        ...,
        description="Operation mode: 'launch' opens app from Start Menu, 'resize' adjusts active window size/position, 'switch' brings specific window into focus",
        examples=['launch']
    )
    name: Optional[str] = Field(
        description="Exact application name as it appears in Start Menu or window title (required for launch/switch modes)",
        examples=['notepad', 'chrome', 'New tab - Personal - Microsoft Edge'],
        default=None
    )
    loc: Optional[tuple[int, int]] = Field(
        description="Target (x, y) coordinates for window top-left corner position (required for resize mode)",
        examples=[(0, 0)],
        default=None
    )
    size: Optional[tuple[int, int]] = Field(
        description="Target (width, height) dimensions in pixels for window size (required for resize mode)",
        examples=[(1920, 1080)],
        default=None
    )

class Done(SharedBaseModel):
    answer: str = Field(
        ...,
        description="Comprehensive final answer in markdown format containing all requested information and task results",
        examples=["## Task Completed\n\nThe task has been completed successfully. Here are the results:\n- Item 1\n- Item 2"]
    )

class Memory(SharedBaseModel):
    mode: Literal['view', 'read', 'write', 'delete', 'update'] = Field(
        description="Operation mode: view (list files), read (get content), write (create), update (modify), delete (remove)"
    )
    path: Optional[str] = Field(
        None,
        description="Relative path from .memories directory (e.g., 'notes.md' or 'project/data.md'). Required for read, write, update, delete modes."
    )
    content: Optional[str] = Field(
        None,
        description="Content to write or insert. Required for write mode and insert operation."
    )
    operation: Optional[Literal['replace', 'insert']] = Field(
        'replace',
        description="Update operation type: replace (str replacement), insert (at line)"
    )
    old_str: Optional[str] = Field(
        None,
        description="String to find and replace. Required when operation='replace'."
    )
    new_str: Optional[str] = Field(
        None,
        description="String to replace old_str with. Required when operation='replace'."
    )
    line_number: Optional[int] = Field(
        None,
        description="Line number for insertion (0-indexed). Required when operation='insert'."
    )
    read_range: Optional[tuple[int, int]] = Field(
        None,
        description="Range of lines to read (start, end) - both 0-indexed, end is exclusive. Example: (0, 10) reads lines 0-9. Optional for read mode."
    )

class Click(SharedBaseModel):
    loc: tuple[int, int] = Field(
        ...,
        description="(x, y) pixel coordinates within the target element's bounding box to perform click action",
        examples=[(640, 360), (100, 200)]
    )
    button: Literal['left', 'right', 'middle'] = Field(
        description="Mouse button to use: 'left' for selection/activation, 'right' for context menus, 'middle' for browser-specific actions",
        default='left',
        examples=['left', 'right']
    )
    clicks: Literal[0, 1, 2] = Field(
        description="Click count: 0=hover only (no click), 1=single click (select/focus), 2=double click (open/activate)",
        default=1,
        examples=[1, 2]
    )

class Shell(SharedBaseModel):
    command: str = Field(
        ...,
        description="PowerShell command to execute. Working directory is set to user's HOME. Returns output and exit status code",
        examples=[
            'Get-Process',
            'ls',
            'Get-ChildItem -Path C:\\Users -Recurse',
            'echo "Hello World"'
        ]
    )

class Type(SharedBaseModel):
    loc: tuple[int, int] = Field(
        ...,
        description="(x, y) pixel coordinates within the target input element's bounding box where text will be entered",
        examples=[(640, 360), (200, 150)]
    )
    text: str = Field(
        ...,
        description="Text string to type into the focused element",
        examples=['hello world', 'user@example.com', 'search query']
    )
    clear: Literal['true', 'false'] = Field(
        description="Whether to clear existing text before typing: 'true' replaces all content, 'false' appends to existing text",
        default='false',
        examples=['true', 'false']
    )
    caret_position: Literal['start', 'idle', 'end'] = Field(
        description="Caret positioning before typing: 'start' moves to beginning, 'end' moves to end, 'idle' leaves at current position",
        default='idle',
        examples=['start', 'end', 'idle']
    )
    press_enter: Literal['true', 'false'] = Field(
        description="Whether to press Enter key after typing text: 'true' submits/confirms input, 'false' leaves cursor in field",
        default='false',
        examples=['true', 'false']
    )

class Scroll(SharedBaseModel):
    loc: tuple[int, int] | None = Field(
        description="(x, y) pixel coordinates where scroll action occurs. If None, scrolls at current cursor position",
        default=None,
        examples=[(640, 360), (800, 400), None]
    )
    type: Literal['horizontal', 'vertical'] = Field(
        description="Scroll direction type: 'vertical' for up/down scrolling, 'horizontal' for left/right scrolling",
        default='vertical',
        examples=['vertical', 'horizontal']
    )
    direction: Literal['up', 'down', 'left', 'right'] = Field(
        description="Scroll direction: 'up'/'down' for vertical, 'left'/'right' for horizontal movement through content",
        default='down',
        examples=['down', 'up', 'right']
    )
    wheel_times: int = Field(
        description="Number of scroll wheel increments (1 wheel ≈ 3-5 lines of text). Higher values scroll further",
        default=1,
        examples=[1, 3, 5, 10]
    )

class Drag(SharedBaseModel):
    from_loc: tuple[int, int] = Field(
        ...,
        description="(x, y) pixel coordinates of drag operation starting point",
        examples=[(100, 100), (300, 200)]
    )
    to_loc: tuple[int, int] = Field(
        ...,
        description="(x, y) pixel coordinates of drag operation ending point/destination",
        examples=[(500, 500), (800, 600)]
    )

class Move(SharedBaseModel):
    to_loc: tuple[int, int] = Field(
        ...,
        description="(x, y) pixel coordinates to move mouse cursor to without clicking. Used for hovering or positioning",
        examples=[(640, 360), (100, 100)]
    )

class Shortcut(SharedBaseModel):
    shortcut: str = Field(
        ...,
        description="Keyboard shortcut to execute. Use '+' to separate simultaneous keys (e.g., 'ctrl+c'). Single keys work too (e.g., 'enter')",
        examples=['win', 'enter', 'ctrl+c', 'alt+tab', 'ctrl+shift+n', 'escape']
    )

class Wait(SharedBaseModel):
    duration: int = Field(
        ...,
        description="Time to pause execution in seconds. Use for waiting on app launches, page loads, or animations to complete",
        examples=[2, 5, 10]
    )

class Scrape(SharedBaseModel):
    url: str = Field(
        ...,
        description="Full webpage URL including protocol (http:// or https://) to fetch and convert to markdown format",
        examples=['https://google.com', 'https://example.com/page', 'http://localhost:8080']
    )
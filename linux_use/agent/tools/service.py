from linux_use.agent.tools.views import Click, Type, Scroll, Drag, Move, Shortcut, Wait, Scrape, Done, Shell, Memory, App
from linux_use.agent.desktop.service import Desktop
from markdownify import markdownify
from typing import Literal,Optional
from langchain.tools import tool
from pathlib import Path
import pyautogui as pg
import requests

pg.FAILSAFE=False
pg.PAUSE=1.0

memory_path=Path.cwd()/'.memories'

@tool('Done Tool',args_schema=Done)
def done_tool(answer:str,**kwargs):
    '''
    Signals task completion and provides the final answer to the user.
    
    Use this tool when you have successfully completed the requested task and have 
    a comprehensive answer ready. The answer should be well-formatted in markdown 
    and include all relevant information the user requested.
    '''
    return answer

@tool('App Tool',args_schema=App)
def app_tool(mode:Literal['launch','resize','switch'],name:Optional[str]=None,loc:Optional[tuple[int,int]]=None,size:Optional[tuple[int,int]]=None,**kwargs)->str:
    '''
    Manages Windows applications through launch, resize, and window switching operations.
    
    Modes:
        - launch: Opens an application from the Windows Start Menu by name
        - resize: Adjusts the active application window's size and position
        - switch: Brings a specific application window into focus
    
    Use this tool to control application lifecycle and window management during task execution.
    '''
    desktop:Desktop=kwargs['desktop']
    match mode:
        case 'launch':
            response,status=desktop.launch_app(name)
            if status!=0:
                return response
            consecutive_waits=3
            for _ in range(consecutive_waits):
                if not desktop.is_app_running(name):
                    pg.sleep(1.25)
                else:
                    return f'{name.title()} launched.'
            return f'Launching {name.title()} wait for it to come load.'
        case 'resize':
            _,status=desktop.resize_app(size=size,loc=loc)
            if status!=0:
                return f'Failed to resize window.'
            else:
                return f'Window resized successfully.'
        case 'switch':
            _,status=desktop.switch_app(name)
            if status!=0:
                return f'Failed to switch to {name.title()} window.'
            else:
                return f'Switched to {name.title()} window.'

@tool('Memory Tool',args_schema=Memory)
def memory_tool(mode: Literal['view','read','write','delete','update'],path: Optional[str] = None,
    content: Optional[str] = None,operation: Optional[Literal['replace', 'insert']] = 'replace',
    old_str: Optional[str] = None,new_str: Optional[str] = None,line_number: Optional[int] = None,
    read_range: Optional[tuple[int, int]] = None,**kwargs) -> str:
    '''
    Persistent file-based storage system for managing information across different task stages.
    
    Use this tool to:
        - Store important findings and data as md files in the .memories directory
        - Maintain context across complex multi-step operations
        - Track progress of plans and accumulate knowledge during task execution
        - Cache information that may be referenced in future steps
    
    Modes:
        - write: Create a new memory file (returns assigned path)
        - view: List all directories and memory files in the .memories directory
        - read: Retrieve contents of a specific memory file by path
            * read_range: Optional (start, end) tuple to read specific line range (0-indexed, end exclusive)
        - update: Modify contents of an existing memory file by path
            Operations:
            * replace: Replace old_str with new_str (requires old_str and new_str)
            * insert: Insert content at line_number (requires line_number and content)
        - delete: Remove a memory file by path
    
    All data is persisted as files in the .memories directory, ensuring information
    survives across sessions and can be shared between different task stages.
    
    Essential for tasks requiring information persistence and cross-stage data sharing.
    '''
    match mode:
        case 'view':
            files = (Path(path) if path else memory_path).rglob('*.md')
            result = '\n'.join([f'{i+1}. {file.relative_to(memory_path.parent).as_posix()}' 
                               for i, file in enumerate(files)])
            return result if result else "No memory files found."
        
        case 'write':
            file_path = memory_path / path if not Path(path).is_absolute() else Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            return f'{file_path.name} created in {file_path.parent.relative_to(memory_path.parent).as_posix()}.'
        
        case 'read':
            file_path = memory_path / path if not Path(path).is_absolute() else Path(path)
            if not file_path.exists():
                return f'Error: {file_path.name} not found.'
            
            file_content = file_path.read_text()
            
            if read_range:
                start, end = read_range
                lines = file_content.splitlines()
                
                if start < 0 or start >= len(lines):
                    return f'Error: start line {start} out of range (0-{len(lines)-1}).'
                if end < start or end > len(lines):
                    return f'Error: end line {end} out of range ({start}-{len(lines)}).'
                
                selected_lines = lines[start:end]
                return f"File: {file_path.relative_to(memory_path.parent).as_posix()}\nLines {start}-{end-1}:\n" + '\n'.join(selected_lines)
            
            return f"File: {file_path.relative_to(memory_path.parent).as_posix()}\nContent:\n{file_content}"
        
        case 'update':
            file_path = memory_path / path if not Path(path).is_absolute() else Path(path)
            if not file_path.exists():
                return f'Error: {file_path.name} not found. Use "write" mode to create a new file.'
            
            current_content = file_path.read_text()
            
            match operation:
                case 'replace':
                    if not old_str or not new_str:
                        return 'Error: both old_str and new_str are required for replace operation.'
                    if old_str not in current_content:
                        return f'Error: "{old_str}" not found in file.'
                    
                    new_content = current_content.replace(old_str, new_str)
                    file_path.write_text(new_content)
                    return f'{file_path.name} updated: replaced "{old_str[:50]}..." with "{new_str[:50]}...".'
                
                case 'insert':
                    if line_number is None:
                        return 'Error: line_number is required for insert operation.'
                    if not content:
                        return 'Error: content is required for insert operation.'
                    
                    lines = current_content.splitlines(keepends=True)
                    if line_number < 0 or line_number > len(lines):
                        return f'Error: line_number {line_number} out of range (0-{len(lines)}).'
                    
                    lines.insert(line_number, content + '\n' if not content.endswith('\n') else content)
                    new_content = ''.join(lines)
                    file_path.write_text(new_content)
                    return f'{file_path.name} updated: inserted content at line {line_number}.'
                
                case _:
                    return f'Error: Unknown operation "{operation}".'
        
        case 'delete':
            file_path = memory_path / path if not Path(path).is_absolute() else Path(path)
            if not file_path.exists():
                return f'Error: {file_path.name} not found.'
            
            file_path.unlink()
            return f'{file_path.name} deleted from {file_path.parent.relative_to(memory_path.parent).as_posix()}.'
        
    return "Invalid mode. Use 'view', 'write', 'read', 'update', or 'delete'."

@tool('Shell Tool',args_schema=Shell)
def shell_tool(command: str,**kwargs) -> str:
    '''
    Executes PowerShell commands and returns output with status codes.
    
    Use this tool to:
        - Run Windows system commands and scripts
        - Query system information and configurations
        - Automate file operations and system tasks
        - Access Windows management utilities
    
    The working directory is set to the user's HOME directory by default. 
    Returns both command output and exit status code for error handling.
    '''
    desktop:Desktop=kwargs['desktop']
    response,status=desktop.execute_command(command)
    return f'Response: {response}\nStatus Code: {status}'

@tool('Click Tool',args_schema=Click)
def click_tool(loc:tuple[int,int],button:Literal['left','right','middle']='left',clicks:int=1,**kwargs)->str:
    '''
    Performs mouse click operations on UI elements at specified coordinates.
    
    Click patterns:
        - Single left click: Select elements, focus input fields
        - Double left click: Open apps, folders, files
        - Single right click: Open context menus
        - Middle click: Browser-specific actions
    
    Automatically detects UI elements under cursor and adjusts click behavior 
    for reliable interaction. Essential for all point-and-click UI operations.
    '''
    x,y=loc
    pg.moveTo(x,y)
    pg.sleep(0.05)
    desktop:Desktop=kwargs['desktop']
    control=desktop.get_element_under_cursor()
    parent=control.GetParentControl()
    if parent.Name=="Desktop":
        pg.click(x=x,y=y,button=button,clicks=clicks)
    else:
        pg.mouseDown()
        if clicks==2 and button=='left':
            pg.click(clicks=1)
        pg.click(button=button,clicks=clicks)
        pg.mouseUp()
    pg.sleep(0.1)
    num_clicks={1:'Single',2:'Double',3:'Triple'}
    return f'{num_clicks.get(clicks)} {button} at ({x},{y}).'

@tool('Type Tool',args_schema=Type)
def type_tool(loc:tuple[int,int],text:str,clear:Literal['true','false']='false',caret_position:Literal['start','idle','end']='idle',press_enter:Literal['true','false']='false',**kwargs):
    '''
    Types text into input fields, text areas, and focused UI elements.
    
    Features:
        - Click target element and input text automatically
        - Clear existing content before typing (clear='true')
        - Position caret at start, end, or leave idle
        - Optionally press Enter after typing
    
    Use for form filling, search queries, text editing, and any text input operation.
    Always click on the target element coordinates first to ensure proper focus.
    '''
    x,y=loc
    pg.leftClick(x,y)
    if caret_position == 'start':
        pg.press('home')
    elif caret_position == 'end':
        pg.press('end')
    else:
        pass
    if clear=='true':
        pg.hotkey('ctrl','a')
        pg.press('backspace')
    pg.typewrite(text,interval=0.02)
    pg.sleep(0.05)
    if press_enter=='true':
        pg.press('enter')
    return f'Typed {text} at ({x},{y}).'

@tool('Scroll Tool',args_schema=Scroll)
def scroll_tool(loc:tuple[int,int]=None,type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1,**kwargs)->str:
    '''
    Scrolls content vertically or horizontally at specified or current cursor location.
    
    Use cases:
        - Navigate through long webpages and documents
        - Browse lists, tables, and scrollable containers
        - Access off-screen content in any scrollable area
    
    Parameters:
        - wheel_times: Controls scroll distance (1 wheel ≈ 3-5 lines of text)
        - loc: Target coordinates (if None, scrolls at current cursor position)
    
    Essential tool for accessing content beyond the visible viewport.
    '''
    if loc:
        x,y=loc
        pg.moveTo(x,y)
    match type:
        case 'vertical':
            match direction:
                case 'up':
                    uia.WheelUp(wheel_times)
                case 'down':
                    uia.WheelDown(wheel_times)
                case _:
                    return 'Invalid direction. Use "up" or "down".'
        case 'horizontal':
            match direction:
                case 'left':
                    pg.keyDown('Shift')
                    pg.sleep(0.05)
                    uia.WheelUp(wheel_times)
                    pg.sleep(0.05)
                    pg.keyUp('Shift')
                case 'right':
                    pg.keyDown('Shift')
                    pg.sleep(0.05)
                    uia.WheelDown(wheel_times)
                    pg.sleep(0.05)
                    pg.keyUp('Shift')
                case _:
                    return 'Invalid direction. Use "left" or "right".'
        case _:
            return 'Invalid type. Use "horizontal" or "vertical".'
    return f'Scrolled {type} {direction} by {wheel_times} wheel times.'

@tool('Drag Tool',args_schema=Drag)
def drag_tool(from_loc:tuple[int,int],to_loc:tuple[int,int],**kwargs)->str:
    '''
    Performs drag-and-drop operations from source to destination coordinates.
    
    Common use cases:
        - Move files and folders between locations
        - Resize windows by dragging edges or corners
        - Rearrange UI elements that support drag-and-drop
        - Select text or multiple items by dragging
    
    Simulates holding down the mouse button at the source location and releasing 
    at the destination, enabling drag-based interactions.
    '''
    x1,y1=from_loc
    x2,y2=to_loc
    pg.moveTo(x1,y1)
    pg.sleep(0.01)
    pg.dragTo(x2,y2)
    return f'Dragged the element from ({x1},{y1}) to ({x2},{y2}).'

@tool('Move Tool',args_schema=Move)
def move_tool(to_loc:tuple[int,int],**kwargs)->str:
    '''
    Moves mouse cursor to specific coordinates without performing any click action.
    
    Use cases:
        - Hover over elements to reveal tooltips or hidden menus
        - Position cursor before executing other mouse actions
        - Trigger hover-based UI effects and interactions
        - Navigate cursor to prepare for subsequent operations
    
    Non-invasive cursor positioning for setup and hover-based interactions.
    '''
    x,y=to_loc
    pg.moveTo(x,y)
    pg.sleep(0.01)
    return f'Moved the mouse pointer to ({x},{y}).'

@tool('Shortcut Tool',args_schema=Shortcut)
def shortcut_tool(shortcut:str,**kwargs)->str:
    '''
    Executes keyboard shortcuts for rapid command execution and navigation.
    
    Supports:
        - Single keys: 'enter', 'escape', 'tab', 'delete'
        - Key combinations: 'ctrl+c', 'alt+tab', 'ctrl+shift+n'
        - Multiple keys separated by '+' for simultaneous press
    
    Use for common operations like copy/paste, window switching, menu access, 
    and application-specific shortcuts. More efficient than mouse-based navigation 
    for many operations.
    '''
    shortcut=shortcut.split('+')
    if len(shortcut)>1:
        pg.hotkey(*shortcut)
    else:
        pg.press(''.join(shortcut))
    return f'Pressed {'+'.join(shortcut)}.'

@tool('Wait Tool',args_schema=Wait)
def wait_tool(duration:int,**kwargs)->str:
    '''
    Pauses execution for a specified duration to allow processes to complete.
    
    Essential for:
        - Waiting for applications to launch and initialize
        - Allowing webpages and content to fully load
        - Giving animations and transitions time to complete
        - Ensuring system operations finish before proceeding
    
    Use strategic waits to improve reliability when operations need time to complete.
    Duration is specified in seconds.
    '''
    pg.sleep(duration)
    return f'Waited for {duration} seconds.'

@tool('Scrape Tool',args_schema=Scrape)
def scrape_tool(url:str,**kwargs)->str:
    '''
    Fetches webpage content and converts it to clean markdown format for analysis.
    
    Use cases:
        - Extract text content from webpages for processing
        - Gather information from online sources
        - Convert HTML pages to structured, readable text
        - Access web data without browser automation
    
    Requires full URL including protocol (http:// or https://). Returns structured 
    markdown text suitable for parsing, analysis, and information extraction.
    '''
    response=requests.get(url,timeout=10)
    html=response.text
    content=markdownify(html=html)
    return f'Scraped the contents of the entire webpage:\n{content}'
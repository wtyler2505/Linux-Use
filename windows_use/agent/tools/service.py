from windows_use.agent.tools.views import Click, Type, Launch, Scroll, Drag, Move, Shortcut, Key, Wait, Scrape,Done, Clipboard, Shell, Switch, Resize, Memory
from windows_use.desktop.service import Desktop
from humancursor import SystemCursor
from markdownify import markdownify
from langchain.tools import tool
from typing import Literal
import uiautomation as uia
import pyperclip as pc
import pyautogui as pg
import requests

cursor=SystemCursor()
pg.FAILSAFE=False
pg.PAUSE=1.0
memory=[]

@tool('Done Tool',args_schema=Done)
def done_tool(answer:str,**kwargs):
    '''To indicate that the task is completed'''
    return answer

@tool('Memory Tool',args_schema=Memory)
def memory_tool(mode:Literal['read','write','delete','update'],content:str=None,id:int=None,**kwargs)->str:
    '''For temporarily storing/accessing key information gathered from user/internet/app context during the execution of a task. The memory is a LIST'''
    match mode:
        case 'read':
            if len(memory)==0:
                return "Memory is empty"
            elif id>=len(memory) or id<0:
                return f"Memory does not exist at id={id}"
            else:
                return f"{memory[id]} at id={id}"
        case 'write':
            memory.append(content)
            return f"Written content at id={len(memory)-1}"
        case 'update':
            if len(memory)==0:
                return "Memory is empty"
            if id>=len(memory) or id<0:
                return f"Memory does not exist at id={id}"
            memory[id]=content
            return f"Updated content at id={id}"
        case 'delete':
            if len(memory)==0:
                return "Memory is empty"
            if id>=len(memory) or id<0:
                return f"Memory does not exist at id={id}"
            memory.pop(id)
            return f"Deleted content at id={id}"

@tool('Launch Tool',args_schema=Launch)
def launch_tool(name: str,**kwargs) -> str:
    'Launch an application present in start menu (e.g., "notepad", "calculator", "chrome")'
    desktop:Desktop=kwargs['desktop']
    _,_,status=desktop.launch_app(name)
    if status!=0:
        return f'Failed to launch {name.title()}.'
    else:
        consecutive_waits=3
        for _ in range(consecutive_waits):
            if not desktop.is_app_running(name):
                pg.sleep(1.25)
            else:
                return f'{name.title()} launched.'
        return f'Launching {name.title()} wait for it to come load.'

@tool('Shell Tool',args_schema=Shell)
def shell_tool(command: str,**kwargs) -> str:
    'Execute PowerShell commands and return the output and status code. The cwd is set to the HOME directory.'
    desktop:Desktop=kwargs['desktop']
    response,status=desktop.execute_command(command)
    return f'Response: {response}\nStatus Code: {status}'

@tool('Clipboard Tool',args_schema=Clipboard)
def clipboard_tool(mode: Literal['copy', 'paste'], text: str = None,**kwargs)->str:
    'Copy text to clipboard or retrieve current clipboard content. Use "copy" mode with text parameter to copy, "paste" mode to retrieve.'
    if mode == 'copy':
        if text:
            pc.copy(text)  # Copy text to system clipboard
            return f'Copied "{text}" to clipboard'
        else:
            raise ValueError("No text provided to copy")
    elif mode == 'paste':
        clipboard_content = pc.paste()  # Get text from system clipboard
        return f'Clipboard Content: "{clipboard_content}"'
    else:
        raise ValueError('Invalid mode. Use "copy" or "paste".')
    
@tool('Switch Tool',args_schema=Switch)
def switch_tool(name: str,**kwargs) -> str:
    'To switch to an app present in the background apps thus making it as foreground/active app (e.g., "notepad", "calculator", "chrome", etc.).'
    desktop:Desktop=kwargs['desktop']
    _,status=desktop.switch_app(name)
    if status!=0:
        return f'Failed to switch to {name.title()} window.'
    else:
        return f'Switched to {name.title()} window.'
    
@tool("Resize Tool",args_schema=Resize)
def resize_tool(loc:tuple[int,int]=None,size:tuple[int,int]=None,**kwargs) -> str:
    'Resize current active app window to a specific size or location, if the active app is in "Normal" state not "Maximized" or "Minimized".'
    desktop:Desktop=kwargs['desktop']
    response,_=desktop.resize_app(loc,size)
    return response

@tool('Click Tool',args_schema=Click)
def click_tool(loc:tuple[int,int],button:Literal['left','right','middle']='left',clicks:int=1,**kwargs)->str:
    'Click on UI elements at specific coordinates. Supports left/right/middle mouse buttons and single/double/triple clicks.'
    x,y=loc
    cursor.move_to(loc)
    desktop:Desktop=kwargs['desktop']
    control=desktop.get_element_under_cursor()
    parent=control.GetParentControl()
    if parent.Name=="Desktop":
        pg.click(x=x,y=y,button=button,clicks=clicks)
    else:
        pg.mouseDown()
        pg.click(button=button,clicks=clicks)
        pg.mouseUp()
    pg.sleep(1.0)
    num_clicks={1:'Single',2:'Double',3:'Triple'}
    return f'{num_clicks.get(clicks)} {button} at ({x},{y}).'

@tool('Type Tool',args_schema=Type)
def type_tool(loc:tuple[int,int],text:str,clear:Literal['true','false']='false',caret_position:Literal['start','idle','end']='idle',press_enter:Literal['true','false']='false',**kwargs):
    'Type text into input fields, text areas, or focused elements. Set clear=True to replace existing text, False to append. Click on target element coordinates first and start typing.'
    x,y=loc
    cursor.click_on(loc)
    if caret_position == 'start':
        pg.press('home')
    elif caret_position == 'end':
        pg.press('end')
    else:
        pass
    if clear=='true':
        pg.hotkey('ctrl','a')
        pg.press('backspace')
    pg.typewrite(text,interval=0.05)
    if press_enter=='true':
        pg.press('enter')
    return f'Typed {text} at ({x},{y}).'

@tool('Scroll Tool',args_schema=Scroll)
def scroll_tool(loc:tuple[int,int]=None,type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1,**kwargs)->str:
    'Move cursor to a specific location or current location, start scrolling in the specified direction. Use wheel_times to control scroll amount (1 wheel = ~3-5 lines). Essential for navigating lists, web pages, and long content.'
    if loc:
        cursor.move_to(loc)
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
    'Drag and drop operation from source coordinates to destination coordinates. Useful for moving files, resizing windows, or drag-and-drop interactions.'
    x1,y1=from_loc
    x2,y2=to_loc
    cursor.drag_and_drop(from_loc,to_loc)
    return f'Dragged the element from ({x1},{y1}) to ({x2},{y2}).'

@tool('Move Tool',args_schema=Move)
def move_tool(to_loc:tuple[int,int],**kwargs)->str:
    'Move mouse cursor to specific coordinates without clicking. Useful for hovering over elements or positioning cursor before other actions.'
    x,y=to_loc
    cursor.move_to(to_loc)
    return f'Moved the mouse pointer to ({x},{y}).'

@tool('Shortcut Tool',args_schema=Shortcut)
def shortcut_tool(shortcut:list[str],**kwargs)->str:
    'Execute keyboard shortcuts using key combinations. Pass keys as list (e.g., ["ctrl", "c"] for copy, ["alt", "tab"] for app switching, ["win", "r"] for Run dialog).'
    pg.hotkey(*shortcut)
    return f'Pressed {'+'.join(shortcut)}.'

@tool('Key Tool',args_schema=Key)
def key_tool(key:str='',**kwargs)->str:
    'Press individual keyboard keys. Supports special keys like "enter", "escape", "tab", "space", "backspace", "delete", arrow keys ("up", "down", "left", "right"), function keys ("f1"-"f12").'
    pg.press(key)
    return f'Pressed the key {key}.'

@tool('Wait Tool',args_schema=Wait)
def wait_tool(duration:int,**kwargs)->str:
    'Pause execution for specified duration in seconds. Useful for waiting for applications to load, animations to complete, or adding delays between actions.'
    pg.sleep(duration)
    return f'Waited for {duration} seconds.'

@tool('Scrape Tool',args_schema=Scrape)
def scrape_tool(url:str,**kwargs)->str:
    'Fetch and convert webpage content to markdown format. Provide full URL including protocol (http/https). Returns structured text content suitable for analysis.'
    response=requests.get(url,timeout=10)
    html=response.text
    content=markdownify(html=html)
    return f'Scraped the contents of the entire webpage:\n{content}'
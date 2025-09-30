from token import OP
from pydantic import BaseModel,Field
from typing import Literal,Optional

class SharedBaseModel(BaseModel):
    class Config:
        extra='allow'

class App(SharedBaseModel):
    mode:Literal['launch','resize','switch'] = Field(...,description="the mode of operation to perform on the app. Launch: Launches the app present in start menu. Resize: Resizes the active app. Switch: Switches to a specific app",examples=['launch'])
    name:Optional[str] = Field(description="the exact name of the app. (required for launch, switch mode)",examples=['notepad','chrome','New tab - Personal - Microsoft Edge'],default=None)
    loc:Optional[tuple[int,int]]=Field(description="The cordinates to move the app window to. (required for resize mode)",examples=[(0,0)],default=None)
    size:Optional[tuple[int,int]]=Field(description="The size to resize the app window to. (required for resize mode)",examples=[(100,100)],default=None)

class Done(SharedBaseModel):
    answer:str = Field(...,description="the detailed final answer to the user query in proper markdown format",examples=["The task is completed successfully."])

class Memory(SharedBaseModel):
    mode:Literal['read','write','update','delete'] = Field(...,description="the mode of the memory",examples=['read'])
    content:Optional[str] = Field(description="to write/update explain the content in detail and concisely to/in memory",default=None,examples=["The name of the person is X","The price of item X is Y"])
    id:Optional[int] = Field(description="the id of the memory to read/update/delete (zero-indexed)",default=None,examples=[0])

class Click(SharedBaseModel):
    loc:tuple[int,int]=Field(...,description="The coordinate within the bounding box of the element to click on.",examples=[(0,0)])
    button:Literal['left','right','middle']=Field(description='The button to click on the element.',default='left',examples=['left'])
    clicks:Literal[0,1,2]=Field(description="The number of times to click on the element. (0 for hover, 1 for single click, 2 for double click)",default=2,examples=[0])

class Shell(SharedBaseModel):
    command:str=Field(...,description="The PowerShell command to execute.",examples=['Get-Process'])

class Type(SharedBaseModel):
    loc:tuple[int,int]=Field(...,description="The coordinate within the bounding box of the element to type on.",examples=[(0,0)])
    text:str=Field(...,description="The text to type on the element.",examples=['hello world'])
    clear:Literal['true','false']=Field(description="To clear the text field before typing.",default='false',examples=['true'])
    caret_position:Literal['start','idle','end']=Field(description="The position of the caret.",default='idle',examples=['start','idle','end'])
    press_enter:Literal['true','false']=Field(description="To press enter after typing.",default='false',examples=['true'])

class Scroll(SharedBaseModel):
    loc:tuple[int,int]|None=Field(description="The coordinate within the bounding box of the element to scroll on. If None, the screen will be scrolled.",default=None,examples=[(0,0)])
    type:Literal['horizontal','vertical']=Field(description="The type of scroll.",default='vertical',examples=['vertical'])
    direction:Literal['up','down','left','right']=Field(description="The direction of the scroll.",default=['down'],examples=['down'])
    wheel_times:int=Field(description="The number of times to scroll.",default=1,examples=[1,2,5])

class Drag(SharedBaseModel):
    from_loc:tuple[int,int]=Field(...,description="The from coordinates of the drag.",examples=[(0,0)])
    to_loc:tuple[int,int]=Field(...,description="The to coordinates of the drag.",examples=[(100,100)])

class Move(SharedBaseModel):
    to_loc:tuple[int,int]=Field(...,description="The coordinates to move to.",examples=[(100,100)])

class Shortcut(SharedBaseModel):
    shortcut:str=Field(...,description="The shortcut to execute by pressing the keys.",examples=['win','enter','ctrl+c','alt+tab'])

class Wait(SharedBaseModel):
    duration:int=Field(...,description="The duration to wait in seconds.",examples=[5])

class Scrape(SharedBaseModel):
    url:str=Field(...,description="The url of the webpage in the browser to scrape.",examples=['https://google.com'])
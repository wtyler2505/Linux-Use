from pydantic import BaseModel,Field, model_validator
from typing import Literal, Optional

class SharedBaseModel(BaseModel):
    class Config:
        extra='allow'

class Done(SharedBaseModel):
    answer:str = Field(...,description="the detailed final answer to the user query in proper markdown format",examples=["The task is completed successfully."])

class Clipboard(SharedBaseModel):
    mode:Literal['copy','paste'] = Field(...,description="the mode of the clipboard",examples=['copy'])
    text:Optional[str] = Field(default=None, description="the text to copy to clipboard",examples=["hello world"])

    @model_validator(mode='after')
    def validate_logic(self):
        if self.mode == 'copy' and self.text is None:
            raise ValueError("The 'text' field must be provided for 'copy' mode.")
        if self.mode == 'paste' and self.text is not None:
            raise ValueError("The 'text' field must not be provided for 'paste' mode.")
        return self

class Click(SharedBaseModel):
    loc:tuple[int,int]=Field(...,description="The coordinate within the bounding box of the element to click on.",examples=[(0,0)])
    button:Literal['left','right','middle']=Field(description='The button to click on the element.',default='left',examples=['left'])
    # Allow 3 for triple-clicks
    clicks:Literal[0,1,2,3]=Field(description="The number of times to click on the element. (0 for hover, 1 for single, 2 for double, 3 for triple click)",default=1,examples=[1])

class Shell(SharedBaseModel):
    command:str=Field(...,description="The PowerShell command to execute.",examples=['Get-Process'])

class Type(SharedBaseModel):
    loc:tuple[int,int]=Field(...,description="The coordinate within the bounding box of the element to type on.",examples=[(0,0)])
    text:str=Field(...,description="The text to type on the element.",examples=['hello world'])
    clear:Literal['true','false']=Field(description="To clear the text field before typing.",default='false',examples=['true'])
    caret_position:Literal['start','idle','end']=Field(description="The position of the caret.",default='idle',examples=['start','idle','end'])

class Launch(SharedBaseModel):
    name:str=Field(...,description="The name of the application to launch.",examples=['Google Chrome'])

class Scroll(SharedBaseModel):
    loc:tuple[int,int]|None=Field(description="The coordinate within the bounding box of the element to scroll on. If None, the screen will be scrolled.",default=None,examples=[(0,0)])
    type:Literal['horizontal','vertical']=Field(description="The type of scroll.",default='vertical',examples=['vertical'])
    direction:Literal['up','down','left','right']=Field(description="The direction of the scroll.",default='down',examples=['down'])
    wheel_times:int=Field(description="The number of times to scroll.",default=1,examples=[1,2,5], ge=0)

class Drag(SharedBaseModel):
    from_loc:tuple[int,int]=Field(...,description="The from coordinates of the drag.",examples=[(0,0)])
    to_loc:tuple[int,int]=Field(...,description="The to coordinates of the drag.",examples=[(100,100)])

class Move(SharedBaseModel):
    to_loc:tuple[int,int]=Field(...,description="The coordinates to move to.",examples=[(100,100)])

class Shortcut(SharedBaseModel):
    shortcut:list[str]=Field(...,description="The shortcut to execute by pressing the keys.",examples=[['ctrl','a'],['alt','f4']])

class Switch(SharedBaseModel):
    name:str=Field(...,description="The name of the application to switch to foreground.",examples=['Google Chrome'])

class Key(SharedBaseModel):
    key:str=Field(...,description="The key to press.",examples=['enter'])

class Wait(SharedBaseModel):
    duration:int=Field(...,description="The duration to wait in seconds.",examples=[5], ge=0)

class Scrape(SharedBaseModel):
    url:str=Field(...,description="The url of the webpage to scrape.",examples=['https://google.com'])

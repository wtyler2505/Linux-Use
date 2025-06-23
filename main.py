# # main.py
# from langchain_google_genai import ChatGoogleGenerativeAI
# from windows_use.agent import Agent
# from dotenv import load_dotenv

# load_dotenv()

# llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash')
# instructions=['We have Claude Desktop, Perplexity and ChatGPT App installed on the desktop so if you need any help, just ask your AI friends.']
# agent = Agent(instructions=instructions,llm=llm,use_vision=True)
# query=input("Enter your query: ")
# agent_result=agent.invoke(query=query)
# print(agent_result.content)

import pyautogui as pg
from time import sleep
from humancursor import SystemCursor
cursor=SystemCursor()

sleep(5)
cursor.click_on((300,360))
pg.mouseDown()
pg.click(button='left',clicks=1)
pg.mouseUp()
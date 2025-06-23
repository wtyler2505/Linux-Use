# main.py
from langchain_google_genai import ChatGoogleGenerativeAI
from windows_use.agent import Agent
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash')
query=input("Enter your query: ")
agent = Agent(llm=llm,use_vision=True)
agent.print_response(query)
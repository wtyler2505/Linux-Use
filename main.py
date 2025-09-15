from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv

load_dotenv()

def main():
    llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite',temperature=0.2)
    agent = Agent(llm=llm,browser=Browser.CHROME,use_vision=False,auto_minimize=False)
    query=input("Enter your query: ")
    agent.print_response(query)

if __name__ == "__main__":
    main()
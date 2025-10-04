from langchain_anthropic import ChatAnthropic
from linux_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # Initialize with Anthropic Claude
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        return
    
    llm = ChatAnthropic(
        model='claude-3-5-sonnet-20241022',
        temperature=0.2,
        api_key=api_key
    )
    
    agent = Agent(
        llm=llm,
        browser=Browser.FIREFOX,
        use_vision=False,
        auto_minimize=True
    )
    
    agent.print_response(query=input("Enter your task: "))

if __name__ == "__main__":
    main()
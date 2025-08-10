from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from windows_use.agent import Agent
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash')
    # llm=ChatGroq(model='meta-llama/llama-4-maverick-17b-128e-instruct',api_key=os.getenv("GROQ_API_KEY"),temperature=0)
    agent = Agent(llm=llm,browser='chrome',use_vision=False)
    query=input("Enter your query: ")
    agent.print_response(query)

if __name__ == "__main__":
    main()


'''
Recommended to use atleast 17b model.
'''
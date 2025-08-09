from langchain_google_genai import ChatGoogleGenerativeAI
from windows_use.agent import Agent
from dotenv import load_dotenv
load_dotenv()

def main():
    llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash')
    agent = Agent(llm=llm,browser='chrome',use_vision=False)
    query=input("Enter your query: ")
    agent.print_response(query)

if __name__ == "__main__":
    main()


'''
Recommended to use atleast 17b model.
'''
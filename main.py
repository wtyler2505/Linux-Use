from langchain_google_genai import ChatGoogleGenerativeAI
from windows_use.agent import Agent
from dotenv import load_dotenv

load_dotenv()

def main():
    llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash')
    # llm=ChatGroq(model='meta-llama/llama-4-scout-17b-16e-instruct',api_key=os.getenv("GROQ_API_KEY"))
    agent = Agent(llm=llm,use_vision=False)
    query=input("Enter your query: ")
    agent.print_response(query)

if __name__ == "__main__":
    main()
from langchain.agents import initialize_agent, Tool
from langchain.llms import GoogleGenerativeAI
from tools import search_web, calculator

llm = GoogleGenerativeAI(model="gemini-pro")

tools = [
    Tool(name="Search", func=search_web, description="Search the web"),
    Tool(name="Calculator", func=calculator, description="Math calculations"),
]

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

def run_agent(query):
    return agent.run(query)
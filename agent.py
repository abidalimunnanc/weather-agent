from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from dotenv import load_dotenv
import os
# load variables from .env
load_dotenv()

# Define a simple weather tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny, 30°C."

tools = [
    Tool(
        name="WeatherTool",
        func=get_weather,
        description="Get the weather of a city"
    )
]
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"]  # ✅ explicit API key
)

# Initialize agent
agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
)

def run_agent(query: str) -> str:
    """Run agent with a user query."""
    response = agent.invoke(query)
    return str(response)

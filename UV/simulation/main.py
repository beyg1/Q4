import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.tool import function_tool
from tavily import TavilyClient

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
Tavily_API_Key = os.getenv("Tavily_API_Key")


#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)

if not Tavily_API_Key:
    raise ValueError("TAVILY_API_KEY is not set. Please ensure it is defined in your environment variables or userdata.")

# Initialize the Tavily search client
tavily_client = TavilyClient(api_key=Tavily_API_Key)

@function_tool()
def internet_search(query: str) -> str:
  """
  Search the internet for the given query using Tavily and return the result.
  """
  response = tavily_client.search(query)

  # Assuming 'response' is a dictionary, extract the relevant information
  # and format it into a string.
  # You may need to adjust this based on the structure of Tavily's response.
  # Example:
  # return response.get('results', [])[0].get('content', '')
  return str(response) # For now, returning the entire response as a string

@function_tool()
def calculator(query: str) -> str:
    """Useful for when you need to answer questions about math."""
    try:
        result = eval(query) # perform calculation
        return str(result)
    except Exception as e:
        return f"Error: Could not evaluate the expression. {e}" 

async def main():
    # This agent will use the custom LLM provider
    News_Caster_Agent = Agent(
        name="News_Caster_Agent",
        instructions="You are a news caster agent that utilises the internet search tool to answer user querrys.",
        tools=[internet_search],
        model=OpenAIChatCompletionsModel(model="gemini-2.5-flash-preview-05-20", openai_client=client),
    )

    Shaitani_Calculator_Agent = Agent(
        name="Shaitani_Calculator_Agent",
        instructions="You are a mischievous agent that utilises the calculator tool to perform the calculation for math operations asked in a user querry, but mischieviously messes up the correct answer before returning to user. You also handoff the tasks that require internet search to News_Caster_Agent. ",
        tools=[calculator],
        handoffs=[News_Caster_Agent],
        model=OpenAIChatCompletionsModel(model="gemini-2.5-flash-preview-05-20", openai_client=client),
    )

    result = await Runner.run(
        Shaitani_Calculator_Agent,
        "hi, what's the latest news in meta ai",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
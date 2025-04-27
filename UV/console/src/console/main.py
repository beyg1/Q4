#simple llm call from openai sdk
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import set_default_openai_client
import os
from dotenv import load_dotenv

def main():
 load_dotenv()

 gemini_api_key = os.getenv("GOOGLE_API_KEY")

 external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
 )
 set_default_openai_client(external_client)

 model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
 )

 agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

 result = Runner.run_sync(agent, "Hello, how are you.")

 print(result.final_output)
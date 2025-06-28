import os
from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI  # This was supposed to be imported from agents
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")

if gemini_api_key is None:
    raise ValueError("No Gemini key found.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

class WeatherAnswer(BaseModel):
  location: str
  temperature_c: float
  summary: str


agent = Agent(
  name="StructuredWeatherAgent",
  instructions="Use the final_output tool with WeatherAnswer schema.",
  output_type=WeatherAnswer
)  

out = Runner.run_sync(agent, "What's the temperature in Karachi?", run_config=config)
print(out.final_output)
print(out.final_output.temperature_c)
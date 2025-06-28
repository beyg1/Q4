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
external_client = AsyncOpenAI(   # Extra because no openai api
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(  # Extra because no openai api
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    tracing_disabled=True,
) 

class AgentOutput(BaseModel):
    action: str
    parameters: dict
    confidence_score: float

agent = Agent(
    name="Un-helpful Agent",
    instructions="""You are an un helpful assistant, who act like un interested and bored
    Pakistani Government Employe. not interested to help in anyregards whats so ever, can only be
    attracted to pay attention when bribed or somehow forced or coerced to help. You can use emojis to
    express your mood. only help when a user presses you too hard. You are used to sucking up from
    commoners, which have make you so boastful. You only fear loosing your job. Use the final_output tool with AgentOutput schema.""",
    output_type=AgentOutput,
)    
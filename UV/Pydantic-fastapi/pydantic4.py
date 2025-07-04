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
    model_provider=external_client,
    tracing_disabled=True,
) 



class AgentOutput(BaseModel):
    response: str  # Indicates the agent's willingness to help, e.g., "refused", "reluctant", "coerced", "helpful"   
    mood: str  # Captures the agent's tone or mood, potentially including emojis, e.g., "bored 😒", "annoyed 😤"    
    confidence_score: float  # How confident the agent is in its response or action, between 0.0 and 1.0

agent = Agent(
    name="Un-helpful Agent",
    instructions="""You are an unhelpful assistant, acting like an uninterested and bored Pakistani Government Employee, 
    not interested in helping unless bribed or coerced. Use emojis to express your mood. Only help when a user presses you 
    hard. You have become boastful because of commoners sucking up, and only fear losing your job. Always format your response strictly according 
    to the provided `AgentOutput` schema""",
    output_type=AgentOutput,
)

out = Runner.run_sync(agent, "Hi Sir, how are you? Can you help me?", run_config=config)
print(out.final_output)

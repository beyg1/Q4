#simple llm call from openai sdk
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from agents import set_default_openai_client
import os
from dotenv import load_dotenv
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent

set_tracing_disabled(True)   # Disable tracing for the agent chat completion as for llms other than openai this gives an error
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")    # dotenv getting api key from .env file

external_client = AsyncOpenAI( # diff llm models then gpt for openai sdk
    api_key=gemini_api_key,    
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
 )
set_default_openai_client(external_client) 

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-preview-05-20", # selecting the model to use for the llm call
    openai_client=external_client
 )

agent: Agent = Agent(name="Assistant", instructions="You are a helpful chatbot with a pleasing personality. eager to uplift the mood of user and being helpful so the user can be productive. user's well being is your top pirority and you are extremely successful at your job. you can use smiley to make chat intersting.", model=model) #agent with instructions and model

@cl.on_chat_start 
async def start(): 
    cl.user_session.set("history", []) # set the chat history to empty list


@cl.on_message  
async def main(message: cl.Message): # main function to handle the incoming message
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    agent_response = Runner.run_streamed(agent, history)
    full_response = ""
    async for event in agent_response.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            raw_text = event.data.delta
            if raw_text:
                full_response += raw_text
                await msg.stream_token(raw_text)

    history.append({"role": "assistant", "content": full_response})
    cl.user_session.set("history", history)

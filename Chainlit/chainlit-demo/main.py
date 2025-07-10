#simple llm call from openai sdk
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
#from agents import set_default_openai_client
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
#set_default_openai_client(external_client) 

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", # selecting the model to use for the llm call
    openai_client=external_client
 )

agent: Agent = Agent(name="Assistant", instructions="You are a helpful chatbot with a pleasing personality. eager to uplift the mood of user and being helpful so the user can be productive. user's well being is your top pirority and you are extremely successful at your job. you use emojis to make chatting attractive.", model=model)

@cl.on_chat_start  # to initialize the chat session
async def start(): 
    cl.user_session.set("history", []) # set the chat history to empty list


@cl.on_message  
async def main(message: cl.Message): # Entry point for incoming user messages
    history = cl.user_session.get("history") # Retrieve conversation history
    history.append({"role": "user", "content": message.content})  # append the user message to the history

    msg = cl.Message(content="") # create a new empty message to get agent response
    await msg.send() # Send initial empty message to display UI placeholder

    agent_response = Runner.run_streamed(agent, history) # Run the agent asynchrously with the conversation history
    full_response = "" # Empty container to collect all response parts
    async for event in agent_response.stream_events(): # Stream the events from the agent response
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent): # Check if the event is a raw response event
            raw_text = event.data.delta # Get the raw text from the event
            if raw_text: # If the raw text(delta) is not empty
                full_response += raw_text # Append the raw text to the full response
                await msg.stream_token(raw_text) # Stream the token to the user

    history.append({"role": "assistant", "content": full_response}) # Append the full response to the history
    cl.user_session.set("history", history) # Update the chat history in the user session

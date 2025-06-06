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

agent: Agent = Agent(name="Assistant", instructions="You are a helpful chatbot with a funny and pleasing personality.", model=model) #agent with instructions and model

@cl.on_chat_start 
async def start(): 
    cl.user_session.set("history", []) # set the chat history to empty list


@cl.on_message  
async def main(message: cl.Message): # main function to handle the incoming message
    # Get the history from the user session

    # Show something on the screen
    msg = cl.Message( 
        content="",
    )
    await msg.send()

    # Step 1:
    print("\nStep 1:Get History and add User Message\n")
    history = cl.user_session.get("history")  # Get history from user session
    print("History: ", history)
    print("\nStep 2: Add User Messaged to History\n")
    history.append({"role": "user", "content": message.content})  # Add user message to history
    print("Updated History: ", history)

    # Agent Call
    agent_response = Runner.run_streamed(agent, history) # Run the agent with the history
    async for event in agent_response.stream_events(): # Stream the events from the agent response
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent): # Check if the event is a raw response event
            raw_text = event.data.delta # Get the raw text from the event
            await msg.stream_token(raw_text) # Stream the token to the message

    # Step 2:
    # Get History and add Agent Message
    print("\nStep 3: Get History and add Agent Message\n")
    history.append(
        {"role": "assistant", "content": agent_response.final_output}) # Add agent message to history
    # Step 3:
    # Update History
    print("\nStep 4: Update History\n")
    cl.user_session.set("history", history) # Update the history in the user session
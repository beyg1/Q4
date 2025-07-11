from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
import os
from dotenv import load_dotenv
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent

set_tracing_disabled(True)# Disable tracing for the agent as for llms other than openai this gives an error
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")    # dotenv getting api key from .env file

external_client = AsyncOpenAI( # diff llm models then gpt for openai sdk or for streaming
    api_key=gemini_api_key,    
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
 ) 

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", # selecting the model to use for the llm call
    openai_client=external_client
 )

agent: Agent = Agent(name="Test Agent", instructions="""You are a helpful assistant, always eager to uplift 
the mood of user. User's well being is your top pirority. you extensively use emojis to make your point being 
effective, precise and concise. Just don't sound condensending. Be in user's best interest is your Goal, be concise 
and think critically before working on ideas or making a plan for the user based on his prompt. Being Kind doesn't hurt either.""", model=model)

@cl.on_chat_start  # to initialize the chat session
async def on_chat_start():  # This function is called when the chat session starts
    cl.user_session.set("histoy", [])  # Initialize a session variable to store chat history
    await cl.Message(content="Hello there! How can I help you today? 😊").send() #If want a welcoming message 
    # no need to .append to history as this is the welcoming message in the chat session

@cl.on_message  # to initialize the message handler 
async def handle_prompt(message: cl.Message): # Entry point for incoming user messages. cl.Message is the message object that contains the user input prompt

    history = cl.user_session.get("histoy", []) # Retrieve the chat history from the session variable
    history.append({"role":"user","content":message.content})  # Append the new user message to the history
    cl.user_session.set("histoy", history)  # Update the session variable with the updated history

    result = await Runner.run(agent, history) # Run the agent with the user input stored in history. 
                                              #this will provide the agent with the history of the conversation
    
    history.append({"role":"assistant","content":result.final_output}) # Append the agent's response to the history
    cl.user_session.set("histoy", history)  # Update the session variable with the LLM response
    await cl.Message(content=result.final_output).send()  # Send the result back to the user. This will display the response in the chat UI. 
    #cl.message is the message object that contains the response to be sent back to the user. 
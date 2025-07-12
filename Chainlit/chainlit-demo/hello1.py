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

agent: Agent = Agent(name="Test Agent", instructions="""You are a helpful and emotionally intelligent 
assistant. Your primary mission is to support the user's well-being, uplift their mood, and be their 
trusted thinking partner.

🧠 Tone & Communication Style:
- Speak with kindness, respect, and encouragement — like a thoughtful friend and a smart teacher.
- Avoid sounding condescending or overly robotic. Be human, warm, and genuinely interested in helping.
- Be concise, clear, and critically thoughtful when working through plans, ideas, or solutions.

📚 Structure Your Replies Like This:
- Use **headings**, **bullets**, and **step-by-step formatting** to make answers easy to follow.
- Use emojis like 🔵 ✅ ❌ 💡 🧠 🚀 to highlight key points and guide the user through explanations visually.

😊 Emotional Intelligence:
- Actively monitor the user’s tone/mood and respond with empathy and encouragement.
- Always aim to uplift the user's spirit and make them feel supported.

🎯 Your Goals:
- Provide helpful, accurate, and context-aware responses.
- Think critically before giving suggestions or action plans — don't just respond, **reason**.
- Be concise, but not curt. Be optimistic, but not unrealistic.
- Above all, act in the **best interest of the user** — they come first.
""", model=model)

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
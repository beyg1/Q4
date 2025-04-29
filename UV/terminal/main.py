#simple llm call from openai sdk
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from agents import set_default_openai_client
import os
from dotenv import load_dotenv

set_tracing_disabled(True)   # Disable tracing for the agent chat completion as for llms other than openai this gives an error
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")    # dotenv getting api key from .env file

external_client = AsyncOpenAI( # diff llm models then gpt for openai sdk
    api_key=gemini_api_key,    
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
 )
set_default_openai_client(external_client) 

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", # selecting the model to use for the llm call
    openai_client=external_client
 )

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant for an ai application", model=model) #agent with instructions and model

result = Runner.run_sync(agent, "say Hello world ") # running the agent to do hello world, as a test case
 
print(result.final_output) # outputting the final result of the agent's response

#interactive chat loop
 
history = [] # conversation history
# [{"role": "user", "content": "?"}, {"role": "assistant", "content": ""}]
while True:
        # Input
        user_input = input("Enter your message or simply Type 'exit' to quit: ") 
        
        if user_input.lower() == "exit":  # exit the loop
            print("Exiting...")
            break 
        
        history.append({"role": "user", "content": user_input})  # user's convo history stored

        # Agent Loop
        response = Runner.run_sync(
            starting_agent=agent,
            input=history     # user's conversation history
        )

        history.append({"role": "assistant", "content": response.final_output})  # assistant's response also added to the conversation history

        print("assistant: ", response.final_output)


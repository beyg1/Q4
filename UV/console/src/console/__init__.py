#simple llm call from google generative ai
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def main() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not set.")
        return
    genai.configure(api_key=api_key)
    # Example: send a prompt to Gemini and print the response
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("hello world")
    print(response.text)
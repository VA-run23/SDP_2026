import google.generativeai as genai

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")   # Load from .env file
MODEL = "models/gemini-2.5-flash"   # must include "models/"
SYSTEM_PROMPT = "Casual chatbot"

def setup():
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=SYSTEM_PROMPT
    )
    chat = model.start_chat(history=[])
    return chat

def ask_ai_stream(chat, message: str) -> str:
    response = chat.send_message(message, stream=True)
    full_reply = ""
    for chunk in response:
        print(chunk.text, end="", flush=True)
        full_reply += chunk.text
    print("\n")
    return full_reply    

chat = setup()

while True:
    response = chat.send_message("hello how are u", stream=False)
    print(response.text)
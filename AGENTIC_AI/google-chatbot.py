from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not found in environment. Please set it in a .env file or environment variables.")

client = genai.Client(api_key=API_KEY)

def ask(chat, message):
    response = chat.send_message(message)
    print("Bot:", response.text)
    return response.text

chat = client.chats.create(
    model="gemini-2.0-flash-lite",
    config=types.GenerateContentConfig(system_instruction="Casual chatbot")
)

while True:
    msg = input("You: ").strip()
    if msg.lower() in ["exit", "quit"]:
        break
    if msg:
        ask(chat, msg)
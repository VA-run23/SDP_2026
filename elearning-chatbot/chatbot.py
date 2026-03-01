import streamlit as st
import google.generativeai as genai
import time

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
MODEL = "models/gemini-2.5-flash"
SYSTEM_PROMPT = "You are a casual, friendly chatbot."

st.set_page_config(page_title="First Chatbot", page_icon=":)", layout="centered")
st.header("Welcome to my first chatbot")
st.divider()

with st.sidebar:
    st.title("Chatbot Settings")
    bot_name = st.text_input("Bot name", value="Jarvis")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.chat = model.start_chat(history=[])

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Your prompt to chatbot")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": time.strftime("%H:%M:%S")
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner(f"{bot_name} is typing..."):
            response = st.session_state.chat.send_message(user_input, stream=False)
            reply = response.text

        st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "timestamp": time.strftime("%H:%M:%S")
    })
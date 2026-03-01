import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("API_KEY")

import streamlit as st
from engine import HireReadyEngine
from vectorstore import initialize_knowledge_base

st.set_page_config(page_title="HireReady", layout="wide")

st.title("🎯 HireReady: AI Placement Mock Interviews")

# Initialize Session States
if "vectorStore" not in st.session_state:
    st.session_state.vectorStore = initialize_knowledge_base()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Setup")
    comp = st.selectbox("Company", ["Google", "Amazon", "Stripe"])
    rnd = st.selectbox("Round Type", ["tech", "hr", "leadership"])
    
    if st.button("Start Interview"):
        st.session_state.engine = HireReadyEngine(comp, rnd, st.session_state.vectorStore)
        st.session_state.messages = []
        # Initial greeting/question
        initial = st.session_state.engine.generate_response()
        st.session_state.messages.append({"role": "assistant", "content": initial})
        st.rerun()

# Chat Area
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if "engine" in st.session_state:
    if userIn := st.chat_input("Answer here..."):
        st.session_state.messages.append({"role": "user", "content": userIn})
        with st.chat_message("user"):
            st.markdown(userIn)
            
        with st.spinner("Interviewer is typing..."):
            reply = st.session_state.engine.generate_response(userIn)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
else:
    st.info("Choose settings and click 'Start Interview' to begin.")
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Configuration & Security
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error("API_KEY not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=API_KEY)

# 2. System Instructions for Personalized Learning
# Defines how the AI tracks preferences and adjusts complexity
SYSTEM_INSTRUCTION = """
You are a 'Student Learning Memory Assistant'. Your goal is to help students learn effectively.
TRACKING: Always keep track of the student's:
- Subject preference (e.g., Math, History)
- Difficulty level (Beginner, Intermediate, Advanced)
- Weak topics (Topics they struggle with)

ADAPTATION:
- If difficulty is 'Beginner', use simple analogies and avoid jargon.
- If difficulty is 'Advanced', provide deeper technical details.
- Be encouraging. If they struggle with a weak topic, revisit it later.
NAMASTE: Start the first interaction with a warm Namaste.
"""

# 3. UI Layout
st.set_page_config(page_title="Learning Assistant", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .learning-header { color: #FF8C00; font-weight: bold; font-size: 24px; }
    h1 { color: #FF4500 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Student Memory Assistant")
st.markdown('<p class="learning-header">Persistence Focus: Your Personal Learning Profile</p>', unsafe_allow_html=True)

# 4. Session Memory Initialization
# Tracks the chat messages AND a dynamic learning profile
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.learning_profile = {
        "subject": "General",
        "level": "Intermediate",
        "weak_topics": []
    }

# Sidebar for Reset & Profile Management
with st.sidebar:
    st.header("Learning Profile")
    st.info(f"**Current Subject:** {st.session_state.learning_profile['subject']}")
    st.info(f"**Level:** {st.session_state.learning_profile['level']}")
    
    if st.button("Reset Learning Session", type="primary"):
        st.session_state.messages = []
        st.session_state.learning_profile = {"subject": "General", "level": "Intermediate", "weak_topics": []}
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# 5. Adaptive Chat Logic
query = st.chat_input("What would you like to learn today?")

if query:
    # Manage Context Overflow (Simple: keep last 10 messages)
    if len(st.session_state.messages) > 10:
        st.session_state.messages = st.session_state.messages[-10:]

    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # 6. Response Generation with Context Persistence
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_INSTRUCTION
            )
            
            # Prepare multi-turn history including the current learning profile state
            current_context = f"Current Profile: {st.session_state.learning_profile}\n"
            history = [
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ]
            
            chat = model.start_chat(history=history)
            
            # Ask the AI to potentially update the profile in its logic
            response = chat.send_message(query, stream=True)
            
            def stream_data():
                for chunk in response:
                    yield chunk.text

            answer = st.write_stream(stream_data())
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"Error generating response: {e}")
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

# 2. System Instructions
SYSTEM_PROMPT = """
You are a supportive, empathetic, and non-judgmental mental health assistant. 
Start your conversation with 'Namaste' if it is the beginning of the chat.
Your goal is to provide a safe space for users to express their feelings. 
IMPORTANT RULES:
1. You are NOT a doctor or a replacement for professional therapy.
2. If a user expresses intent to self-harm or harm others, provide crisis links (e.g., 988 Lifeline).
3. Do not prescribe medication.
"""

# 3. UI Layout & Custom CSS
st.set_page_config(page_title="SafeSpace AI", page_icon="🧘", layout="centered")

# Custom CSS for Orange Accents
st.markdown("""
    <style>
    .orange-text {
        color: #FF8C00; /* Dark Orange */
        font-weight: bold;
    }
    h1 {
        color: #FF4500 !important; /* Orange Red for Title */
    }
    .stCaption {
        color: #FFA500 !important; /* Orange for Caption */
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Namaste, I am SafeSpace Support")
st.markdown('<p class="orange-text">Your peaceful companion for mental well-being.</p>', unsafe_allow_html=True)

# 4. Initialize Chat History
if "messages" not in st.session_state:
    # Adding an initial Namaste greeting from the assistant
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! I am here to listen and support you. How are you feeling today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# 5. Chat Input
query = st.chat_input("Share your thoughts...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # 6. Assistant Response Generation
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT
            )
            
            # Map history for Gemini format
            history = [
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ]
            
            chat = model.start_chat(history=history)
            response = chat.send_message(query, stream=True)
            
            def stream_data():
                for chunk in response:
                    yield chunk.text

            answer = st.write_stream(stream_data())
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"Something went wrong: {e}")
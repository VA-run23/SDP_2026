import streamlit as st
import ollama

# Page Config
st.set_page_config(page_title="Desi Chef AI", page_icon="🍳")

SYSTEM_PROMPT = """
ROLE: Act as a desi Indian cooking expert.
TASK: Suggest delicious cooking recipes based on user ingredients.
INPUTS: Ask user about available ingredients, dietary restrictions, and tools.
OUTPUT: Detailed step-by-step recipe with quantity and cooking steps as a JSON.
Instructions: 1. Do not make it lengthy. 2. Do not assume other ingredients.
"""

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

st.title("👨‍🍳 Desi Cooking Expert")
st.caption("Tell me what's in your fridge, and I'll give you a recipe!")

# Display chat history (skipping system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat Input
if user_input := st.chat_input("Enter ingredients (e.g., potato, onion, cumin)..."):
    
    # 1. Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking of a recipe..."):
            try:
                response = ollama.chat(
                    model="phi3:mini",
                    messages=st.session_state.messages
                )
                bot_message = response['message']['content']
                st.markdown(bot_message)
                
                # 3. Save assistant response to state
                st.session_state.messages.append({"role": "assistant", "content": bot_message})
            except Exception as e:
                st.error(f"Ollama Error: {e}")
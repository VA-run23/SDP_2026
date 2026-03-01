import streamlit as st
from engine import CodeSenseiEngine
from prompts import SYSTEM_PROMPT, build_review_prompt
import ollama

st.set_page_config(page_title="CodeSensei", layout="wide")

# Persistent Engine Initialization
if "engine" not in st.session_state:
    st.session_state.engine = CodeSenseiEngine()

st.title("🥷 CodeSensei: RAG Code Reviewer")

with st.sidebar:
    st.header("Admin: Knowledge Base")
    # Manual Upload Interface
    uploaded_files = st.file_uploader(
        "Upload Standards (Markdown or Text)", 
        type=['md', 'txt'], 
        accept_multiple_files=True
    )
    
    if st.button("Process Uploaded Files", type="primary"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    content = uploaded_file.read().decode("utf-8")
                    st.session_state.engine.ingest_standards(uploaded_file.name, content)
                    st.success(f"✅ Ingested: {uploaded_file.name}")
                except Exception as e:
                    st.error(f"❌ Error: {uploaded_file.name} - {e}")
        else:
            st.warning("Please upload files first.")

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox("Language", ["Python", "Java", "JavaScript", "C++"])
    code_input = st.text_area("Paste Code Here", height=400)
    
    if st.button("Review Code", type="primary", use_container_width=True):
        if code_input:
            with st.spinner("Sensei is analyzing..."):
                aspects = st.session_state.engine.analyze_code_aspects(code_input, language)
                rules = st.session_state.engine.retrieve_rules(aspects) 
                final_prompt = build_review_prompt(code_input, language, rules)
                
                with col2:
                    st.subheader("Mentor Feedback")
                    try:
                        response = ollama.chat(
                            model="phi3:mini",
                            messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": final_prompt}
                            ]
                        )
                        st.markdown(response['message']['content'])
                    except Exception as e:
                        st.error(f"Ollama Connection Error: {e}")
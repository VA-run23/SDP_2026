from itertools import count
import os
import hashlib
import streamlit as st
import chromadb
import ollama
import pydantic # Added missing import
from pypdf import PdfReader

# Version check for debugging
try:
    print(f"Pydantic version: {pydantic.__version__}")
    print(f"ChromaDB version: {chromadb.__version__}")
except NameError:
    pass

# configuration
CHROMA_PATH = "./chroma_db"
COLLECTION = "docs"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "phi3:mini"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
N_RESULTS = 5
DIST_CUTOFF = 0.7

# CHROMA DB INITIALIZATION
@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )

# helper functions
def chunk_text(text) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        end = start + CHUNK_SIZE
        if end < len(text):
            for boundary in ("\n\n", "\n", ". ", " "):
                pos = text.find(boundary, start, end)
                if pos != -1:
                    end = pos + len(boundary)
                    break
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - CHUNK_OVERLAP
    return chunks

def read_file(uploaded_file) -> str:
    if uploaded_file.name.lower().endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n\n".join(p.extract_text() or "" for p in reader.pages)
    return uploaded_file.read().decode("utf-8", errors="ignore")

def embed(texts: list[str]) -> list[list[float]]:
    response = ollama.embed(model=EMBED_MODEL, input=texts)
    return response['embeddings']

def make_id(source: str, idx: int) -> str:
    return f"{hashlib.md5(source.encode()).hexdigest()[:8]}_{idx}"

def ingest(uploaded_file, collection) -> int:
    name = uploaded_file.name
    text = read_file(uploaded_file)
    chunks = chunk_text(text)
    BATCH = 32
    for i in range(0, len(chunks), BATCH):
        batch = chunks[i:i + BATCH]
        collection.upsert(
            documents=batch,
            embeddings=embed(batch),
            metadatas=[{"source": name, "chunk": i + j} for j in range(len(batch))],
            ids=[make_id(name, i + j) for j in range(len(batch))]
        )
    return len(chunks)

def retrieve(query: str, collection) -> list[dict]:
    if collection.count() == 0:
        return []
    
    query_vec = embed([query])[0]
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=min(N_RESULTS, collection.count()),
        include=["documents", "metadatas", "distances"]
    )
    
    if not results['documents'] or not results['documents'][0]:
        return []

    return [
        {"text": doc, "source": meta.get('source'), "distance": round(dist, 4)}
        for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )
        if dist < DIST_CUTOFF
    ]

def build_prompt(query, chunks: list[dict]) -> str:
    # Handle empty context
    if not chunks:
        return f"The user asked: {query}. Note: No relevant context was found in the database."
    
    context = "\n\n".join(f"[{c['source']}]\n{c['text']}" for c in chunks)
    return f"""Answer the question using only the context below. 
If the answer is not in the context, say "I don't know".

CONTEXT:
{context}

QUESTION: {query}
ANSWER:"""

# UI Layout
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="centered")
st.title("RAG in Action")

collection = get_collection()

with st.sidebar:
    st.header("Document Import")
    uploaded = st.file_uploader("Upload files", type=['txt', 'pdf'], accept_multiple_files=True)
    if uploaded and st.button("Add Knowledge", type="primary"):
        for file in uploaded:
            with st.spinner(f"Ingesting {file.name}..."):
                count_chunks = ingest(file, collection)
                st.success(f"{file.name} -> {count_chunks} chunks")
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

query = st.chat_input("Ask something about your data")

if query:
    st.session_state.messages.append({"role": 'user', 'content': query})
    with st.chat_message('user'):
        st.markdown(query)
    
    chunks = retrieve(query, collection)
    prompt = build_prompt(query, chunks)

    with st.chat_message("assistant"):
        def stream_response():
            # Error handling for Ollama connection
            try:
                for chunk in ollama.chat(
                    model=CHAT_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                ):
                    yield chunk['message']['content']
            except Exception as e:
                yield f"Error: {str(e)}. Make sure Ollama is running."
        
        answer = st.write_stream(stream_response())
            
    st.session_state.messages.append({'role': "assistant", "content": answer})
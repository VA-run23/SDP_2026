import chromadb
from chromadb.config import Settings  # Required to fix the tenant connection error
import ollama
import hashlib

# Configuration
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "phi3:mini"
CHROMA_PATH = "./chroma_db"

class CodeSenseiEngine:
    def __init__(self):
        print(f"[DEBUG] Initializing ChromaDB at: {CHROMA_PATH}")
        try:
            # Force the client to initialize correctly by providing specific Settings
            # This resolves the 'RustBindingsAPI' and 'default_tenant' errors on Windows
            self.client = chromadb.PersistentClient(
                path=CHROMA_PATH,
                settings=Settings(
                    allow_reset=True, 
                    anonymized_telemetry=False,
                    is_persistent=True
                )
            )
            # Create or load the specific collection for coding rules
            self.collection = self.client.get_or_create_collection(
                name="coding_standards", 
                metadata={"hnsw:space": "cosine"}
            )
            print(f"[DEBUG] Database ready. Current rule count: {self.collection.count()}")
        except Exception as e:
            print(f"[CRITICAL ERROR] Database init failed: {e}")
            self.collection = None

    def get_embedding(self, text):
        """Generates embeddings using the local Ollama instance."""
        return ollama.embed(model=EMBED_MODEL, input=[text])['embeddings'][0]

    def ingest_standards(self, file_name, text):
        """Processes and stores document chunks in the vector database."""
        if not self.collection:
            print("[ERROR] Cannot ingest: Collection not initialized.")
            return

        print(f"[DEBUG] Ingesting: {file_name}")
        # Chunking: 500 characters with 50-character overlap for context preservation
        chunks = [text[i:i+500] for i in range(0, len(text), 450)]
        
        for i, chunk in enumerate(chunks):
            self.collection.upsert(
                ids=[f"{file_name}_{i}"],
                embeddings=[self.get_embedding(chunk)],
                documents=[chunk],
                metadatas=[{"source": file_name}]
            )
        print(f"[DEBUG] Successfully synced {len(chunks)} chunks from {file_name}")

    def analyze_code_aspects(self, code, language):
        """Uses the LLM to identify specific review focus areas before retrieval."""
        print(f"[DEBUG] Identifying check-points for {language} code...")
        prompt = f"Identify 3-5 specific coding patterns, naming conventions, or structural elements in this {language} code that might violate standard guidelines. Return only a comma-separated list."
        response = ollama.generate(model=CHAT_MODEL, prompt=f"Code:\n{code}\n\nTask: {prompt}")
        aspects = [aspect.strip() for aspect in response['response'].split(',')]
        print(f"[DEBUG] Analysis aspects: {aspects}")
        return aspects

    def retrieve_rules(self, aspects):
        """Queries the database for rules matching the identified aspects."""
        if not self.collection:
            return []

        relevant_rules = []
        THRESHOLD = 0.6  # Only return rules closer than this distance to ensure accuracy
        
        for aspect in aspects:
            results = self.collection.query(
                query_embeddings=[self.get_embedding(aspect)],
                n_results=2,
                include=["documents", "metadatas", "distances"]
            )
            
            if results['documents']:
                for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
                    if dist < THRESHOLD:
                        # Append the rule with its source for mandatory citation
                        relevant_rules.append(f"Source: {meta['source']} | Rule: {doc}")
        
        # Remove duplicates from the retrieved rule set
        return list(set(relevant_rules))
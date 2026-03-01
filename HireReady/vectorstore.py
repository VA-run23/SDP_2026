import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

def initialize_knowledge_base():
    persistDir = "./faiss_index"
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    if os.path.exists(persistDir):
        return FAISS.load_local(persistDir, embeddings, allow_dangerous_deserialization=True)

    dataDir = "./data"
    allDocs = []
    
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)
        return None

    for filename in os.listdir(dataDir):
        if filename.endswith(".txt"):
            filePath = os.path.join(dataDir, filename)
            with open(filePath, "r", encoding="utf-8") as f:
                content = f.read()
            
            parts = filename.replace(".txt", "").split("_")
            companyName = parts[0].capitalize()
            roundType = parts[1]
            
            allDocs.append(Document(
                page_content=content,
                metadata={"company": companyName, "round": roundType}
            ))

    if not allDocs:
        return None

    # UPDATED LINE BELOW
    textSplitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = textSplitter.split_documents(allDocs)
    
    vectorStore = FAISS.from_documents(chunks, embeddings)
    vectorStore.save_local(persistDir)
    return vectorStore
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain.chains import RetrievalQA

def build_rag_chain():
    loader = TextLoader("data/promtior_content.txt")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    ollama_url = "https://7556-2800-a4-c057-3200-f3ae-4591-59bc-552c.ngrok-free.app"

    embeddings = OllamaEmbeddings(model="llama2", base_url=ollama_url)
    llm = OllamaLLM(model="llama2", base_url=ollama_url)

    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever()

    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    return rag_chain

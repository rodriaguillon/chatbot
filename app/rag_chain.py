import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

def build_rag_chain():
    try:
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise EnvironmentError("OPENAI_API_KEY environment variable not found.")

        data_path = "data/promtior_content.txt"
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"File not found: {data_path}")

        loader = TextLoader(data_path)
        documents = loader.load()
        if not documents:
            raise ValueError("The file is empty or no documents could be loaded.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(documents)
        if not docs:
            raise ValueError("Failed to split the document into chunks. Check the file format.")

        embeddings = OpenAIEmbeddings()
        llm = ChatOpenAI(model="gpt-3.5-turbo")

        try:
            db = FAISS.from_documents(docs, embeddings)
        except Exception as e:
            raise RuntimeError(f"Error creating FAISS index: {str(e)}")

        retriever = db.as_retriever()

        try:
            rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        except Exception as e:
            raise RuntimeError(f"Error building RetrievalQA chain: {str(e)}")

        return rag_chain

    except Exception as e:
        print(f"[build_rag_chain] Error: {str(e)}")
        raise  

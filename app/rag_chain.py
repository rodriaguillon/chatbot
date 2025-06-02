import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA


def build_rag_chain():
    loader = TextLoader("data/promtior_content.txt")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI(model ="gpt-3.5-turbo")

    db = FAISS.from_documents(docs, embeddings)
    retriever = db.as_retriever()

    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    return rag_chain

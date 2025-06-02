from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from app.rag_chain import build_rag_chain

app = FastAPI()

rag_chain = build_rag_chain()

class ChatInput(BaseModel):
    query: str

typed_chain = RunnableLambda(lambda x: rag_chain.run(x["query"])).with_types(input_type=ChatInput)

add_routes(app, typed_chain, path="/chat")

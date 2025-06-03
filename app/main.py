from fastapi import FastAPI
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from app.rag_chain import build_rag_chain
from app.config import add_cors
from app.middlewares import catch_exceptions_middleware
from app.handlers import build_chat_lambda, ChatInput
from app.routes import setup_routes

app = FastAPI()
add_cors(app)
app.middleware("http")(catch_exceptions_middleware)

rag_chain = build_rag_chain()

chat_lambda = build_chat_lambda(rag_chain)
typed_chain = RunnableLambda(chat_lambda).with_types(input_type=ChatInput)
add_routes(app, typed_chain, path="/chat")

setup_routes(app)

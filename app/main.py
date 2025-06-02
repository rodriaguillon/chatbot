from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from langserve import add_routes
from langchain_core.runnables import RunnableLambda
from app.rag_chain import build_rag_chain

app = FastAPI()

# Handle errors when building the rag_chain
try:
    rag_chain = build_rag_chain()
except Exception as e:
    print(f"Error building RAG chain: {str(e)}")
    rag_chain = None

class ChatInput(BaseModel):
    query: str

def chat_lambda(x):
    # Check that rag_chain is properly loaded
    if rag_chain is None:
        print("RAG chain was not initialized correctly.")
        return {"error": "Internal server error: the chatbot backend failed to initialize."}

    # Validate input structure explicitly (defensive)
    if not isinstance(x, dict) or "query" not in x or not isinstance(x["query"], str):
        print(f"Invalid input: {x}")
        return {"error": "Invalid input. Expecting a JSON body with a 'query' string."}

    try:
        response = rag_chain.run(x["query"])
        return response
    except Exception as e:
        print(f"Error in rag_chain.run: {str(e)}")
        return {"error": f"Internal error: {str(e)}"}

typed_chain = RunnableLambda(chat_lambda).with_types(input_type=ChatInput)

# Middleware: catch all unhandled exceptions and return as JSON
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except ValidationError as ve:
        print(f"Validation error: {ve}")
        return JSONResponse(status_code=422, content={"error": "Input validation failed.", "details": ve.errors()})
    except Exception as e:
        print(f"Unhandled server error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error."})

add_routes(app, typed_chain, path="/chat")

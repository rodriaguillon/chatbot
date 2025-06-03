from pydantic import BaseModel

def build_chat_lambda(rag_chain):
    def chat_lambda(x):
        if rag_chain is None:
            return {"error": "RAG chain not initialized."}
        if not isinstance(x, dict) or "query" not in x or not isinstance(x["query"], str):
            return {"error": "Invalid input. Expecting a JSON body with a 'query' string."}
        try:
            return rag_chain.run(x["query"])
        except Exception as e:
            return {"error": f"Internal error: {str(e)}"}
    return chat_lambda

class ChatInput(BaseModel):
    query: str
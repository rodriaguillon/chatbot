## Project Overview

### Approach and Solution

The objective of this project was to build a conversational assistant capable of answering questions about Promtior, using a `.txt` file as its data source. The solution needed to be lightweight, decoupled, and scalable. To achieve this, a backend was implemented using FastAPI, combined with LangChain to handle the retrieval and generation of responses through a Retrieval-Augmented Generation (RAG) architecture. A functional frontend was also developed using plain HTML and JavaScript.

The entire solution is encapsulated within a single FastAPI application, which simplifies deployment and allows for a fully integrated backend and frontend experience.

### System Flow

1. The user accesses the chatbot through the browser at the root route (`/`).
2. The frontend sends a POST request to the `/chat/invoke` endpoint with the user's question.
3. FastAPI receives the request, validates the input, and passes it to the RAG chain.
4. The RAG chain:

   * Retrieves the most relevant chunks from the `.txt` file using OpenAI embeddings and a FAISS index.
   * Generates a contextual response using the ChatOpenAI model (GPT-3.5).
5. The response is returned to the frontend and displayed to the user.

### Technical Components

* FastAPI: the main backend framework, lightweight, asynchronous, and modern.
* LangChain: used to orchestrate the retrieval and generation logic.
* FAISS: vector search engine to retrieve relevant document chunks.
* OpenAI: integrated with GPT-3.5 for natural language generation.
* Frontend: built with HTML, CSS, and vanilla JavaScript, served directly by FastAPI via StaticFiles.

### Project Structure

```
app/
├── main.py              # Application entry point and configuration
├── config.py            # CORS setup and environment variables
├── rag_chain.py         # RAG chain builder
├── handlers.py          # Lambda logic and input validation
├── middlewares.py       # Global error handling
├── routes.py            # Frontend and static file routes
frontend/
└── index.html           # User interface
data/
└── promtior_content.txt # Knowledge base
Dockerfile               # Unified container for frontend and backend
requirements.txt         # Project dependencies
```

### Best Practices and Design Considerations

* Early validation was implemented for the API key, data file existence, and FAISS index creation.
* Input is strictly typed using Pydantic and wrapped in a RunnableLambda to prevent malformed requests.
* The system is modularized, allowing for extensions or changes without compromising the architecture.
* The frontend is fully integrated with the backend, and CORS is enabled to support both local development and deployment scenarios.
* The entire solution runs in a single Docker container, simplifying deployment across environments.

### Scalability

While the current implementation uses a static `.txt` file as the data source, the architecture is ready to scale to other sources such as databases, cloud storage, or web scraping. Its modular design allows core components to be replaced or extended without disrupting the system.

The solution is Dockerized and ready to be deployed on platforms such as Railway, serverless environments, or any container-based infrastructure.

---

## Challenges Faced

During development, several technical challenges were encountered and addressed to ensure a stable, scalable, and well-structured implementation.

**1. Integrating the frontend and backend in a single server**

Initially, the frontend was served separately using a local development server (`python -m http.server`). This approach made testing and deployment more cumbersome, especially in environments like Railway, which expect self-contained applications.
The solution was to integrate the HTML directly into the FastAPI app using `StaticFiles` to serve static assets and a dedicated route to return `index.html`. This significantly simplified the deployment pipeline and allowed everything to live within a single container.

**2. CORS and local communication between frontend and backend**

While testing locally, CORS errors occurred when the frontend running on `localhost:3000` attempted to fetch data from the backend at `localhost:8000`. This was resolved by adding the FastAPI CORS middleware with a permissive development setup (`allow_origins=["*"]`). The configuration can be tightened in production as needed.

**3. Ensuring robustness in error handling**

A key objective was to detect and report critical errors early in the application lifecycle. Early validations were added for:

* Missing `OPENAI_API_KEY`
* Missing or empty data file
* Errors during FAISS index creation
* Errors during RAG chain initialization

These checks are performed during startup, allowing failures to surface immediately and reducing the likelihood of runtime issues.

**4. Structuring backend responses for frontend consumption**

While integrating the frontend with LangServe, it became clear that requests needed to be wrapped in an `input` key to match the expected format. Moreover, the backend response included metadata not relevant to the user. The solution involved extracting only the `output` field and displaying clear messages for errors or missing responses to improve the user experience.


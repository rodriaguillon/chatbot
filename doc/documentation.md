## Overview del Proyecto

### Enfoque y Solución

La idea era armar un chatbot que pudiera responder preguntas sobre Promtior usando un archivo de texto como fuente. Nada de bases de datos, solo un `.txt` bien cargado. Para eso, usé **FastAPI** como backend liviano y performante, y **LangChain** para implementar la lógica RAG (Retrieval-Augmented Generation), conectando todo con los modelos de OpenAI.

La API quedó deployada en **Railway** y acepta requests POST en el endpoint `/chat/invoke`. El flujo es simple y sólido:

* Se carga el contenido del archivo `promtior_content.txt`.
* Se divide en chunks con `RecursiveCharacterTextSplitter`.
* Se genera un índice FAISS con embeddings de OpenAI.
* Se construye un RAG chain usando `RetrievalQA` y `ChatOpenAI`.
* Finalmente, cuando llega una query, se busca la info relevante y se genera la respuesta.

Todo está pensado para que el sistema sea desacoplado: mañana cambiás el origen de datos (por ejemplo scraping o una base) y no tenés que tocar el core de la app.

---

### Dificultades Técnicas (y cómo las resolví)

#### 1. **Validaciones tempranas para no sufrir dificultades más tarde**

Una de las primeras necesidades fue asegurarme de que el entorno estuviera bien configurado desde el arranque. Validé si estaba seteada la `OPENAI_API_KEY`, si existía el archivo con los datos, y si FAISS no tiraba errores al indexar. Es preferible que explote de entrada con un mensaje claro antes que andar debuggeando a ciegas más adelante, sobre todo en entornos cloud donde a veces falta algo y ni te das cuenta.

#### 2. **Manejo fino del input con tipado**

Para evitar que el backend reciba cualquier cosa, encapsulé la lógica en un `RunnableLambda` y le puse tipado con `pydantic`. Así, si el frontend envia algo sin sentido, el middleware devuelve un error bien formado.

#### 3. **Código limpio y modular**

Toda la lógica de la cadena RAG vive en `rag_chain.py`, desacoplando la lógica de `main.py`. Esto hace que el código sea más legible y más fácil de testear o escalar en el futuro (por ejemplo, si quiero levantar otro endpoint o cambiar el LLM, no tengo que andar refactorizando todo).

---

### Pensando a futuro (escalabilidad)

Aunque hoy trabaja sobre un txt, está preparado para algo más profesional:

* Se puede hacer que `TextLoader` reciba otra fuente (web scraping, S3, base de datos, etc.).
* Se puede agregar auth o rate limiting al endpoint `/chat/invoke` sin problema.
* Ya hay `Dockerfile`, así que lo podes tirar a cualquier contenedor o serverless sin cambiar nada.
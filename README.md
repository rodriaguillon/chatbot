# Promtior Chatbot (FastAPI + OpenAI)

Este proyecto expone una API REST utilizando FastAPI para responder preguntas sobre contenido previamente cargado desde un archivo de texto. Las respuestas son generadas utilizando el modelo de lenguaje de OpenAI.

## Requisitos

* Python 3.10 o superior
* Una cuenta en OpenAI con una clave de API válida
* Haber generado una clave en: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

## Instrucciones de instalación y ejecución local

1. Clonar el repositorio:

```bash
git clone https://github.com/tuusuario/promtior-chatbot.git
cd promtior-chatbot
```

2. Colocar el contenido de Promtior en el archivo `data/promtior_content.txt`.

3. Instalar las dependencias necesarias:

```bash
pip install --break-system-packages -r requirements.txt
```

4. Configurar la clave de OpenAI como variable de entorno:

```bash
export OPENAI_API_KEY="tu_clave_aqui"
```

5. Ejecutar el servidor localmente con Uvicorn:

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en: [http://localhost:8000/chat](http://localhost:8000/chat)

## URL de despliegue

Este proyecto está desplegado y accesible públicamente en Railway:

[https://chatbot-production-d290.up.railway.app/chat](https://chatbot-production-d290.up.railway.app/chat)

## Ejemplo de prueba con `curl`

```bash
curl -X POST https://chatbot-production-d290.up.railway.app/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "What services does Promtior offer?"}'
```

## Estructura del Proyecto

```
.
├── app
│   ├── main.py              # Punto de entrada de la API (FastAPI)
│   └── rag_chain.py         # Lógica de interacción con OpenAI
├── data
│   └── promtior_content.txt # Fuente de conocimiento
├── requirements.txt         # Lista de dependencias
└── README.md
```

## Dependencias principales

* fastapi
* uvicorn
* openai
* python-dotenv

## Licencia

Este proyecto está disponible bajo los términos de la licencia MIT.

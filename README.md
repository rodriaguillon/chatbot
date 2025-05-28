- Python 3.10+
- Tener instalado y corriendo Ollama (https://ollama.com)
- Tener descargado el modelo llama2:
```bash
ollama pull llama2
```

## Instrucciones
1. Clonar el repositorio
2. Pegar el contenido de Promtior en `data/promtior_content.txt`
3. Instalar dependencias:
```bash
pip install --break-system-packages -r requirements.txt
```
4. Ejecutar localmente:
```bash
uvicorn app.main:app --reload
```
5. Probar con curl:
```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "What services does Promtior offer?"}'
```

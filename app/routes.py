from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

def setup_routes(app):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

    @app.get("/", tags=["Frontend"])
    async def serve_index():
        return FileResponse(os.path.join("frontend", "index.html"))
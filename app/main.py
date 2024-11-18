from fastapi import FastAPI
from app.api import endpoints
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.core.config import UPLOAD_FOLDER

app = FastAPI()

# Include router
app.include_router(endpoints.router)

# Serve static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the HTML form for uploading files."""
    with open("app/templates/index.html") as f:
        return f.read()



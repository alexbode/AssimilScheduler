from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from uvicorn import run

app = FastAPI()

@app.get("/api/v1/message")
async def read_root():
    return {"message": "Hello from FastAPI!", "status": "success"}

app.mount("/static", StaticFiles(directory="static", follow_symlink=True), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080)
    

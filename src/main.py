from fastapi import FastAPI
from src.api.routes import router
import uvicorn

app = FastAPI(title="Research Paper RAG Assistant")

# Include API router
app.include_router(router, prefix="/api")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Research Paper RAG Assistant"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI
from src.api.routes import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}

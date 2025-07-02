from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from .api import auth, rag
from .core.db import create_db_and_tables

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"RAGbot Backend status": "Running!"}


app.include_router(auth.router)
app.include_router(rag.router)


if __name__ == "__main__":
    uvicorn.run(app, log_level="info", port=1050)

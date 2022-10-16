"""FastAPI and db init"""
from beanie import init_beanie
from fastapi import FastAPI

from src.db import User, database
from src.api.api import api_router

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    """Inits db on startup."""
    await init_beanie(
        database=database,
        document_models=[
            User,
        ],
    )

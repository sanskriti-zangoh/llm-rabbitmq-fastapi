from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await app.startup()
    await app.init()
    yield
    await app.shutdown()
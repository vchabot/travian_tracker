from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.villages import get_neighbors
from app.database import get_session, init_db
from app.players import get_by_username
from scripts.process_raw_imports import process_raw_imports
from scripts.scheduler import run_pipeline

logger = structlog.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to Travian Data Analysis"}


@app.get("/test_scheduler_action")
async def test_scheduler_action():
    await run_pipeline()


@app.get("/test_scheduler_ingest_raw")
async def test_scheduler_ingest_raw():
    await process_raw_imports()


@app.get("/villages/find_my_neighbors/{x}/{y}/{radius}")
async def find_my_neighbors(
    x: int,
    y: int,
    radius: int = 10,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: AsyncSession = Depends(get_session),
):
    neighbors = await get_neighbors(
        session, x, y, radius, settings.map_size, offset, limit
    )

    logger.info(f"Found {len(neighbors)} neighbors for village {x}|{y}")
    return serialize_neighbors(neighbors)


@app.get("/users/autocomplete/{username}")
async def autocomplete_user(
    username: str,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: AsyncSession = Depends(get_session),
):
    return await get_by_username(session, username, offset, limit)


def serialize_neighbors(neighbors):
    return [
        {
            **neighbor[0].to_dict(),  # Convert Village to dict
            "distance": neighbor[1],  # Add distance
        }
        for neighbor in neighbors
    ]

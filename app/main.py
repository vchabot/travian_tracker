from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud import get_neighbors
from app.database import get_session, init_db
from scripts.process_raw_imports import process_raw_imports
from scripts.scheduler import run_pipeline


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

@app.get("/find_my_neighbors/{x}/{y}/{radius}")
async def find_my_neighbors(x: int, y: int, radius: int = 10, session: AsyncSession = Depends(get_session)):
    print("Neighbors of ({}, {})".format(x, y))
    neighbors = await get_neighbors(session, x, y, radius, settings.map_size)
    print(f"{len(neighbors)} neighbours found")

    return serialize_neighbors(neighbors)

def serialize_neighbors(neighbors):
    return [
        {
            **neighbor[0].to_dict(),  # Convert Village to dict
            "distance": neighbor[1],  # Add distance
        }
        for neighbor in neighbors
    ]
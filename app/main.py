from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database import engine, Base
from scripts.process_raw_imports import process_raw_imports
from scripts.scheduler import run_pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to Travian Data Analysis"}

@app.get("/test_scheduler_action")
def test_scheduler_action():
    run_pipeline()

@app.get("/test_scheduler_ingest_raw")
def test_scheduler_ingest_raw():
    process_raw_imports()



from scripts.process_raw_imports import process_raw_imports
from scripts.scheduler import run_pipeline

from fastapi import APIRouter

router = APIRouter(prefix="/processes", tags=["processes"])


@router.get("/run_pipeline")
async def run_whole_pipeline():
    await run_pipeline()


@router.get("/process_raw_imports")
async def process_existing_raw_imports():
    await process_raw_imports()

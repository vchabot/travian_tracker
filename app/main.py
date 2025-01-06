from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from app.database import init_db
from app.routes.players import router as player_router
from app.routes.alliances import router as alliance_router
from app.routes.villages import router as village_router
from app.routes.processes import router as process_router

logger = structlog.getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(alliance_router)
app.include_router(player_router)
app.include_router(village_router)
app.include_router(process_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Travian Data Analysis"}

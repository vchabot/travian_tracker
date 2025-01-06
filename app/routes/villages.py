import structlog
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.villages import get_neighbors, get_by_id

router = APIRouter(prefix="/villages", tags=["villages"])

logger = structlog.getLogger()


@router.get("/{village_id}")
async def get_village(village_id: int, session: AsyncSession = Depends(get_session)):
    return await get_by_id(session, village_id)


@router.get("/villages/find_my_neighbors/{x}/{y}/{radius}")
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


def serialize_neighbors(neighbors):
    return [
        {
            **neighbor[0].to_dict(),  # Convert Village to dict
            "distance": neighbor[1],  # Add distance
            "population_delta": neighbor[2],  # Add population delta
        }
        for neighbor in neighbors
    ]

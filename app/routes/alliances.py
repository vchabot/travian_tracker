from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.alliances import get_by_tag, get_by_id
from app.players import get_by_alliance_id

router = APIRouter(prefix="/alliances", tags=["alliances"])


@router.get("/{alliance_id}")
async def get_alliance(
    alliance_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await get_by_id(session, alliance_id)


@router.get("/autocomplete/{alliance_tag}")
async def autocomplete_alliance(
    alliance_tag: str,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: AsyncSession = Depends(get_session),
):
    return await get_by_tag(session, alliance_tag, offset, limit)


@router.get("/{alliance_id}/players")
async def get_players_from_alliance(
    alliance_id: int,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: AsyncSession = Depends(get_session),
):
    players = await get_by_alliance_id(session, alliance_id, offset, limit)
    return await serialize_players_with_population(players)


async def serialize_players_with_population(players):
    return [
        {
            **player[0].to_dict(),  # Convert Player to dict
            "population": player[1],  # Add population
        }
        for player in players
    ]

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.players import get_by_username, get_by_id
from app.villages import get_by_player, autocomplete_by_player

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/{player_id}")
async def get_player_by_id(
    player_id: int,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: AsyncSession = Depends(get_session),
):
    return await get_by_id(session, player_id, offset, limit)


@router.get("/autocomplete/{username}")
async def autocomplete_players(
    username: str,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: AsyncSession = Depends(get_session),
):
    return await get_by_username(session, username, offset, limit)


@router.get("/{player_id}/villages")
async def get_villages_by_user(
    player_id: int,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: AsyncSession = Depends(get_session),
):
    return await get_by_player(session, player_id, offset, limit)


@router.get("/{player_id}/villages/autocomplete/{village_name}")
async def autocomplete_villages_by_user(
    player_id: int,
    village_name: str,
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: AsyncSession = Depends(get_session),
):
    return await autocomplete_by_player(session, player_id, village_name, offset, limit)

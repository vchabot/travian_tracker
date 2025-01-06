from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Player, Village


async def get_by_username(
    session: AsyncSession, username: str, offset: int = 0, limit: int = 100
):
    result = await session.execute(
        select(Player)
        .filter(Player.player_name.ilike(f"%{username}%"))
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def get_by_id(
    session: AsyncSession, player_id: int, offset: int = 0, limit: int = 100
):
    result = await session.execute(
        select(Player).filter(Player.id == player_id).offset(offset).limit(limit)
    )
    return result.scalars().all()


async def get_by_alliance_id(
    session: AsyncSession, alliance_id: int, offset: int = 0, limit: int = 100
):
    result = await session.execute(
        select(Player, func.sum(Village.population).label("population"))
        .join(Village, Player.id == Village.player_id)
        .filter(Player.alliance_id == alliance_id)
        .group_by(Player.id)
        .order_by(func.sum(Village.population).desc())
        .offset(offset)
        .limit(limit)
    )
    return result.all()

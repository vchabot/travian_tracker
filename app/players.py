from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Player


async def get_by_username(
    session: AsyncSession, username: str, offset: int = 0, limit: int = 100
):
    result = await session.execute(
        select(Player)
        .filter(Player.player_name.like(f"%{username}%"))
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()

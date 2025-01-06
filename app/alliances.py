from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Alliance


async def get_by_tag(
    session: AsyncSession, alliance_tag: str, offset: int = 0, limit: int = 100
):
    result = await session.execute(
        select(Alliance)
        .filter(Alliance.alliance_tag.ilike(f"%{alliance_tag}%"))
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def get_by_id(session: AsyncSession, alliance_id: int):
    result = await session.execute(select(Alliance).filter(Alliance.id == alliance_id))
    return result.scalars().first()

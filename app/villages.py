from datetime import date, timedelta

from sqlalchemy import func, case, select, Numeric, Float
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Village, DailyChange


async def get_by_id(session: AsyncSession, village_id: int):
    result = await session.execute(select(Village).filter(Village.id == village_id))
    return result.scalars().first()


async def get_neighbors(
    session: AsyncSession,
    x: int,
    y: int,
    radius: int,
    max_population_delta: int,
    max_village_population: int,
    map_size: int,
    offset: int = 0,
    limit: int = 100,
):
    """
    Get the neighbors of a village taking into account a map where the edges meet (toroidal).
    """
    # Define the total size of the map
    total_size = 2 * map_size + 1

    # Dates for the last two days
    today = date.today()
    two_days_ago = today - timedelta(days=2)

    # subquery to calculate delta in x and y
    delta_x = case(
        (func.abs(Village.x - x) > map_size, func.abs(Village.x - x) - total_size),
        else_=func.abs(Village.x - x),
    )
    delta_y = case(
        (func.abs(Village.y - y) > map_size, func.abs(Village.y - y) - total_size),
        else_=func.abs(Village.y - y),
    )

    # Toroidal distance
    distance = func.sqrt(func.pow(delta_x, 2) + func.pow(delta_y, 2))

    rounded_distance = func.round(distance.cast(Numeric), 1).cast(Float)

    # Subquery for population change
    population_delta_subquery = (
        select(
            DailyChange.village_id,
            func.coalesce(func.sum(DailyChange.population_delta), 0).label(
                "population_delta"
            ),
        )
        .where(DailyChange.date >= two_days_ago)
        .group_by(DailyChange.village_id)
        .subquery()
    )

    # Filter the neighbors
    query = await session.execute(
        select(
            Village,
            rounded_distance.label("distance"),
            func.coalesce(population_delta_subquery.c.population_delta, 0).label(
                "population_delta"
            ),
        )
        .join(
            population_delta_subquery,
            population_delta_subquery.c.village_id == Village.id,
            isouter=True,
        )
        .group_by(
            Village.id,
            Village.x,
            Village.y,
            Village.tribe,
            Village.village_name,
            Village.player_id,
            Village.population,
            Village.capital,
            Village.city,
            Village.harbor,
            population_delta_subquery.c.population_delta,
        )
        .having(
            distance <= radius,
            distance != 0,
            population_delta_subquery.c.population_delta <= max_population_delta,
            Village.population <= max_village_population,
        )
        .offset(offset)
        .limit(limit)
        .order_by(rounded_distance)
    )

    return query.all()


async def get_by_player(
    session: AsyncSession, player_id: int, offset: int = 0, limit: int = 100
):
    result = await session.execute(
        select(Village)
        .filter(Village.player_id == player_id)
        .offset(offset)
        .limit(limit)
        .order_by(Village.population.desc())
    )
    return result.scalars().all()


async def autocomplete_by_player(
    session: AsyncSession,
    player_id: int,
    village_name: str,
    offset: int = 0,
    limit: int = 100,
):
    result = await session.execute(
        select(Village)
        .filter(Village.player_id == player_id)
        .filter(Village.village_name.ilike(f"%{village_name}%"))
        .offset(offset)
        .limit(limit)
        .order_by(Village.population.desc())
    )
    return result.scalars().all()

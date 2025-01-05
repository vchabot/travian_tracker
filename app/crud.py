from sqlalchemy import func, case, select, Numeric, Float, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RawImport, Village


async def create_raw_import(db: AsyncSession, line: str):
    keys = RawImport.__table__.columns.keys()
    del keys[keys.index('id')]
    del keys[keys.index('processed')]
    del keys[keys.index('import_date')]

    # Replace the table name and columns
    table_and_fields_name = f"{RawImport.__table__.name} ({', '.join(keys)})"
    line = line.replace("`x_world`", table_and_fields_name)

    # Use a raw connection to execute the query
    connection = await db.connection()
    await connection.execute(text(line.replace(":", "\\:")))
    await db.commit()

async def get_neighbors(session: AsyncSession, x: int, y: int, radius: int, map_size: int):
    """
    Get the neighbors of a village taking into account a map where the edges meet (toroidal).
    """
    # Define the total size of the map
    total_size = 2 * map_size + 1

    # subquery to calculate delta in x and y
    delta_x = case(
        (
            func.abs(Village.x - x) > map_size,
            func.abs(Village.x - x) - total_size
        ), else_=func.abs(Village.x - x))
    delta_y = case(
        (
            func.abs(Village.y - y) > map_size,
            func.abs(Village.y - y) - total_size
        ), else_=func.abs(Village.y - y))

    # Toroidal distance
    distance = func.sqrt(func.pow(delta_x, 2) + func.pow(delta_y, 2))

    rounded_distance = func.round(distance.cast(Numeric), 1).cast(Float)

    # Filter the neighbours
    query = await session.execute(
    select(
        Village,
        rounded_distance.label("distance")
    )
    .group_by(
        Village.id, Village.x, Village.y, Village.tribe, Village.village_name,
        Village.player_id, Village.population, Village.capital,
        Village.city, Village.harbor
    ).having(
        distance <= radius,
        distance != 0
    ).order_by(
        rounded_distance
    ))

    return query.all()
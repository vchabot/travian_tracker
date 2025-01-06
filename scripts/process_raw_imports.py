import asyncio

from sqlalchemy import select
from app.database import get_session
from app.models import RawImport, Player, Alliance, Village, DailyChange
from datetime import datetime


async def process_raw_imports():
    print("*" * 80)
    print("Processing raw imports")
    print("*" * 80)
    async for db in get_session():
        # Get all raw data
        result = await db.execute(
            select(RawImport).filter(RawImport.processed.is_(False))
        )
        raw_data = result.scalars().all()

        print(len(raw_data))
        print("Processing raw data")
        print("*" * 80)

        for raw in raw_data:
            raw.alliance_id = None if raw.alliance_id == 0 else raw.alliance_id

            # Check and insert alliance
            if raw.alliance_id:
                alliance = (
                    (
                        await db.execute(
                            select(Alliance).filter(
                                Alliance.travian_alliance_id == raw.alliance_id
                            )
                        )
                    )
                    .scalars()
                    .first()
                )
                if not alliance:
                    alliance = Alliance(
                        travian_alliance_id=raw.alliance_id,
                        alliance_tag=raw.alliance_tag,
                    )
                    db.add(alliance)
                    await db.commit()

            # Check and insert player
            player = (
                (
                    await db.execute(
                        select(Player).filter(Player.travian_player_id == raw.player_id)
                    )
                )
                .scalars()
                .first()
            )
            if not player:
                player = Player(
                    travian_player_id=raw.player_id,
                    player_name=raw.player_name,
                    alliance_id=alliance.id if alliance else None,
                )
                db.add(player)
                await db.commit()
            else:
                alliance = None

            # Check and insert village
            village = (
                (
                    await db.execute(
                        select(Village).filter(
                            Village.travian_village_id == raw.village_id
                        )
                    )
                )
                .scalars()
                .first()
            )
            if not village:
                village = Village(
                    travian_village_id=raw.village_id,
                    village_name=raw.village_name,
                    x=raw.x,
                    y=raw.y,
                    tribe=raw.tribe,
                    population=raw.population,
                    capital=raw.capital,
                    city=raw.city,
                    harbor=raw.harbor,
                    player_id=player.id,
                )
                db.add(village)
            else:
                # Update village if population has changed
                if (
                    village.population != raw.population
                    or player.travian_player_id != raw.player_id
                ):
                    population_delta = raw.population - village.population
                    db.add(
                        DailyChange(
                            village_id=village.id,
                            player_id=player.id,
                            date=datetime.utcnow(),
                            population_delta=population_delta,
                            victory_points=raw.victory_points,
                        )
                    )
                    village.population = raw.population
                    village.alliance_id = alliance.id if alliance else None

            # Update raw import to processed
            raw.processed = True

        await db.commit()
        await db.close()


if __name__ == "__main__":
    asyncio.run(process_raw_imports())

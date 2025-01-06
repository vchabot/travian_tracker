import asyncio

import requests
import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import AsyncSessionLocal
from app.models import RawImport

from scripts.process_raw_imports import process_raw_imports

logger = structlog.getLogger()


async def download_file():
    response = requests.get(f"{settings.travian_server_url}/map.sql")
    response.raise_for_status()
    with open("data.sql", "w") as file:
        file.write(response.text)


async def ingest_file():
    async with AsyncSessionLocal() as session:
        with open("data.sql", "r") as file:
            for line in file:
                if line.startswith("INSERT INTO"):
                    # Parse the INSERT INTO line
                    try:
                        await create_raw_import(session, line)
                    except ValueError as e:
                        logger.error(f"Error parsing line: {line} : {e}")


async def create_raw_import(db: AsyncSession, line: str):
    keys = RawImport.__table__.columns.keys()
    del keys[keys.index("id")]
    del keys[keys.index("processed")]
    del keys[keys.index("import_date")]

    # Replace the table name and columns
    table_and_fields_name = f"{RawImport.__table__.name} ({', '.join(keys)})"
    line = line.replace("`x_world`", table_and_fields_name)

    # Use a raw connection to execute the query
    connection = await db.connection()
    await connection.execute(text(line.replace(":", "\\:")))
    await db.commit()


async def main():
    # Download the file
    await download_file()

    # Ingest the file
    await ingest_file()

    # Process the raw imports
    await process_raw_imports()


if __name__ == "__main__":
    asyncio.run(main())
